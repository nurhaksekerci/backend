from rest_framework import serializers
from .models import Operation, OperationCustomer, OperationSalesPrice, OperationDay, OperationItem, OperationSubItem
from files.serializers import *
class OperationCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationCustomer
        fields = '__all__'

class OperationSalesPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationSalesPrice
        fields = '__all__'

class OperationSubItemReadSerializer(serializers.ModelSerializer):
    museums = MuseumSerializer(many=True, read_only=True)
    activity = ActivitySerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)
    guide = GuideSerializer(read_only=True)
    tour = TourSerializer(read_only=True)
    transfer = TransferSerializer(read_only=True)
    class Meta:
        model = OperationSubItem
        fields = '__all__'

class OperationItemReadSerializer(serializers.ModelSerializer):
    subitems = OperationSubItemReadSerializer(many=True, read_only=True)
    no_vehicle_activity = ActivitySerializer(read_only=True)
    no_vehicle_tour = NoVehicleTourSerializer(read_only=True)
    vehicle_supplier = VehicleSupplierSerializer(read_only=True)
    activity_supplier = ActivitySupplierSerializer(read_only=True)
    vehicle_cost = VehicleCostSerializer(read_only=True)
    activity_cost = ActivityCostSerializer(read_only=True)
    vehicle_type_name = serializers.CharField(source='vehicle_type.name', read_only=True)
    vehicle_supplier_name = serializers.CharField(source='vehicle_supplier.name', read_only=True)
    no_vehicle_tour_name = serializers.CharField(source='no_vehicle_tour.name', read_only=True)
    activity_name = serializers.CharField(source='no_vehicle_activity.name', read_only=True)
    activity_supplier_name = serializers.CharField(source='activity_supplier.name', read_only=True)

    class Meta:
        model = OperationItem
        fields = '__all__'

class OperationItemSerializer(serializers.ModelSerializer):
    vehicle_type_name = serializers.CharField(source='vehicle_type.name', read_only=True)
    vehicle_supplier_name = serializers.CharField(source='vehicle_supplier.name', read_only=True)
    no_vehicle_tour_name = serializers.CharField(source='no_vehicle_tour.name', read_only=True)
    activity_name = serializers.CharField(source='no_vehicle_activity.name', read_only=True)
    activity_supplier_name = serializers.CharField(source='activity_supplier.name', read_only=True)
    class Meta:
        model = OperationItem
        fields = '__all__'


class OperationSubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationSubItem
        fields = '__all__'


    def create(self, validated_data):
        # no_vehicle_tour ID'sini al
        no_vehicle_tour_id = validated_data.get('no_vehicle_tour')

        # Nesneyi oluştur
        instance = super().create(validated_data)

        # no_vehicle_tour'u özel olarak güncelle
        if no_vehicle_tour_id:
            instance.no_vehicle_tour_id = no_vehicle_tour_id
            instance.save()

        return instance

class OperationDaySerializer(serializers.ModelSerializer):
    items = OperationItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = OperationDay
        fields = '__all__'

class OperationSerializer(serializers.ModelSerializer):
    days = OperationDaySerializer(many=True, read_only=True)
    customers = OperationCustomerSerializer(many=True, read_only=True)
    sales_prices = OperationSalesPriceSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    follow_by_name = serializers.CharField(source='follow_by.get_full_name', read_only=True)
    buyer_company_name = serializers.CharField(source='buyer_company.name', read_only=True)

    class Meta:
        model = Operation
        fields = '__all__'