from django.contrib import admin
from django.contrib.auth.models import Group

from app.models import Member, User, People, Contact, Event
# from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.


# admin.site.register(Event)
admin.site.register(Member)


# admin.site.register(Founders)
# admin.site.register(People)
# admin.site.register(Contact)

# admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_superuser')

    search_fields = ('email',)

    list_filter = ('date_joined',)
    date_hierarchy = 'date_joined'


@admin.register(Event)
class EventModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'description', 'location', 'price']
    list_filter = ['title', 'created_at', 'price']
    search_fields = ['title', 'location']


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'updated_at']
    search_fields = ['email']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'message']
    search_fields = ['email', 'full_name']
    list_filter = ['created_at']

# @admin.register(Group)