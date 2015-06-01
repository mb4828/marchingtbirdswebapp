import csv, datetime, re
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib import admin, messages
from django.contrib.admin.utils import label_for_field
from django.utils.translation import ugettext_lazy as _
from nest.models import Jacket, Pants, Hat, Raincoat, Uniform, Student, AuthenticationCode, Bulletin

# HELPER FUNCTIONS

# disable site wide delete action
admin.site.disable_action('delete_selected')

#def is_staff(user):
#    if user:
#        return user.groups.filter(name='Student').exists()
#    return False

def export_as_csv(modeladmin, request, queryset, filename, field_names, header=True):
    """
    Generic csv export admin action.
    based on http://djangosnippets.org/snippets/1697/ and /2020/
    """
    if not request.user.is_staff:
        raise PermissionDenied
    #opts = self.model._meta
    if 'action_checkbox' in field_names:
        field_names.remove('action_checkbox')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    writer = csv.writer(response)
    if header:
        headers = []
        for field_name in list(field_names):
            label = str(label_for_field(field_name, modeladmin.model, modeladmin))
            if str.islower(label):
                label = str.title(label)
            headers.append(label)
        writer.writerow(headers)
    for row in queryset:
        values = []
        for field in field_names:
            try:
                # normal field
                value = (getattr(row, field))
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(unicode(value).encode('utf-8'))
            except:
                # field is a function - only occurs in garment admin
                value = modeladmin.get_assigned_name(row)
                values.append(unicode(value).encode('utf-8'))
        writer.writerow(values)
    return response

# HELPER CLASSES

class GarmentInline(admin.StackedInline):
    model = Uniform
    fields = ('first_name', 'last_name', 'class_year',)
    readonly_fields = ('first_name', 'last_name', 'class_year',)

class SectionListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Section')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('woodwinds', _('Woodwinds')),
            ('brass', _('Brass')),
            ('percussion', _('Percussion')),
            ('guard', _('Color Guard'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value() == 'woodwinds':
            return queryset.filter(instrument__in=Student.WOODWINDS)

        if self.value() == 'brass':
            return queryset.filter(instrument__in=Student.BRASS)

        if self.value() == 'percussion':
            return queryset.filter(instrument__in=Student.PERCUSSION)

        if self.value() == 'guard':
            return queryset.filter(instrument=Student.GUARD)

# MODEL ADMINS

class GarmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'size', 'condition', 'get_assigned_url')
    ordering = ('name',)
    actions = ('export_garment', 'delete_selected',)
    list_filter = ('type', 'size', 'condition')
    inlines = [GarmentInline,]

    def get_assigned_url(self, obj):
        url = reverse('admin:nest_uniform_change', args=(obj.uniform.pk,))
        name = Uniform.objects.get(pk=obj.uniform.pk).__str__()
        return '<a href="%s">%s</a>' % (url, name)
    get_assigned_url.allow_tags = True
    get_assigned_url.short_description = 'Assigned to'

    def get_assigned_name(self, obj):
        try:
            name = Uniform.objects.get(pk=obj.uniform.pk).__str__()
            return name
        except:
            return ''
    get_assigned_name.short_description = 'Assigned to'

    def export_garment(self, request, queryset):
        modelname = self.model._meta.verbose_name_plural.title().lower()
        field_names = ('name', 'type', 'size', 'condition', 'get_assigned_name', 'notes',)
        return export_as_csv(self, request, queryset, '%s.csv' % modelname, field_names)
    export_garment.short_description = 'Download data spreadsheet'

class UniformAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'class_year', 'tshirt', 'jacket_link', 'pants_link', 'hat_link', 'raincoat_link', 'returned',)
    ordering = ('last_name',)
    list_filter = ('class_year', SectionListFilter, 'instrument',)
    actions = ('export_uniform', 'set_returned', 'clear_returned', 'clear_uniform',)

    readonly_fields = ('first_name', 'last_name', 'class_year', 'instrument', 'tshirt')
    fieldsets = [
        ('Student information', {'fields': ['first_name', 'last_name', 'class_year', 'instrument', 'tshirt']}),
        ('Uniform assignment', {'fields': ['jacket', 'pants', 'hat', 'raincoat',]}),
        ('Uniform return', {'fields': ['returned', ]}),
    ]

    def jacket_link(self, obj):
        if not obj.jacket:
            return '(None)'
        url = reverse('admin:nest_jacket_change', args=(obj.jacket.pk,))
        name = Jacket.objects.get(pk=obj.jacket.pk).name
        size = Jacket.objects.get(pk=obj.jacket.pk).size
        return '<a href="%s">%s</a> (%s)' % (url, name, size)
    jacket_link.allow_tags = True
    jacket_link.short_description = 'Jacket'

    def pants_link(self, obj):
        if not obj.pants:
            return '(None)'
        url = reverse('admin:nest_pants_change', args=(obj.pants.pk,))
        name = Pants.objects.get(pk=obj.pants.pk).name
        size = Pants.objects.get(pk=obj.pants.pk).size
        return '<a href="%s">%s</a> (%s)' % (url, name, size)
    pants_link.allow_tags = True
    pants_link.short_description = 'Pants'

    def hat_link(self, obj):
        if not obj.hat:
            return '(None)'
        url = reverse('admin:nest_hat_change', args=(obj.hat.pk,))
        name = Hat.objects.get(pk=obj.hat.pk).name
        size = Hat.objects.get(pk=obj.hat.pk).size
        return '<a href="%s">%s</a> (%s)' % (url, name, size)
    hat_link.allow_tags = True
    hat_link.short_description = 'Hat'

    def raincoat_link(self, obj):
        if not obj.raincoat:
            return '(None)'
        url = reverse('admin:nest_raincoat_change', args=(obj.raincoat.pk,))
        name = Raincoat.objects.get(pk=obj.raincoat.pk).name
        size = Raincoat.objects.get(pk=obj.raincoat.pk).size
        return '<a href="%s">%s</a> (%s)' % (url, name, size)
    raincoat_link.allow_tags = True
    raincoat_link.short_description = 'Raincoat'

    def clear_uniform(self, request, queryset):
        if not self.has_change_permission(request, obj=None):
            self.message_user(request, "You do not have permission to modify uniform assignments!", level=messages.ERROR,)
            return

        rows_updated = queryset.update(jacket=None, pants=None, hat=None, raincoat=None, returned=False,)

        if rows_updated == 1:
            message_bit = "1 uniform assignment was"
        else:
            message_bit = "%s uniform assignments were" % rows_updated
        self.message_user(request, "%s successfully cleared." % message_bit, level=messages.SUCCESS,)
    clear_uniform.short_description = 'Clear uniform assignment'

    def clear_returned(self, request, queryset):
        if not self.has_change_permission(request, obj=None):
            self.message_user(request, "You do not have permission to modify uniform assignments!", level=messages.ERROR,)
            return

        rows_updated = queryset.update(returned=False,)

        if rows_updated == 1:
            message_bit = "1 uniform assignment was"
        else:
            message_bit = "%s uniform assignments were" % rows_updated
        self.message_user(request, "%s set to NOT returned." % message_bit, level=messages.SUCCESS,)
    clear_returned.short_description = 'Mark uniform NOT returned'

    def set_returned(self, request, queryset):
        if not self.has_change_permission(request, obj=None):
            self.message_user(request, "You do not have permission to modify uniform assignments!", level=messages.ERROR,)
            return

        rows_updated = queryset.update(returned=True,)

        if rows_updated == 1:
            message_bit = "1 uniform assignment was"
        else:
            message_bit = "%s uniform assignments were" % rows_updated
        self.message_user(request, "%s set to returned." % message_bit, level=messages.SUCCESS,)
    set_returned.short_description = 'Mark uniform returned'

    def export_uniform(self, request, queryset):
        field_names = ('first_name', 'last_name', 'instrument', 'class_year', 'tshirt', 'jacket', 'pants', 'hat', 'raincoat', 'returned',)
        return export_as_csv(self, request, queryset, 'uniform_data.csv', field_names)
    export_uniform.short_description = 'Download data spreadsheet'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'class_year', 'instrument', )
    ordering = ('last_name',)
    list_filter = ('class_year', SectionListFilter, 'instrument',)
    actions = ('export_student', 'export_mailing_list', 'clear_student', 'delete_student', )

    readonly_fields = ('class_year',)
    fieldsets = [
        ('Student information', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['first_name', 'last_name', 'grad_year', 'class_year', 'instrument',]
        }),
        ('T-shirt', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['tshirt',]
        }),
        ('Street Address', {
            'classes': ('suit-tab', 'suit-tab-contact',),
            'fields': ['street_address',]
        }),
        ('E-mail addresses', {
            'classes': ('suit-tab', 'suit-tab-contact',),
            'fields': ['student_email', 'parent_email1', 'parent_email2',]
        }),
        ('Phone numbers', {
            'classes': ('suit-tab', 'suit-tab-contact',),
            'fields': ['home_phone', 'parent_cell1', 'parent_cell2',]
        }),
        ('Emergency contact', {
            'classes': ('suit-tab', 'suit-tab-emergency',),
            'fields': ['emergency_contact', 'emergency_relationship', 'emergency_phone',]
        }),
    ]

    suit_form_tabs = (('general', 'General Information'), ('contact', 'Contact Information'), ('emergency', 'Emergency Contact'))

    def export_mailing_list(self, request, queryset):
        cdate = str(datetime.date.today())
        query = str(request.META['QUERY_STRING']).replace('__exact','').replace('&',', ').replace('+',' ').replace('_',' ').upper()
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=mtb_mailing_list_%s.txt' % cdate

        # get students, parent, and section emails
        student_emails = []
        parent_emails = []

        for row in queryset:
            s1 = unicode(getattr(row, 'student_email')).encode('utf-8')
            p1 = unicode(getattr(row, 'parent_email1')).encode('utf-8')
            p2 = unicode(getattr(row, 'parent_email2')).encode('utf-8')

            student_emails.append(s1)
            if p1:
                parent_emails.append(p1)
            if p2:
                parent_emails.append(p2)

        # put it all together!
        data = 'MAHWAH MARCHING THUNDERBIRDS MAILING LISTS\n' \
               'FILTERS: ' + query + '\n' + \
               'GENERATED ON: ' + cdate

        data += '\n\n\nSTUDENT MAILING LIST:\n\n'

        for i in range(len(student_emails)-1):
            data += student_emails[i] + ', '
        data += student_emails[-1]

        data += '\n\n\nPARENT MAILING LIST:\n\n'

        for i in range(len(parent_emails)-1):
            data += parent_emails[i] + ', '
        data += parent_emails[-1]

        data += '\n\n\nCOMBINED STUDENT & PARENT MAILING LIST:\n\n'

        for i in range(len(student_emails)):        # it's inefficient - get over it!
            data += student_emails[i] + ', '

        for i in range(len(parent_emails)-1):
            data += parent_emails[i] + ', '
        data += parent_emails[-1]

        data += '\n'

        response.write(data)
        return response
    export_mailing_list.short_description = 'Download mailing list'

    def clear_student(self, request, queryset):
        if not self.has_change_permission(request, obj=None):
            self.message_user(request, "You do not have permission to modify students!", level=messages.ERROR,)
            return

        rows_updated = queryset.update(street_address='',
                                       parent_email1='',
                                       parent_email2='',
                                       home_phone='',
                                       parent_cell1='',
                                       parent_cell2='',
                                       emergency_contact='',
                                       emergency_relationship='',
                                       emergency_phone='',)

        if rows_updated == 1:
            message_bit = "1 student profile was"
        else:
            message_bit = "%s student profiles were" % rows_updated
        self.message_user(request, "%s successfully cleared." % message_bit, level=messages.SUCCESS,)
    clear_student.short_description = 'Clear profile (will not delete student information or uniform assignment)'

    def delete_student(self, request, queryset):
        if not self.has_delete_permission(request, obj=None):
            self.message_user(request, "You do not have permission to delete students!", level=messages.ERROR,)
            return

        rows_updated = 0
        for obj in queryset:
            obj.delete()
            rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 student was"
        else:
            message_bit = "%s student were" % rows_updated
        self.message_user(request, "%s successfully deleted and their account(s) deactivated. If this was a mistake, you can reactivate accounts under User Management" % message_bit, level=messages.SUCCESS,)
    delete_student.short_description = 'Delete student (should be used only for graduating seniors, will deactivate the student\'s account)'

    def export_student(self, request, queryset):
        field_names = ('first_name', 'last_name', 'instrument', 'class_year', 'street_address', 'home_phone', 'parent_cell1', 'parent_cell2', 'emergency_contact', 'emergency_relationship', 'emergency_phone', 'student_email', 'parent_email1', 'parent_email2',)
        return export_as_csv(self, request, queryset, 'student_data.csv', field_names)
    export_student.short_description = 'Download data spreadsheet'

class AuthcodeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_update',)

class BulletinAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'last_update',)
    actions = ('delete_selected',)

admin.site.register(Jacket, GarmentAdmin)
admin.site.register(Pants, GarmentAdmin)
admin.site.register(Hat, GarmentAdmin)
admin.site.register(Raincoat, GarmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Uniform, UniformAdmin)
admin.site.register(AuthenticationCode, AuthcodeAdmin)
admin.site.register(Bulletin, BulletinAdmin)