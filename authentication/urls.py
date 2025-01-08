from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'branches', views.BranchViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'certificates', views.CertificateViewSet)
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'languages', views.LanguageViewSet)
router.register(r'user-languages', views.UserLanguageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 