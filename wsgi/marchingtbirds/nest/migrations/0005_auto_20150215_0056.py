# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0004_auto_20150215_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='jacket',
            name='chest',
            field=models.CharField(default='L', help_text=b'Chest measurement', max_length=5, choices=[(b'S', b'S'), (b'M', b'R'), (b'L', b'L'), (b'XL', b'XL'), (b'PLR', b'PLR')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jacket',
            name='shoulder',
            field=models.SmallIntegerField(default=34, help_text=b'Deltoid measurement', choices=[(34, b'34'), (36, b'36'), (38, b'38'), (40, b'40'), (42, b'42'), (44, b'44'), (46, b'46'), (48, b'48'), (50, b'50'), (52, b'52'), (54, b'54')]),
            preserve_default=False,
        ),
    ]
