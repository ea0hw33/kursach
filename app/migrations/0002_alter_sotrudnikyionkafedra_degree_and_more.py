# Generated by Django 5.0.1 on 2024-01-14 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sotrudnikyionkafedra',
            name='degree',
            field=models.CharField(choices=[('bk', 'bakalavr'), ('mg', 'magistr'), ('dn', 'doktor nauk'), ('kn', 'kandidat nauk')], max_length=3),
        ),
        migrations.AlterField(
            model_name='sotrudnikyionkafedra',
            name='job',
            field=models.CharField(choices=[('as', 'asperan'), ('te', 'teacher')], max_length=3),
        ),
    ]