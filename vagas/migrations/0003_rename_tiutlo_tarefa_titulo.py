# Generated by Django 4.1.3 on 2022-11-15 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_rename_data_final_tarefa_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarefa',
            old_name='tiutlo',
            new_name='titulo',
        ),
    ]