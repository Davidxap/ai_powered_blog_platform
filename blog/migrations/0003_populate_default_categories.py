from django.db import migrations


def create_default_categories(apps, schema_editor):
    """
    Create default blog categories if they don't exist
    """
    Category = apps.get_model('blog', 'Category')
    
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
    
    for category_name in default_categories:
        if not Category.objects.filter(name=category_name).exists():
            Category.objects.create(name=category_name)


def reverse_migration(apps, schema_editor):
    """
    Remove default categories if migration is reversed
    """
    Category = apps.get_model('blog', 'Category')
    
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
    
    Category.objects.filter(name__in=default_categories).delete()


class Migration(migrations.Migration):
    
    dependencies = [
        ('blog', '0002_alter_post_categories'),  # Adjust to your last migration
    ]
    
    operations = [
        migrations.RunPython(
            create_default_categories,
            reverse_code=reverse_migration
        ),
    ]
