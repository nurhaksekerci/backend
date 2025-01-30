from django.shortcuts import render
<<<<<<< HEAD
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Operation, OperationCustomer, OperationSalesPrice, OperationDay, OperationItem, OperationSubItem
from .serializers import (
    OperationSerializer, OperationCustomerSerializer, OperationSalesPriceSerializer,
    OperationDaySerializer, OperationItemSerializer, OperationSubItemSerializer
)

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'is_active', 'company', 'branch', 'buyer_company', 'created_by', 'follow_by']  # created_by'yi ekledik
    search_fields = ['reference_number', 'buyer_company__name']
    ordering_fields = ['start_date', 'created_at', 'reference_number']
    pagination_class = None

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Operation.objects.none()

        return Operation.objects.filter(company=self.request.user.company)


    @action(detail=True)
    def full_details(self, request, pk=None):
        operation = self.get_object()
        serializer = self.get_serializer(operation)
        return Response(serializer.data)

class OperationCustomerViewSet(viewsets.ModelViewSet):
    queryset = OperationCustomer.objects.all()
    serializer_class = OperationCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['operation', 'customer_type', 'is_active', 'is_buyer']
    search_fields = ['first_name', 'last_name', 'passport_no']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return OperationCustomer.objects.none()

        return OperationCustomer.objects.filter(operation__company=self.request.user.company)

class OperationSalesPriceViewSet(viewsets.ModelViewSet):
    queryset = OperationSalesPrice.objects.all()
    serializer_class = OperationSalesPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'currency', 'is_active']
    pagination_class = None

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return OperationSalesPrice.objects.none()

        return OperationSalesPrice.objects.filter(operation__company=self.request.user.company)

class OperationDayViewSet(viewsets.ModelViewSet):
    queryset = OperationDay.objects.all()
    serializer_class = OperationDaySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['operation', 'date', 'is_active']
    ordering_fields = ['date']
    pagination_class = None

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return OperationDay.objects.none()

        return OperationDay.objects.filter(operation__company=self.request.user.company)

class OperationItemViewSet(viewsets.ModelViewSet):
    queryset = OperationItem.objects.all()
    serializer_class = OperationItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation_day', 'item_type', 'is_active']
    pagination_class = None

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return OperationItem.objects.none()

        return OperationItem.objects.filter(operation_day__operation__company=self.request.user.company)

class OperationSubItemViewSet(viewsets.ModelViewSet):
    queryset = OperationSubItem.objects.all()
    serializer_class = OperationSubItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['operation_item', 'subitem_type', 'is_active']
    ordering_fields = ['ordering']
    pagination_class = None

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return OperationSubItem.objects.none()

        return OperationSubItem.objects.filter(operation_item__operation_day__operation__company=self.request.user.company)
=======

# Create your views here.
>>>>>>> 56a07c6e4ea95ffd215c388348ff0b8d7c2dbe33
