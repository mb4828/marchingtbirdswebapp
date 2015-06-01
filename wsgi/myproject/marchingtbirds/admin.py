from django.db import models
from django.contrib import admin
from suit.widgets import SuitSplitDateTimeWidget
from marchingtbirds.models import NewsPost, StaffMember, HistoryRecord, CurrentFieldShow, CoverPhoto


class PostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pub_date')
    ordering = ('-pub_date',)
    actions = ('delete_selected',)
    formfield_overrides = {
        models.DateTimeField: {'widget': SuitSplitDateTimeWidget},
    }


class StaffAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'last_update', 'order')
    ordering = ('order',)
    actions = ('delete_selected',)

    fieldsets = [
        ('Personal information', {'fields': ['name', 'title', 'email', 'bio']}),
        ('Sort order', {'fields': ['order']}),
    ]


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    ordering = ('-year',)
    actions = ('delete_selected',)


class ShowAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    ordering = ('-year',)
    actions = ('delete_selected',)

    fieldsets = [
        ('Visibility', {'fields': ['display', ]}),
        ('Basic information', {'fields': ['year', 'title', 'display_title', 'tag']}),
        ('Image', {'fields': ['image', 'image_width', ]}),
        ('Additional information', {'fields': ['links', 'description', ]}),
    ]


class CoverAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'last_update',)
    ordering = ('-last_update',)
    actions = ('delete_selected',)


admin.site.register(NewsPost, PostAdmin)
admin.site.register(StaffMember, StaffAdmin)
admin.site.register(HistoryRecord, HistoryAdmin)
admin.site.register(CurrentFieldShow, ShowAdmin)
admin.site.register(CoverPhoto, CoverAdmin)

