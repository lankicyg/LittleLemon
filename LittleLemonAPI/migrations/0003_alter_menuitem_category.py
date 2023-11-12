# Generated by Django 4.2.6 on 2023-10-23 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0002_category_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LittleLemonAPI.category'),
        ),
    ]
