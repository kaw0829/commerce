# Generated by Django 3.1.7 on 2021-04-05 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210404_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.CharField(default='please provide a description', max_length=200),
        ),
        migrations.AddField(
            model_name='listing',
            name='listing_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
