from django.contrib import admin
from .models import participant, reservation
from django.utils import timezone
from django.db.models import Count

class ReservationInline(admin.TabularInline):
    model = reservation
    extra = 1
    readonly_fields = ('reservation_date',)
    can_delete = True

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'cin', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('participant_category', 'is_active', 'created_at')
    ordering = ('created_at',)
    inlines = [ReservationInline]

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('participant', 'conference', 'reservation_date', 'confirmed')
    search_fields = ('participant__username', 'conference__title')
    list_filter = ('confirmed', 'reservation_date')
    ordering = ('reservation_date',)

    actions = ['mark_confirmed', 'mark_not_confirmed']

    def mark_confirmed(self, request, queryset):
        queryset.update(confirmed=True)
    mark_confirmed.short_description = "Mark selected reservations as confirmed"

    def mark_not_confirmed(self, request, queryset):
        queryset.update(confirmed=False)
    mark_not_confirmed.short_description = "Mark selected reservations as not confirmed"

admin.site.register(participant, ParticipantAdmin)
admin.site.register(reservation, ReservationAdmin)