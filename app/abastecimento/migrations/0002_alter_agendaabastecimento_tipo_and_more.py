# Generated by Django 4.0.4 on 2022-05-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abastecimento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendaabastecimento',
            name='tipo',
            field=models.CharField(choices=[('Mensal Fornecedores', 'Mensal Fornecedores'), ('Mensal Armazenado', 'Mensal Armazenado'), ('Quinzenal Alimentos', 'Quinzenal Alimentos'), ('Pedidos Itens Açougue', 'Pedidos Itens Açougue'), ('Pedidos Linea Verde', 'Pedidos Linea Verde')], max_length=32),
        ),
        migrations.AlterField(
            model_name='itemabastecimento',
            name='tipo',
            field=models.CharField(choices=[('Mensal Fornecedores', 'Mensal Fornecedores'), ('Mensal Armazenado', 'Mensal Armazenado'), ('Quinzenal Alimentos', 'Quinzenal Alimentos'), ('Pedidos Itens Açougue', 'Pedidos Itens Açougue'), ('Pedidos Linea Verde', 'Pedidos Linea Verde')], max_length=32),
        ),
    ]
