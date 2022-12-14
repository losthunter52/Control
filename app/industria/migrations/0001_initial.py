# Generated by Django 4.0.4 on 2022-05-13 17:23

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaIndustria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=96)),
                ('tipo', models.CharField(choices=[('0', 'Segunda'), ('1', 'Terça'), ('2', 'Quarta'), ('3', 'Quinta'), ('4', 'Sexta')], max_length=32)),
                ('data_cadastro', models.DateField(auto_now=True)),
                ('data_final', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaIndustria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ItemIndustria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=8, unique=True)),
                ('descricao', models.CharField(max_length=32, unique=True)),
                ('tipo', models.CharField(choices=[('0', 'Segunda'), ('1', 'Terça'), ('2', 'Quarta'), ('3', 'Quinta'), ('4', 'Sexta')], max_length=32)),
                ('data_cadastro', models.DateField(auto_now=True)),
                ('data_modificado', models.DateField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='industria.categoriaindustria')),
                ('empresas', models.ManyToManyField(to='core.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoIndustria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(default='', max_length=96)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.empresa')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='industria.agendaindustria')),
            ],
        ),
        migrations.CreateModel(
            name='QuantidadeItemIndustria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(default='', max_length=96)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('habilitado', models.CharField(default='', max_length=2)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='industria.itemindustria')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='industria.pedidoindustria')),
            ],
        ),
    ]
