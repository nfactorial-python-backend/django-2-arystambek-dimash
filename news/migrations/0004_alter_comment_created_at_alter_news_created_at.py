# Generated by Django 4.2.4 on 2023-08-12 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_comment_created_at_alter_news_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]