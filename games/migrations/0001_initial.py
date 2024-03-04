# Generated by Django 5.0.3 on 2024-03-04 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLBGame',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('home_team', models.TextField()),
                ('away_team', models.TextField()),
                ('location', models.TextField()),
            ],
        ),
    ]
