# Generated by Django 5.0.1 on 2024-03-06 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0007_alter_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="disease",
            field=models.CharField(default="Nothing", max_length=100),
        ),
    ]
