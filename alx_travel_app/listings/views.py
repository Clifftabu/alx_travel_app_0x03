import requests
from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions



class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            amount = booking.total_price  # Adjust based on your Booking model
            callback_url = "http://127.0.0.1:8000/api/payments/verify/"

            headers = {
                "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
                "Content-Type": "application/json",
            }
            data = {
                "amount": str(amount),
                "currency": "ETB",
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "tx_ref": f"{request.user.id}-{booking.id}",
                "callback_url": callback_url,
            }
            response = requests.post(
                "https://api.chapa.co/v1/transaction/initialize",
                json=data,
                headers=headers,
            )
            result = response.json()
            if result["status"] == "success":
                checkout_url = result["data"]["checkout_url"]
                transaction_id = result["data"]["tx_ref"]
                Payment.objects.create(
                    booking=booking,
                    user=request.user,
                    amount=amount,
                    transaction_id=transaction_id,
                    status="Pending",
                )
                return Response({"checkout_url": checkout_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

class VerifyPaymentView(APIView):
    permission_classes = [permissions.AllowAny]  # Webhook callbacks

    def get(self, request):
        tx_ref = request.GET.get("tx_ref")
        if not tx_ref:
            return Response({"error": "Missing tx_ref"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }
        response = requests.get(
            f"https://api.chapa.co/v1/transaction/verify/{tx_ref}",
            headers=headers,
        )
        result = response.json()

        if result["status"] == "success" and result["data"]["status"] == "success":
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                payment.status = "Completed"
                payment.save()
                return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                payment.status = "Failed"
                payment.save()
            except Payment.DoesNotExist:
                pass
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
