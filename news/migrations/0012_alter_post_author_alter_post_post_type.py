# Generated by Django 5.0.1 on 2024-05-01 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_category_name_en_category_name_ru_post_text_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='news.author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('A', 'Article'), ('N', 'News')], default='A', max_length=1, verbose_name='Type'),
        ),
    ]
