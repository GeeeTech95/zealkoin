# Generated by Django 3.0.5 on 2022-03-15 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0008_wallet_withdrawal_allowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalapplication',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('DECLINED', 'DECLINED')], default='PENDING', max_length=20),
        ),
        migrations.AlterField(
            model_name='withdrawalapplication',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_withdrawal', to=settings.AUTH_USER_MODEL),
        ),
    ]