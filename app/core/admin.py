from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from django.utils.translation import gettext as _

from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class InlineCompetition(admin.TabularInline):
    model = models.Competition
    extra = 3


@admin.register(models.Swimmer)
class SwimmerAdmin(admin.ModelAdmin):
    inlines = [InlineCompetition]
    ordering = ['id']
    list_display = (
        'thumbnail',
        'user', 'age', 'city_of_birth', 'fathers_name', 'mothers_name',
        'country', 'city', 'state', 'max_heart_rate', 'rest_heart_rate',
        'height_in_cm', 'weight_in_pound', 'distance', 'stroke_rate',
        'main_stroke', 'school', 'phone_no')
    list_filter = ('city', 'state')
    search_fields = ['city', 'school', 'fathers_name']
    list_display_links = ['user']


@admin.register(models.Game)
class GamesAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'start_date', 'end_date',
    )


admin.site.site_header = 'Swim App'
admin.site.site_title = 'Swim App'
admin.site.unregister(Group)
admin.site.unregister(Token)
