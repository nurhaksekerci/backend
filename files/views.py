from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
<<<<<<< HEAD

=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33

class CompanyFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
<<<<<<< HEAD

        # Swagger kontrolü
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()

        # Company filtresi
        if hasattr(self.get_serializer().Meta.model, 'company'):
            return queryset.filter(company=self.request.user.company)
        return queryset

=======
        # Eğer modelde company alanı varsa filtrele
        if hasattr(self.get_serializer().Meta.model, 'company'):
            return queryset.filter(company=self.request.user.company)
        return queryset

>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33
@swagger_auto_schema(tags=['Basic Data'])
class VehicleTypeViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'created_at']

class CityViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['is_active']
    pagination_class = None

class BuyerCompanyViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = BuyerCompany.objects.all()
    serializer_class = BuyerCompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'short_name', 'contact']
    filterset_fields = ['is_active']
    pagination_class = None

@swagger_auto_schema(tags=['Tours & Transfers'])
class TourViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['start_city', 'end_city', 'is_active']
    pagination_class = None

class NoVehicleTourViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = NoVehicleTour.objects.all()
    serializer_class = NoVehicleTourSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'is_active']
    pagination_class = None

class TransferViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['start_city', 'end_city', 'is_active']
    pagination_class = None

@swagger_auto_schema(tags=['Accommodation'])
class HotelViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'currency', 'is_active']
    pagination_class = None

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        hotel = self.get_object()
        history = hotel.price_history.all()
        serializer = HotelPriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class MuseumViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'currency', 'is_active']
    pagination_class = None

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        museum = self.get_object()
        history = museum.price_history.all()
        serializer = MuseumPriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class ActivityViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']
    pagination_class = None

class GuideViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'phone', 'document_no']
    filterset_fields = ['cities', 'is_active']
    pagination_class = None

class VehicleSupplierViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = VehicleSupplier.objects.all()
    serializer_class = VehicleSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']
    pagination_class = None

class ActivitySupplierViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = ActivitySupplier.objects.all()
    serializer_class = ActivitySupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']
    pagination_class = None

class VehicleCostViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = VehicleCost.objects.all()
    serializer_class = VehicleCostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['supplier__name', 'tour__name', 'transfer__name']
    filterset_fields = ['supplier', 'currency', 'is_active']
    pagination_class = None

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        cost = self.get_object()
        history = cost.price_history.all()
        serializer = VehicleCostHistorySerializer(history, many=True)
        return Response(serializer.data)

class ActivityCostViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = ActivityCost.objects.all()
    serializer_class = ActivityCostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['activity__name', 'supplier__name']
    filterset_fields = ['activity', 'supplier', 'currency', 'is_active']
    pagination_class = None

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        cost = self.get_object()
        history = cost.price_history.all()
        serializer = ActivityCostHistorySerializer(history, many=True)
        return Response(serializer.data)

<<<<<<< HEAD

=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33
class ActivityCostHistoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = ActivityCostHistory.objects.all()
    serializer_class = ActivityCostHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_cost', 'currency', 'is_active']
    search_fields = ['activity_cost__activity__name']
    ordering_fields = ['valid_from', 'valid_until', 'created_at']
<<<<<<< HEAD
    pagination_class = None
=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33

# Fiyat geçmişi ViewSet'leri
class HotelPriceHistoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = HotelPriceHistory.objects.all()
    serializer_class = HotelPriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['hotel', 'currency', 'is_active']
    search_fields = ['hotel__name']
    ordering_fields = ['valid_from', 'valid_until', 'created_at']
<<<<<<< HEAD
    pagination_class = None
=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33

class MuseumPriceHistoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = MuseumPriceHistory.objects.all()
    serializer_class = MuseumPriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['museum', 'currency', 'is_active']
    search_fields = ['museum__name']
    ordering_fields = ['valid_from', 'valid_until', 'created_at']
<<<<<<< HEAD
    pagination_class = None
=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33

class VehicleCostHistoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = VehicleCostHistory.objects.all()
    serializer_class = VehicleCostHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vehicle_cost', 'currency', 'is_active']
    search_fields = ['vehicle_cost__supplier__name']
    ordering_fields = ['valid_from', 'valid_until', 'created_at']
<<<<<<< HEAD
    pagination_class = None
=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33

class ActivityCostHistoryViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = ActivityCostHistory.objects.all()
    serializer_class = ActivityCostHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_cost', 'currency', 'is_active']
    search_fields = ['activity_cost__activity__name']
    ordering_fields = ['valid_from', 'valid_until', 'created_at']
<<<<<<< HEAD
    pagination_class = None
=======
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33
