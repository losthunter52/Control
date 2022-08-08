# Generated by Django 4.0.4 on 2022-05-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastecimento', '0005_remove_quantidadeitemabastecimento_acougue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantidadeitemabastecimento',
            name='acougue',
            field=models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], default='N', max_length=2),
        ),
        migrations.AddField(
            model_name='quantidadeitemabastecimento',
            name='loja',
            field=models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], default='N', max_length=2),
        ),
        migrations.AddField(
            model_name='quantidadeitemabastecimento',
            name='padaria',
            field=models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], default='N', max_length=2),
        ),
        migrations.AddField(
            model_name='quantidadeitemabastecimento',
            name='verdura',
            field=models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], default='N', max_length=2),
        ),
    ]
