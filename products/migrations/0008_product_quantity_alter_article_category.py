# Generated by Django 4.2.7 on 2024-01-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_content_article_main_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Haircare', 'Haircare'), ('Skincare', 'Skincare'), ('Bodycare', 'Bodycare'), ('Fragrance', 'Fragrance')], default='Haircare', max_length=20),
        ),
    ]