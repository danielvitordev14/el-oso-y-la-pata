# Generated by Django 5.2.2 on 2025-06-12 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_itemhistoria_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemhistoria',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
