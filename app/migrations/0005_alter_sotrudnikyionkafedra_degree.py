# Generated by Django 4.2.7 on 2023-12-17 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_nir_type_alter_sotrudnikyionkafedra_degree_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sotrudnikyionkafedra',
            name='degree',
            field=models.CharField(choices=[('kn', 'kandidat nauk'), ('dn', 'doktor nauk'), ('mg', 'magistr'), ('bk', 'bakalavr')], max_length=3),
        ),
    ]
