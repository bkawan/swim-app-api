# Generated by Django 2.1.8 on 2019-04-07 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190407_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='swimmers',
        ),
        migrations.AddField(
            model_name='competition',
            name='swimmers',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='core.Swimmer'),
            preserve_default=False,
        ),
    ]