from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'vehicle-types', views.VehicleTypeViewSet, basename='vehicle-type')
router.register(r'cities', views.CityViewSet, basename='city')
router.register(r'buyer-companies', views.BuyerCompanyViewSet, basename='buyer-company')
router.register(r'tours', views.TourViewSet, basename='tour')
router.register(r'no-vehicle-tours', views.NoVehicleTourViewSet, basename='no-vehicle-tour')
router.register(r'transfers', views.TransferViewSet, basename='transfer')
router.register(r'hotels', views.HotelViewSet, basename='hotel')
router.register(r'museums', views.MuseumViewSet, basename='museum')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'guides', views.GuideViewSet, basename='guide')
router.register(r'vehicle-suppliers', views.VehicleSupplierViewSet, basename='vehicle-supplier')
router.register(r'activity-suppliers', views.ActivitySupplierViewSet, basename='activity-supplier')
router.register(r'vehicle-costs', views.VehicleCostViewSet, basename='vehicle-cost')
router.register(r'activity-costs', views.ActivityCostViewSet, basename='activity-cost')

urlpatterns = [
    path('', include(router.urls)),
] 