# Generated by Django 3.1.2 on 2020-11-28 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketproduct',
            name='basket',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='bboard.basket', verbose_name='Корзина'),
        ),
    ]
