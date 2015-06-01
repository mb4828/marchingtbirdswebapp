from datetime import datetime
from django.db import models
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

# uniform conditions
NEW = 'New'
GOOD = 'Good'
FAIR = 'Fair'
POOR = 'Poor'
MISSING = 'Missing'
NOT_AVAILABLE = 'N/A'

# uniform types
DRUM_MAJOR = 'Drum Major'
BAND = 'Band'
GUARD = 'Guard'
PERCUSSION = 'Percussion'
OTHER = 'Other'

# sizes
EXTRA_SMALL = 'XS'
SMALL = 'S'
MEDIUM = 'M'
REGULAR = 'R'
LARGE = 'L'
EXTRA_LARGE = 'XL'
EXTRA_EXTRA = '2XL'
PLR = 'PLR'

# class years
ERROR = 'N/A'
FRESHMAN = '9'
SOPHOMORE = '10'
JUNIOR = '11'
SENIOR = '12'
GRAD = 'Graduated'

# choices fields
CONDITIONS = ((GOOD, 'Good'), (FAIR, 'Fair'), (POOR, 'Poor'), (MISSING, 'Missing'))
TYPES = ((DRUM_MAJOR, 'Drum Major'), (BAND, 'Band'), (GUARD, 'Guard'), (PERCUSSION, 'Drums'), (OTHER, 'Other'))

class Jacket(models.Model):
    JACKET_SIZES = ((SMALL, 'S'), (REGULAR, 'R'), (LARGE, 'L'), (EXTRA_LARGE, 'XL'), (PLR, 'PLR'))
    SHOULDER = ((34,'34'),(36,'36'),(38,'38'),(40,'40'),(42,'42'),(44,'44'),(46,'46'),(48,'48'),(50,'50'),(52,'52'),(54,'54'))

    name = models.CharField('ID', max_length=10)
    type = models.CharField(max_length=15, choices=TYPES, default=BAND)
    shoulder = models.SmallIntegerField(help_text='Deltoid measurement', choices=SHOULDER)
    chest = models.CharField(help_text='Chest measurement', max_length=5, choices=JACKET_SIZES)
    size = models.CharField(max_length=10, editable=False, null=True)
    condition = models.CharField(max_length=10, choices=CONDITIONS, default=GOOD)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.size)

    def getSize(self):
        return str(self.shoulder) + str(self.chest)
        #return 'test'

    def save(self, *args, **kwargs):
        self.size = self.getSize()
        super(Jacket, self).save(*args, **kwargs)

class Pants(models.Model):
    #PANTS_SIZES = ((EXTRA_SMALL, 'XS'), (SMALL, 'S'), (MEDIUM, 'M'), (LARGE, 'L'), (EXTRA_LARGE, 'XL'), (EXTRA_EXTRA, '2XL'))
    WAIST = ((26,'26'),(28,'28'),(30,'30'),(32,'32'),(34,'34'),(36,'36'),(38,'38'),(40,'40'),(42,'42'),(44,'44'),(46,'46'))
    REAR = ((36,'36'),(38,'38'),(40,'40'),(42,'42'),(44,'44'),(46,'46'),(48,'48'),(50,'50'),(52,'52'),(54,'54'),(56,'56'),)
    OUTSEAM = ((38,'38'),(38.5,'38.5'),(39,'39'),(39.5,'39.5'),(40,'40'),(40.5,'40.5'),(41,'41'),(41.5,'41.5'),(42,'42'),(42.5,'42.5'),(43,'43'),(43.5,'43.5'),(44,'44'),)

    name = models.CharField('ID', max_length=10)
    type = models.CharField(max_length=15, choices=TYPES, default=BAND)
    waist = models.SmallIntegerField(help_text='Waist measurement', choices=WAIST)
    rear = models.SmallIntegerField(help_text='Rear measurement', choices=REAR)
    outseam = models.FloatField(help_text='Outseam measurement', choices=OUTSEAM)
    size = models.CharField(max_length=12, editable=False, null=True)
    condition = models.CharField(max_length=10, choices=CONDITIONS, default=GOOD)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.size)

    def getSize(self):
        return str(self.waist) + '/' + str(self.rear) + '/' + str(self.outseam)

    def save(self, *args, **kwargs):
        self.size = self.getSize()
        super(Pants, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'pants'
        verbose_name_plural = 'pants'


class Hat(models.Model):
    HAT_SIZES = ((SMALL, 'S'), (MEDIUM, 'M'), (LARGE, 'L'), (EXTRA_LARGE, 'XL'))

    name = models.CharField('ID', max_length=10)
    type = models.CharField(max_length=15, choices=TYPES, default=BAND)
    size = models.CharField(max_length=5, choices=HAT_SIZES)
    condition = models.CharField(max_length=10, choices=CONDITIONS, default=GOOD)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.size)

class Raincoat(models.Model):
    RAINCOAT_SIZES = ((EXTRA_SMALL, 'XS'), (SMALL, 'S'), (MEDIUM, 'M'), (LARGE, 'L'), (EXTRA_LARGE, 'XL'), (EXTRA_EXTRA, '2XL'))

    name = models.CharField('ID', max_length=10)
    type = models.CharField(max_length=15, choices=TYPES, default=BAND)
    size = models.CharField(max_length=5, choices=RAINCOAT_SIZES)
    condition = models.CharField(max_length=10, choices=CONDITIONS, default=GOOD)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.size)

class Uniform(models.Model):
    # instruments
    FLUTE = 'Flute'
    CLARINET = 'Clarinet'
    BASSCLARI = 'Bass clarinet'
    ASAX = 'Alto sax'
    TSAX = 'Tenor sax'
    BSAX = 'Bari sax'
    TRUMPET = 'Trumpet'
    MELLO = 'Mellophone'
    TROMBONE = 'Trombone'
    BARITONE = 'Baritone'
    TUBA = 'Tuba'
    GUARD = 'Color guard'
    BATTERY = 'Drumline'
    PIT = 'Pit percussion'

    INSTRUMENTS = (
        (FLUTE, 'Flute/Piccolo'), (CLARINET, 'Clarinet'), (BASSCLARI, 'Bass clarinet'), (ASAX, 'Alto sax'),
        (TSAX, 'Tenor sax'), (BSAX, 'Bari sax'), (TRUMPET, 'Trumpet'), (MELLO, 'Mellophone (French horn)'),
        (TROMBONE, 'Trombone'), (BARITONE, 'Baritone'), (TUBA, 'Tuba'), (GUARD, 'Color guard'),
        (BATTERY, 'Drumline'), (PIT, 'Pit percussion')
    )

    WOODWINDS = (FLUTE, CLARINET, BASSCLARI, ASAX, TSAX, BSAX)
    BRASS = (TRUMPET, MELLO, TROMBONE, BARITONE, TUBA)
    PERCUSSION = (BATTERY, PIT)

    TSHIRT_SIZES = ((SMALL, 'S'), (MEDIUM, 'M'), (LARGE, 'L'), (EXTRA_LARGE, 'XL'), (EXTRA_EXTRA, '2XL'))

    # model fields
    user = models.OneToOneField(User, null=True, blank=True, editable=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    grad_year = models.SmallIntegerField('Graduation year', blank=True, null=True)
    class_year = models.CharField('Grade', editable=False, max_length=10, null=True)
    instrument = models.CharField(max_length=20, choices=INSTRUMENTS, blank=True, null=True)
    tshirt = models.CharField('T-shirt size', max_length=5, choices=TSHIRT_SIZES, blank=True, null=True)

    jacket = models.OneToOneField(Jacket, null=True, blank=True, on_delete=models.SET_NULL)
    pants = models.OneToOneField(Pants, null=True, blank=True, on_delete=models.SET_NULL)
    hat = models.OneToOneField(Hat, null=True, blank=True, on_delete=models.SET_NULL)
    raincoat = models.OneToOneField(Raincoat, null=True, blank=True, on_delete=models.SET_NULL)
    returned = models.BooleanField(help_text='Check if student has returned uniform', default=False)

    def classyr(self):
        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month <= 6:
            if not self.grad_year:                      return ERROR
            if current_year > self.grad_year:           return GRAD
            elif current_year == self.grad_year:        return SENIOR
            elif current_year + 1 == self.grad_year:    return JUNIOR
            elif current_year + 2 == self.grad_year:    return SOPHOMORE
            elif current_year + 3 == self.grad_year:    return FRESHMAN
            else:                                       return ERROR
        else:
            if not self.grad_year:                      return ERROR
            if current_year >= self.grad_year:          return GRAD
            elif current_year + 1 == self.grad_year:    return SENIOR
            elif current_year + 2 == self.grad_year:    return JUNIOR
            elif current_year + 3 == self.grad_year:    return SOPHOMORE
            elif current_year + 4 == self.grad_year:    return FRESHMAN
            else:                                       return ERROR

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    def save(self, *args, **kwargs):
        self.class_year = self.classyr()
        super(Uniform, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            usrobj = User.objects.get(pk=self.user.pk)
            usrobj.is_active = False
            usrobj.save()
        super(Uniform, self).delete(*args, **kwargs)

class Student(Uniform):
    student_email = models.EmailField('Student\'s e-mail address', blank=True)
    parent_email1 = models.EmailField('Parent\'s e-mail address 1', blank=True)
    parent_email2 = models.EmailField('Parent\'s e-mail address 2', blank=True)

    street_address = models.CharField(max_length=60, blank=True)
    home_phone = models.CharField(max_length=15, blank=True)
    parent_cell1 = models.CharField('Parent\'s cell phone 1', max_length=15, blank=True)
    parent_cell2 = models.CharField('Parent\'s cell phone 2', max_length=15, blank=True)

    emergency_contact = models.CharField('Emergency contact name', max_length=30, blank=True)
    emergency_relationship = models.CharField('Relationship to student', max_length=30, blank=True)
    emergency_phone = models.CharField('Emergency contact phone', max_length=15, blank=True)

class AuthenticationCode(models.Model):
    code = models.CharField(max_length=40, help_text='This code will be used to verify that new users are actual band members when they register for the site.<br/>If you change the code, make sure to distribute it to band members before they register!')
    enable = models.BooleanField('Enabled', help_text='Check this box to enable new user registration', default=True)
    last_update = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return 'Code: ' + self.code + '; Registration enabled: ' + str(self.enable)

    class Meta:
        verbose_name = 'Authentication & Registration'
        verbose_name_plural = 'Authentication & Registration'

class Bulletin(models.Model):
    message = tinymce_models.HTMLField()
    last_update = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        message = strip_tags(self.message)

        if len(message) > 75:
            message = message[:75].strip()
            return message + '...'
        else:
            return message