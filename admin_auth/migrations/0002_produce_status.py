# Generated by Django 3.2.8 on 2025-06-02 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produce',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
