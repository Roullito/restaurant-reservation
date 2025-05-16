from django.contrib import admin
from .models import Client, Reservation, ServiceSettings
from .forms import ReservationAdminForm


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')  # Colonnes visibles
    search_fields = ('first_name', 'last_name', 'email')          # Barre de recherche
    list_filter = ('last_name',)                                  # Filtres latéraux

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    list_display = ('client', 'reservation_date', 'reservation_time', 'number_of_people')

admin.site.site_header = "ResaPro - Interface d'administration"
admin.site.site_title = "ResaPro Admin"
admin.site.index_title = "Tableau de bord des réservations"
admin.site.register(ServiceSettings)
