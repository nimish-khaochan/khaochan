# Generated by Django 5.1.7 on 2025-03-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_newsitem_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsitem',
            name='image',
        ),
        migrations.AddField(
            model_name='newsitem',
            name='image_url',
            field=models.URLField(blank=True, help_text='URL of the article image.', null=True),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='publisher_logo_url',
            field=models.URLField(blank=True, help_text="URL of the publisher's logo image from the RSS feed.", null=True),
        ),
        migrations.AddField(
            model_name='newsitem',
            name='publisher_name',
            field=models.CharField(blank=True, help_text='Name of the publisher from the RSS feed.', max_length=200, null=True),
        ),
    ]
