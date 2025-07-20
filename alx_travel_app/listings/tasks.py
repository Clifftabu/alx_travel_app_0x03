from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(email, subject, message):
    send_mail(
        subject,
        message,
        'noreply@alxtravelapp.com',
        [email],
        fail_silently=False,
    )
