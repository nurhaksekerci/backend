from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Tek bir router kullanarak düzenleyelim
router = DefaultRouter()

# Vehicle Types
router.register(r'vehicle-types', views.VehicleTypeViewSet, basename='vehicle-type')
router.register(r'cities', views.CityViewSet, basename='city')
router.register(r'buyer-companies', views.BuyerCompanyViewSet, basename='buyer-company')

# Tours & Transfers
router.register(r'tours', views.TourViewSet, basename='tour')
router.register(r'no-vehicle-tours', views.NoVehicleTourViewSet, basename='no-vehicle-tour')
router.register(r'transfers', views.TransferViewSet, basename='transfer')

# Hotels
router.register(r'hotels', views.HotelViewSet, basename='hotel')

# Activities
router.register(r'museums', views.MuseumViewSet, basename='museum')
router.register(r'activities', views.ActivityViewSet, basename='activity')

# HR
router.register(r'guides', views.GuideViewSet, basename='guide')

# Suppliers
router.register(r'vehicle-suppliers', views.VehicleSupplierViewSet, basename='vehicle-supplier')
router.register(r'activity-suppliers', views.ActivitySupplierViewSet, basename='activity-supplier')

# Costs
router.register(r'vehicle-costs', views.VehicleCostViewSet, basename='vehicle-cost')
router.register(r'activity-costs', views.ActivityCostViewSet, basename='activity-cost')

<<<<<<< HEAD
=======
# Price Histories
router.register(r'activity-costs-history', views.ActivityCostHistoryViewSet, basename='activity-cost-history')
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33
router.register(r'hotel-price-history', views.HotelPriceHistoryViewSet, basename='hotel-price-history')
router.register(r'museum-price-history', views.MuseumPriceHistoryViewSet, basename='museum-price-history')
router.register(r'vehicle-cost-history', views.VehicleCostHistoryViewSet, basename='vehicle-cost-history')
router.register(r'activity-cost-history', views.ActivityCostHistoryViewSet, basename='activity-cost-history')

urlpatterns = [
    path('', include(router.urls)),
]