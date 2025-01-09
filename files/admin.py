from django.contrib import admin
from .models import (
    VehicleType, City, BuyerCompany, Tour, NoVehicleTour, Transfer,
    Hotel, Museum, Activity, Guide, VehicleSupplier, ActivitySupplier,
    VehicleCost, ActivityCost, HotelPriceHistory, MuseumPriceHistory,
    VehicleCostHistory, ActivityCostHistory
)

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(BuyerCompany)
class BuyerCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'contact', 'company', 'is_active')
    search_fields = ('name', 'short_name', 'contact')
    list_filter = ('company', 'is_active')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_city', 'end_city', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'start_city', 'end_city', 'is_active')

@admin.register(NoVehicleTour)
class NoVehicleTourAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'city', 'is_active')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_city', 'end_city', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'start_city', 'end_city', 'is_active')

class HotelPriceHistoryInline(admin.TabularInline):
    model = HotelPriceHistory
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'single_price', 'double_price', 'triple_price', 'currency', 'valid_until', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'city', 'currency', 'is_active')
    inlines = [HotelPriceHistoryInline]

class MuseumPriceHistoryInline(admin.TabularInline):
    model = MuseumPriceHistory
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Museum)
class MuseumAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'local_price', 'foreign_price', 'currency', 'valid_until', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'city', 'currency', 'is_active')
    inlines = [MuseumPriceHistoryInline]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'cities', 'is_active')
    filter_horizontal = ('cities',)

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'document_no', 'company', 'is_active')
    search_fields = ('name', 'phone', 'document_no')
    list_filter = ('company', 'cities', 'is_active')
    filter_horizontal = ('cities',)

@admin.register(VehicleSupplier)
class VehicleSupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'cities', 'is_active')
    filter_horizontal = ('cities',)

@admin.register(ActivitySupplier)
class ActivitySupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')
    search_fields = ('name',)
    list_filter = ('company', 'cities', 'is_active')
    filter_horizontal = ('cities',)

class VehicleCostHistoryInline(admin.TabularInline):
    model = VehicleCostHistory
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(VehicleCost)
class VehicleCostAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'tour', 'transfer', 'car_cost', 'minivan_cost', 'minibus_cost', 'midibus_cost', 'bus_cost', 'currency', 'valid_until', 'company', 'is_active')
    search_fields = ('supplier__name', 'tour__name', 'transfer__name')
    list_filter = ('company', 'supplier', 'currency', 'is_active')
    inlines = [VehicleCostHistoryInline]

class ActivityCostHistoryInline(admin.TabularInline):
    model = ActivityCostHistory
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(ActivityCost)
class ActivityCostAdmin(admin.ModelAdmin):
    list_display = ('activity', 'supplier', 'price', 'currency', 'valid_until', 'company', 'is_active')
    search_fields = ('activity__name', 'supplier__name')
    list_filter = ('company', 'activity', 'supplier', 'currency', 'is_active')
    inlines = [ActivityCostHistoryInline]

# Fiyat geçmişi için ayrı admin sınıfları
@admin.register(HotelPriceHistory)
class HotelPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'single_price', 'double_price', 'triple_price', 'currency', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('hotel__company', 'currency', 'is_active')
    search_fields = ('hotel__name',)
    readonly_fields = ('created_at',)

@admin.register(MuseumPriceHistory)
class MuseumPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('museum', 'local_price', 'foreign_price', 'currency', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('museum__company', 'currency', 'is_active')
    search_fields = ('museum__name',)
    readonly_fields = ('created_at',)

@admin.register(VehicleCostHistory)
class VehicleCostHistoryAdmin(admin.ModelAdmin):
    list_display = ('vehicle_cost', 'car_cost', 'minivan_cost', 'minibus_cost', 'midibus_cost', 'bus_cost', 'currency', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('vehicle_cost__company', 'currency', 'is_active')
    search_fields = ('vehicle_cost__supplier__name',)
    readonly_fields = ('created_at',)

@admin.register(ActivityCostHistory)
class ActivityCostHistoryAdmin(admin.ModelAdmin):
    list_display = ('activity_cost', 'price', 'currency', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('activity_cost__company', 'currency', 'is_active')
    search_fields = ('activity_cost__activity__name',)
    readonly_fields = ('created_at',)
