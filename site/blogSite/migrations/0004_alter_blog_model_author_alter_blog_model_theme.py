# Generated by Django 4.1.6 on 2023-04-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogSite', '0003_theme_model_alter_user_account_image_blog_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_model',
            name='author',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='blog_model',
            name='theme',
            field=models.CharField(max_length=25),
        ),
    ]