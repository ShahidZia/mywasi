# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='canceled_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='payment_type',
            field=models.CharField(choices=[(b'transfer', b'Transferencia'), (b'metal', 'Met\xe1lico')], default='transfer', max_length=10),
        ),
        migrations.AddField(
            model_name='offer',
            name='refused_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[(b'accepted', b'Aceptada'), (b'refused', b'Rechazada'), (b'canceled', b'Cancelada'), (b'pending', b'Pendiente')], default='pending', max_length=10),
        ),
    ]
