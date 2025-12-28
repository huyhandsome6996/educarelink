from django.contrib import admin
from .models import CarePartner, Booking


admin.site.register(Booking)

@admin.register(CarePartner)
class CarePartnerAdmin(admin.ModelAdmin):
    list_display = ('ho_ten', 'trang_thai', 'ngay_gui')
    list_filter = ('trang_thai',)
    search_fields = ('ho_ten', 'so_cccd')
