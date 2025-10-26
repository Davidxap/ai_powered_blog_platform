"""
Management command to populate default blog categories
Usage: python manage.py populate_categories
"""
from django.core.management.base import BaseCommand
from blog.models import Category


class Command(BaseCommand):
    help = 'Populate database with default blog categories'

    def handle(self, *args, **kwargs):
        """
        Create default categories if they don't exist
        """
        # Define default categories
        default_categories = [
            'Technology',
            'Artificial Intelligence',
            'Programming',
            'Web Development',
            'Data Science',
            'Tutorial',
            'News',
            'Review',
            'Opinion',
            'Business',
            'Productivity',
            'Lifestyle',
        ]

        created_count = 0
        existing_count = 0

        self.stdout.write(self.style.MIGRATE_HEADING('Creating categories...'))

        for category_name in default_categories:
            category, created = Category.objects.get_or_create(
                name=category_name
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {category_name}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'- Already exists: {category_name}')
                )

        # Summary
        self.stdout.write(self.style.MIGRATE_HEADING('\nSummary:'))
        self.stdout.write(
            self.style.SUCCESS(f'Categories created: {created_count}')
        )
        self.stdout.write(
            self.style.WARNING(f'Categories already existed: {existing_count}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total categories in database: {Category.objects.count()}')
        )
