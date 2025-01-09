from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action

class CompanyFilterMixin:
    def get_queryset(self):
        # Kullanıcının bağlı olduğu şirkete göre filtreleme
        return super().get_queryset().filter(company=self.request.user.company)

class VehicleTypeViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = VehicleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'created_at']

class CityViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['is_active']

class BuyerCompanyViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = BuyerCompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'short_name', 'contact']
    filterset_fields = ['is_active']

class TourViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['start_city', 'end_city', 'is_active']

class NoVehicleTourViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = NoVehicleTourSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'is_active']

class TransferViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['start_city', 'end_city', 'is_active']

class HotelViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'currency', 'is_active']

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        hotel = self.get_object()
        history = hotel.price_history.all()
        serializer = HotelPriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class MuseumViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = MuseumSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['city', 'currency', 'is_active']

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        museum = self.get_object()
        history = museum.price_history.all()
        serializer = MuseumPriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class ActivityViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']

class GuideViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = GuideSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'phone', 'document_no']
    filterset_fields = ['cities', 'is_active']

class VehicleSupplierViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = VehicleSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']

class ActivitySupplierViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = ActivitySupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['cities', 'is_active']

class VehicleCostViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = VehicleCostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['supplier__name', 'tour__name', 'transfer__name']
    filterset_fields = ['supplier', 'currency', 'is_active']

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        cost = self.get_object()
        history = cost.price_history.all()
        serializer = VehicleCostHistorySerializer(history, many=True)
        return Response(serializer.data)

class ActivityCostViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    serializer_class = ActivityCostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['activity__name', 'supplier__name']
    filterset_fields = ['activity', 'supplier', 'currency', 'is_active']

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        cost = self.get_object()
        history = cost.price_history.all()
        serializer = ActivityCostHistorySerializer(history, many=True)
        return Response(serializer.data)
