# Generated by Django 3.2.9 on 2021-11-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='totp_uri',
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_token_sat',
            field=models.DateTimeField(null=True, verbose_name='confirmation_token_sent_at_time_stamp'),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_token',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
