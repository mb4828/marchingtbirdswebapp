# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0003_auto_20150215_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jacket',
            name='chest',
        ),
        migrations.RemoveField(
            model_name='jacket',
            name='shoulder',
        ),
    ]
