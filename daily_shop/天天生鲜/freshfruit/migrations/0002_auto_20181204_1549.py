# Generated by Django 2.1.2 on 2018-12-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshfruit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='usershow',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='useraddress',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='usretel',
            field=models.CharField(default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='youbian',
            field=models.CharField(default='', max_length=6),
        ),
    ]
