# Generated by Django 3.0.5 on 2022-03-07 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
import wallet.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='name you wish to call the investment plan', max_length=40)),
                ('slug', models.SlugField(blank=True)),
                ('max_cost', models.FloatField(blank=True, help_text='maximum investment for thie plan,currency is USD', null=True)),
                ('min_cost', models.FloatField(help_text='minimum investment for thie plan,currency is USD')),
                ('duration', models.PositiveIntegerField(help_text='plan duration in days')),
                ('interest_rate', models.FloatField(help_text='in %,e.g 50,100,200')),
                ('referral_percentage', models.FloatField(help_text='determines how much referal bonus a use gets when a referral makes deposit on this plan')),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['min_cost'],
            },
        ),
        migrations.CreateModel(
            name='WithdrawalApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('coin', models.CharField(choices=[('BTC', 'BTC'), ('USDT', 'USDT'), ('ETH', 'ETH'), ('BNB', 'BNB')], max_length=10)),
                ('wallet_address', models.CharField(help_text='Please enter the correct address matching the selected coin,as any mismatch might lead to complete loss', max_length=200)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'PROCESSING'), ('APPROVED', 'APPROVED'), ('DECLINED', 'DECLINED')], default='PENDING', max_length=20)),
                ('amount_paid', models.FloatField(blank=True, null=True)),
                ('is_received', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pending_withdrawal', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('plan_start', models.DateTimeField(blank=True, null=True)),
                ('plan_end', models.DateTimeField(blank=True, null=True)),
                ('initial_balance', models.FloatField(blank=True, default=0.0)),
                ('expected_maximum_balance', models.FloatField(blank=True, default=0.0)),
                ('referral_earning', models.FloatField(default=0.0)),
                ('past_deposit_earning', models.FloatField(default=0.0)),
                ('past_deposits', models.FloatField(default=0.0)),
                ('funded_earning', models.FloatField(default=0.0)),
                ('withdrawals', models.FloatField(default=0.0)),
                ('plan_is_active', models.BooleanField(blank=True, default=False)),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wallet_subscribers', to='wallet.Plan')),
                ('previous_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_plan', to='wallet.Plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(editable=False, max_length=15)),
                ('transaction_type', models.CharField(choices=[('WITHDRAWAL', 'WITHDRAWAL'), ('DEPOSIT', 'DEPOSIT'), ('BONUS', 'BONUS'), ('AIR DROP', 'AIR DROP'), ('REFERAL EARNING', 'REFERAL EARNING')], max_length=20)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Declined', 'Declined'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('coin', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_transaction', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PendingDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('is_declined', models.BooleanField(default=False)),
                ('decline_reason', models.TextField(null=True)),
                ('payment_method', models.CharField(choices=[('USDT', 'USDT'), ('ETH', 'ETH'), ('BTC', 'BTC'), ('LTC', 'LTC')], max_length=10)),
                ('payment_proof', models.FileField(upload_to=wallet.models.PendingDeposit.get_path)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pending_deposit', to='wallet.Plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_pending_deposit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]