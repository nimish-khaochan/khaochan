# Generated by Django 5.1.7 on 2025-03-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_newsitem_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='is_top_news',
            field=models.BooleanField(default=False, help_text='Mark if this item is top news.'),
        ),
        migrations.AlterField(
            model_name='newsitem',
            name='category',
            field=models.CharField(blank=True, choices=[('alerts', 'Alerts'), ('local', 'Local News'), ('culture', 'Culture'), ('visas', 'Visa Regulations'), ('business', 'Business')], help_text='Select a category for this news item.', max_length=50, null=True),
        ),
    ]
