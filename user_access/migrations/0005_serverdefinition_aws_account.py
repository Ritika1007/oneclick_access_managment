# Generated by Django 4.2.1 on 2023-06-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_access', '0004_userdefinition_emp_ssh_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverdefinition',
            name='aws_account',
            field=models.CharField(default='Cigar', max_length=50),
        ),
    ]
