# Generated by Django 4.2.10 on 2024-03-31 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("paystack_reference", models.CharField(max_length=200, unique=True)),
                ("amount", models.CharField(max_length=80)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("DC", "Debit Card"), ("BT", "Bank Transfer")],
                        default="DC",
                        max_length=2,
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
