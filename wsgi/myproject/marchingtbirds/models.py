import datetime, string, codecs
from django import forms
from django.utils import timezone
from django.db import models
from tinymce import models as tinymce_models


class NewsPost(models.Model):
    title = models.CharField('Post title', max_length=50)
    content = tinymce_models.HTMLField('Content')
    pub_date = models.DateTimeField('Date published', default=timezone.now)

    def __unicode__(self):
        return self.title

    def getUrl(self):
        new_title = ""

        for c in self.title:
            if not c in string.punctuation:
                new_title += c

        new_title = new_title.replace(' ','-').lower()

        new_date = self.pub_date.strftime('%y%U%w%H%M')
        return new_title + '-' + new_date

class StaffMember(models.Model):
    name = models.CharField('Full name', max_length=30)
    title = models.CharField('Title', max_length=30)
    email = models.EmailField('E-mail address', max_length=254, blank=True)
    bio = tinymce_models.HTMLField('Optional bio', blank=True)

    order = models.SmallIntegerField('Order', help_text="This will determine what order the staff members appear on the page")
    last_update = models.DateTimeField('Last modified', auto_now=True, editable=False)

    def __unicode__(self):
        return self.name

    def obsfucate(self):
        return codecs.encode(self.email, "rot-13")

class HistoryRecord(models.Model):
    year = models.PositiveIntegerField('Year')
    title = models.CharField('Show title', max_length=50)
    description = tinymce_models.HTMLField('Show description', blank=True)

    def __unicode__(self):
        return str(self.year) + ': ' + self.title

class CurrentFieldShow(models.Model):
    display = models.BooleanField('Do you want this show to be visible on the site?', default=True)

    year = models.PositiveIntegerField('Season')
    title = models.CharField('Title', max_length=50)
    display_title = models.BooleanField('Do you want the title to be visible?', help_text='Useful if your title image contains the show title', default=True)
    tag = models.TextField('Tag', max_length=100, help_text="A one sentence summary of the theme, to be displayed below the show title")

    image = models.URLField('Image URL (optional)', blank=True, help_text="URL of an image you would like to use for the show. Store on your hosting solution of choice (e.g. Dropbox, Google Drive, etc.)")
    image_width = models.PositiveIntegerField('Image width', blank=True, null=True, help_text='Width of the image in pixels. Use a value from 1 to 900. The image will not display if this field is blank!')

    links = tinymce_models.HTMLField('Music links (optional)', help_text="Store music files on your hosting solutio of choice (e.g. Dropbox, Google Drive) and link to that file", blank=True)
    description = tinymce_models.HTMLField('Additional info (optional)', blank=True)

    def __unicode__(self):
        return str(self.year) + ': ' + self.title

class CoverPhoto(models.Model):
    name = models.CharField('Image name', max_length=50)
    image = models.URLField('Image URL', help_text='Images will be scaled to the entire width of the page, so crop accordingly. Store on your hosting solution of choice (e.g. Dropbox, Google Drive, etc.)')
    caption = models.CharField('Caption', max_length=150, help_text='A caption to appear under the image', blank=True)
    display = models.BooleanField('Display on site?', default=True)
    last_update = models.DateTimeField('Last modified', auto_now=True, editable=False)

    def __unicode__(self):
        return self.name