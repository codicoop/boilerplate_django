# Generated by Django 4.2.9 on 2024-04-08 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verification_code',
            field=models.CharField(default='0000'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
    ]
