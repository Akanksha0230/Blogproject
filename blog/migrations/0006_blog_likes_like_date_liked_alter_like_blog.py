# Generated by Django 4.2.13 on 2024-06-08 09:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blog_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='like',
            name='date_liked',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='like',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_set', to='blog.blog'),
        ),
    ]
