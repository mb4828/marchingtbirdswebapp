# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0002_auto_20150215_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='jacket',
            name='size',
            field=models.CharField(max_length=10, null=True, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jacket',
            name='shoulder',
            field=models.SmallIntegerField(help_text=b'Deltoid measurement', choices=[(34, b'34'), (36, b'36'), (38, b'38'), (40, b'40'), (42, b'42'), (44, b'44'), (46, b'46'), (48, b'48'), (50, b'50'), (52, b'52'), (54, b'54')]),
            preserve_default=True,
        ),
    ]
