# Generated by Django 4.2.1 on 2023-06-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_access', '0003_alter_userdefinition_emp_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdefinition',
            name='emp_ssh_key',
            field=models.TextField(null=True),
        ),
    ]
