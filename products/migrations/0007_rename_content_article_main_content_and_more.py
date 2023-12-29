# Generated by Django 4.2.7 on 2023-12-29 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_article_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='content',
            new_name='main_content',
        ),
        migrations.AddField(
            model_name='article',
            name='secondary_content',
            field=models.TextField(default=''),
        ),
    ]
