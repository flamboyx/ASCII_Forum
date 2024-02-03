# Generated by Django 4.2.9 on 2024-02-02 22:54

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_comment_image_reply_image_tred_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tred',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='tred',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Тема'),
        ),
    ]