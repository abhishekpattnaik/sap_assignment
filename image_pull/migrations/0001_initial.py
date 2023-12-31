# Generated by Django 4.2.7 on 2023-11-27 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_pull.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_file_path', models.CharField(blank=True, max_length=250, null=True)),
                ('file_name', models.CharField(max_length=150, unique=True)),
                ('source_url', models.URLField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', validators=[image_pull.models.validate_image_extension])),
                ('is_valid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
