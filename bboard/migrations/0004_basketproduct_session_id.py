# Generated by Django 3.1.2 on 2020-12-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0003_basket_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketproduct',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
