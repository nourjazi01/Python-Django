from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import conference
from users.models import *
from django.db.models import Count

class reservationInLine(admin.TabularInline):
    model=reservation
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True

class conferenceDateFilter(admin.SimpleListFilter):
    title='date conf filter'
    parameter_name='conference_date'
    def lookups(self,request,model_admin):
        return(
            ('past','past conf'),
            ('today','today conf'),
            ('upcoming','upcoming conf'),
        )
    def queryset(self, request, queryset):
        if self.value()=='past':
            return queryset.filter(end_date__lt=timezone.now().date())
        if self.value()=='today':
            return queryset.filter(start_date=timezone.now().date())
        if self.value()=='upcoming':
            return queryset.filter(start_date__gt=timezone.now().date())
        return queryset



class participantFilter(admin.SimpleListFilter):
    title="participant filter"
    parameter_name="participants"
    def lookups(self, request, model_admin):
        return (
            ('0',('no participants')),
            ('more',('more participants'))
        )
    def queryset(self, request, queryset):
        if self.value()=='0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value()=='more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset


class conferenceAdmin(admin.ModelAdmin):
    list_display=('title','location','start_date','end_date','price')
    search_fields=('title',)
    list_per_page=2
    ordering=('start_date','title')
    fieldsets=(
        ('description',{
            'fields':('title','description','category','location','price','capacity')
        }),
        ('horaires',{
            'fields':('start_date','end_date')
        }),
        ('documents',{
            'fields':('program',)
        })
    )
    inlines=[reservationInLine]
    autocomplete_fields=['category']
    list_filter=('title',participantFilter,conferenceDateFilter)


admin.site.register(conference,conferenceAdmin)




class ReservationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'conference', 'reservation_date')
    actions = ['mark_confirmed', 'mark_not_confirmed']

    def mark_confirmed(self, request, queryset):
        queryset.update(confirmed=True)
    mark_confirmed.short_description = "Mark selected reservations as confirmed"

    def mark_not_confirmed(self, request, queryset):
        queryset.update(confirmed=False)
    mark_not_confirmed.short_description = "Mark selected reservations as not confirmed"