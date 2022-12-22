# Generated by Django 4.0.5 on 2022-12-22 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpapp', '0008_profile_judge_cnt_profile_washer_cnt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='static/upload_img/img/image.jpg', upload_to='report/')),
                ('ai_result', models.CharField(max_length=255)),
                ('user_result', models.CharField(max_length=255)),
            ],
        ),
    ]
