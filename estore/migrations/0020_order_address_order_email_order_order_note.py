# Generated by Django 5.0.2 on 2024-05-27 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore', '0019_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=None, max_length=120, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=None, max_length=254, verbose_name='Электронная почта'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_note',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу'),
        ),
    ]
