# Generated by Django 4.2.2 on 2023-06-25 13:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_communitypost_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitypost",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]