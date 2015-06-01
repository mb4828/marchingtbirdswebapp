# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0005_auto_20150215_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='pants',
            name='outseam',
            field=models.FloatField(default=38, help_text=b'Outseam measurement', choices=[(38, b'38'), (38.5, b'38.5'), (39, b'39'), (39.5, b'39.5'), (40, b'40'), (40.5, b'40.5'), (41, b'41'), (41.5, b'41.5'), (42, b'42'), (42.5, b'42.5'), (43, b'43'), (43.5, b'43.5'), (44, b'44')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pants',
            name='rear',
            field=models.SmallIntegerField(default=36, help_text=b'Rear measurement', choices=[(36, b'36'), (38, b'38'), (40, b'40'), (42, b'42'), (44, b'44'), (46, b'46'), (48, b'48'), (50, b'50'), (52, b'52'), (54, b'54'), (56, b'56')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pants',
            name='waist',
            field=models.SmallIntegerField(default=26, help_text=b'Waist measurement', choices=[(26, b'26'), (28, b'28'), (30, b'30'), (32, b'32'), (34, b'34'), (36, b'36'), (38, b'38'), (40, b'40'), (42, b'42'), (44, b'44'), (46, b'46')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jacket',
            name='chest',
            field=models.CharField(help_text=b'Chest measurement', max_length=5, choices=[(b'S', b'S'), (b'R', b'R'), (b'L', b'L'), (b'XL', b'XL'), (b'PLR', b'PLR')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pants',
            name='size',
            field=models.CharField(max_length=12, null=True, editable=False),
            preserve_default=True,
        ),
    ]
