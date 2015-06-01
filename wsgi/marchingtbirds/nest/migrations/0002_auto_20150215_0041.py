# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jacket',
            name='size',
        ),
        migrations.AddField(
            model_name='jacket',
            name='chest',
            field=models.CharField(default='M', help_text=b'Chest measurement', max_length=5, choices=[(b'S', b'S'), (b'M', b'R'), (b'L', b'L'), (b'XL', b'XL'), (b'PLR', b'PLR')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jacket',
            name='shoulder',
            field=models.SmallIntegerField(default=34, help_text=b'Deltoid measurement', choices=[(34, 34), (36, 36)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hat',
            name='size',
            field=models.CharField(max_length=5, choices=[(b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL')]),
            preserve_default=True,
        ),
    ]
