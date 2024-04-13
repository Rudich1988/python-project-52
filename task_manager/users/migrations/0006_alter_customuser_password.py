# Generated by Django 4.2.10 on 2024-03-04 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(3, message='Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.')]),
        ),
    ]