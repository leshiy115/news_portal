# Generated by Django 5.0.1 on 2024-02-03 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_author_rating_alter_comment_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('A', 'Статья'), ('N', 'Новости')], default='A', max_length=1),
        ),
    ]
