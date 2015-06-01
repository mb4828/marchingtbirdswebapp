# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'This code will be used to verify that new users are actual band members when they register for the site.<br/>If you change the code, make sure to distribute it to band members before they register!', max_length=40)),
                ('enable', models.BooleanField(default=True, help_text=b'Check this box to enable new user registration', verbose_name=b'Enabled')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Authentication & Registration',
                'verbose_name_plural': 'Authentication & Registration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', tinymce.models.HTMLField()),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name=b'ID')),
                ('type', models.CharField(default=b'Band', max_length=15, choices=[(b'Drum Major', b'Drum Major'), (b'Band', b'Band'), (b'Guard', b'Guard'), (b'Percussion', b'Drums'), (b'Other', b'Other')])),
                ('size', models.CharField(max_length=5, choices=[(b'XS', b'XS'), (b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'2XL', b'2XL')])),
                ('condition', models.CharField(default=b'Good', max_length=10, choices=[(b'Good', b'Good'), (b'Fair', b'Fair'), (b'Poor', b'Poor'), (b'Missing', b'Missing')])),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jacket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name=b'ID')),
                ('type', models.CharField(default=b'Band', max_length=15, choices=[(b'Drum Major', b'Drum Major'), (b'Band', b'Band'), (b'Guard', b'Guard'), (b'Percussion', b'Drums'), (b'Other', b'Other')])),
                ('size', models.CharField(max_length=5, choices=[(b'XS', b'XS'), (b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'2XL', b'2XL')])),
                ('condition', models.CharField(default=b'Good', max_length=10, choices=[(b'Good', b'Good'), (b'Fair', b'Fair'), (b'Poor', b'Poor'), (b'Missing', b'Missing')])),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pants',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name=b'ID')),
                ('type', models.CharField(default=b'Band', max_length=15, choices=[(b'Drum Major', b'Drum Major'), (b'Band', b'Band'), (b'Guard', b'Guard'), (b'Percussion', b'Drums'), (b'Other', b'Other')])),
                ('size', models.CharField(max_length=5, choices=[(b'XS', b'XS'), (b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'2XL', b'2XL')])),
                ('condition', models.CharField(default=b'Good', max_length=10, choices=[(b'Good', b'Good'), (b'Fair', b'Fair'), (b'Poor', b'Poor'), (b'Missing', b'Missing')])),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'pants',
                'verbose_name_plural': 'pants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raincoat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name=b'ID')),
                ('type', models.CharField(default=b'Band', max_length=15, choices=[(b'Drum Major', b'Drum Major'), (b'Band', b'Band'), (b'Guard', b'Guard'), (b'Percussion', b'Drums'), (b'Other', b'Other')])),
                ('size', models.CharField(max_length=5, choices=[(b'XS', b'XS'), (b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'2XL', b'2XL')])),
                ('condition', models.CharField(default=b'Good', max_length=10, choices=[(b'Good', b'Good'), (b'Fair', b'Fair'), (b'Poor', b'Poor'), (b'Missing', b'Missing')])),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, blank=True)),
                ('grad_year', models.SmallIntegerField(null=True, verbose_name=b'Graduation year', blank=True)),
                ('class_year', models.CharField(verbose_name=b'Grade', max_length=10, null=True, editable=False)),
                ('instrument', models.CharField(blank=True, max_length=20, null=True, choices=[(b'Flute', b'Flute/Piccolo'), (b'Clarinet', b'Clarinet'), (b'Bass clarinet', b'Bass clarinet'), (b'Alto sax', b'Alto sax'), (b'Tenor sax', b'Tenor sax'), (b'Bari sax', b'Bari sax'), (b'Trumpet', b'Trumpet'), (b'Mellophone', b'Mellophone (French horn)'), (b'Trombone', b'Trombone'), (b'Baritone', b'Baritone'), (b'Tuba', b'Tuba'), (b'Color guard', b'Color guard'), (b'Drumline', b'Drumline'), (b'Pit percussion', b'Pit percussion')])),
                ('tshirt', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'T-shirt size', choices=[(b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'2XL', b'2XL')])),
                ('returned', models.BooleanField(default=False, help_text=b'Check if student has returned uniform')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('uniform_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='nest.Uniform')),
                ('student_email', models.EmailField(max_length=75, verbose_name=b"Student's e-mail address", blank=True)),
                ('parent_email1', models.EmailField(max_length=75, verbose_name=b"Parent's e-mail address 1", blank=True)),
                ('parent_email2', models.EmailField(max_length=75, verbose_name=b"Parent's e-mail address 2", blank=True)),
                ('street_address', models.CharField(max_length=60, blank=True)),
                ('home_phone', models.CharField(max_length=15, blank=True)),
                ('parent_cell1', models.CharField(max_length=15, verbose_name=b"Parent's cell phone 1", blank=True)),
                ('parent_cell2', models.CharField(max_length=15, verbose_name=b"Parent's cell phone 2", blank=True)),
                ('emergency_contact', models.CharField(max_length=30, verbose_name=b'Emergency contact name', blank=True)),
                ('emergency_relationship', models.CharField(max_length=30, verbose_name=b'Relationship to student', blank=True)),
                ('emergency_phone', models.CharField(max_length=15, verbose_name=b'Emergency contact phone', blank=True)),
            ],
            options={
            },
            bases=('nest.uniform',),
        ),
        migrations.AddField(
            model_name='uniform',
            name='hat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='nest.Hat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uniform',
            name='jacket',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='nest.Jacket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uniform',
            name='pants',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='nest.Pants'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uniform',
            name='raincoat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='nest.Raincoat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uniform',
            name='user',
            field=models.OneToOneField(null=True, blank=True, editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
