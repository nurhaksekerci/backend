from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'operations', views.OperationViewSet)
router.register(r'operation-customers', views.OperationCustomerViewSet)
router.register(r'operation-sales-prices', views.OperationSalesPriceViewSet)
router.register(r'operation-days', views.OperationDayViewSet)
router.register(r'operation-items', views.OperationItemViewSet)
router.register(r'operation-subitems', views.OperationSubItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]