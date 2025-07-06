from django.core.management.base import BaseCommand
from listings.models import User, Listing, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.create_users(options['users'])
        self.create_listings(options['listings'])
        self.create_bookings(options['bookings'])
        self.create_reviews(options['reviews'])

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database!')
        )

    def create_users(self, count):
        """Create sample users"""
        self.stdout.write(f'Creating {count} users...')
        
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'phone_number': '+1234567890'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'phone_number': '+1234567891'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson', 'phone_number': '+1234567892'},
            {'username': 'alice_brown', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Brown', 'phone_number': '+1234567893'},
            {'username': 'charlie_davis', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Davis', 'phone_number': '+1234567894'},
            {'username': 'diana_miller', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Miller', 'phone_number': '+1234567895'},
            {'username': 'evan_garcia', 'email': 'evan@example.com', 'first_name': 'Evan', 'last_name': 'Garcia', 'phone_number': '+1234567896'},
            {'username': 'fiona_martinez', 'email': 'fiona@example.com', 'first_name': 'Fiona', 'last_name': 'Martinez', 'phone_number': '+1234567897'},
            {'username': 'george_anderson', 'email': 'george@example.com', 'first_name': 'George', 'last_name': 'Anderson', 'phone_number': '+1234567898'},
            {'username': 'helen_taylor', 'email': 'helen@example.com', 'first_name': 'Helen', 'last_name': 'Taylor', 'phone_number': '+1234567899'},
        ]

        for i in range(count):
            if i < len(users_data):
                user_data = users_data[i]
            else:
                user_data = {
                    'username': f'user_{i+1}',
                    'email': f'user{i+1}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i+1}',
                    'phone_number': f'+123456{i+1:04d}'
                }
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'phone_number': user_data['phone_number']
                }
            )
            if created:
                user.set_password('password123')
                user.save()

    def create_listings(self, count):
        """Create sample listings"""
        self.stdout.write(f'Creating {count} listings...')
        
        listings_data = [
            {
                'name': 'Cozy Downtown Apartment',
                'description': 'Beautiful 2-bedroom apartment in the heart of downtown. Walking distance to restaurants, shops, and attractions.',
                'location': 'New York, NY',
                'pricepernight': Decimal('120.00')
            },
            {
                'name': 'Beachfront Villa',
                'description': 'Stunning ocean view villa with private beach access. Perfect for a relaxing getaway.',
                'location': 'Malibu, CA',
                'pricepernight': Decimal('350.00')
            },
            {
                'name': 'Mountain Cabin Retreat',
                'description': 'Rustic cabin nestled in the mountains. Great for hiking and outdoor activities.',
                'location': 'Aspen, CO',
                'pricepernight': Decimal('200.00')
            },
            {
                'name': 'Modern Loft in Arts District',
                'description': 'Contemporary loft with exposed brick walls and high ceilings in trendy arts district.',
                'location': 'Los Angeles, CA',
                'pricepernight': Decimal('180.00')
            },
            {
                'name': 'Historic Brownstone',
                'description': 'Charming brownstone with original details and modern amenities.',
                'location': 'Boston, MA',
                'pricepernight': Decimal('160.00')
            },
            {
                'name': 'Luxury Penthouse',
                'description': 'High-end penthouse with panoramic city views and premium furnishings.',
                'location': 'Miami, FL',
                'pricepernight': Decimal('450.00')
            },
            {
                'name': 'Garden Cottage',
                'description': 'Peaceful cottage surrounded by beautiful gardens and walking trails.',
                'location': 'Portland, OR',
                'pricepernight': Decimal('95.00')
            },
            {
                'name': 'Urban Studio',
                'description': 'Compact but efficient studio apartment perfect for solo travelers.',
                'location': 'Seattle, WA',
                'pricepernight': Decimal('80.00')
            },
            {
                'name': 'Lakeside Cabin',
                'description': 'Serene cabin on the lake with kayaks and fishing equipment included.',
                'location': 'Lake Tahoe, CA',
                'pricepernight': Decimal('220.00')
            },
            {
                'name': 'Desert Oasis',
                'description': 'Modern home in the desert with pool and stunning sunset views.',
                'location': 'Phoenix, AZ',
                'pricepernight': Decimal('190.00')
            }
        ]

        users = list(User.objects.all())
        if not users:
            self.stdout.write(
                self.style.ERROR('No users found. Please create users first.')
            )
            return

        for i in range(count):
            if i < len(listings_data):
                listing_data = listings_data[i]
            else:
                listing_data = {
                    'name': f'Property {i+1}',
                    'description': f'Description for property {i+1}',
                    'location': f'Location {i+1}',
                    'pricepernight': Decimal(str(random.randint(50, 300)))
                }

            Listing.objects.create(
                host=random.choice(users),
                **listing_data
            )

    def create_bookings(self, count):
        """Create sample bookings"""
        self.stdout.write(f'Creating {count} bookings...')
        
        listings = list(Listing.objects.all())
        users = list(User.objects.all())
        
        if not listings or not users:
            self.stdout.write(
                self.style.ERROR('No listings or users found. Please create them first.')
            )
            return

        statuses = ['pending', 'confirmed', 'canceled', 'completed']
        
        for i in range(count):
            # Generate random date range
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            # Ensure user is not the host of the listing
            listing = random.choice(listings)
            available_users = [user for user in users if user != listing.host]
            if not available_users:
                continue
            
            # Calculate total price
            nights = (end_date - start_date).days
            total_price = listing.pricepernight * nights
                
            Booking.objects.create(
                property=listing,
                user=random.choice(available_users),
                checkin=start_date,
                checkout=end_date,
                total_price=total_price,
                status=random.choice(statuses)
            )

    def create_reviews(self, count):
        """Create sample reviews"""
        self.stdout.write(f'Creating {count} reviews...')
        
        listings = list(Listing.objects.all())
        users = list(User.objects.all())
        
        if not listings or not users:
            self.stdout.write(
                self.style.ERROR('No listings or users found. Please create them first.')
            )
            return

        review_comments = [
            "Great place to stay! Very clean and comfortable.",
            "Amazing location with beautiful views. Highly recommend!",
            "Host was very responsive and helpful. Will stay again.",
            "Perfect for a weekend getaway. Everything was as described.",
            "Exceeded expectations! The property was even better than the photos.",
            "Good value for money. Clean and well-maintained.",
            "Lovely place with all necessary amenities. Very peaceful.",
            "Great experience overall. The host went above and beyond.",
            "Beautiful property in a fantastic location. Five stars!",
            "Comfortable stay with easy check-in and check-out process."
        ]

        created_reviews = set()
        attempts = 0
        max_attempts = count * 3
        
        while len(created_reviews) < count and attempts < max_attempts:
            attempts += 1
            listing = random.choice(listings)
            available_users = [user for user in users if user != listing.host]
            if not available_users:
                continue
                
            user = random.choice(available_users)
            review_key = (listing.listing_id, user.user_id)
            
            if review_key not in created_reviews:
                Review.objects.create(
                    property=listing,
                    user=user,
                    rating=random.randint(3, 5),  # Bias towards higher ratings
                    comment=random.choice(review_comments)
                )
                created_reviews.add(review_key)