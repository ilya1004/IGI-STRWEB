# Generated by Django 5.0.6 on 2024-09-10 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_service_app', '0032_delete_aboutcompany'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('text', models.TextField()),
                ('logo', models.ImageField(default='news/no_image.jpg', upload_to='images')),
                ('video_src', models.FilePathField(default='')),
                ('history', models.JSONField(default={})),
                ('requisites', models.TextField(default='')),
                ('certificate', models.TextField(default='')),
            ],
        ),
    ]
