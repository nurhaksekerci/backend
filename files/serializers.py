from rest_framework import serializers
from .models import *
from django.utils import timezone

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'is_active']

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']

class BuyerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerCompany
        fields = ['id', 'company', 'name', 'short_name', 'contact', 'is_active', 'created_at', 'updated_at']

class TourSerializer(serializers.ModelSerializer):
    start_city_name = serializers.CharField(source='start_city.name', read_only=True)
    end_city_name = serializers.CharField(source='end_city.name', read_only=True)

    class Meta:
        model = Tour
        fields = ['id', 'company', 'name', 'start_city', 'start_city_name', 'end_city', 'end_city_name',
                 'is_active', 'created_at', 'updated_at']

class NoVehicleTourSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = NoVehicleTour
        fields = ['id', 'company', 'name', 'city', 'city_name', 'is_active', 'created_at', 'updated_at']

class TransferSerializer(serializers.ModelSerializer):
    start_city_name = serializers.CharField(source='start_city.name', read_only=True)
    end_city_name = serializers.CharField(source='end_city.name', read_only=True)

    class Meta:
        model = Transfer
        fields = ['id', 'company', 'name', 'start_city', 'start_city_name', 'end_city', 'end_city_name',
                 'is_active', 'created_at', 'updated_at']

class HotelPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPriceHistory
        fields = ['id', 'hotel', 'single_price', 'double_price', 'triple_price', 'currency',
                 'valid_from', 'valid_until', 'is_active', 'created_at']

class HotelSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    current_prices = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'company', 'name', 'city', 'city_name', 'single_price', 'double_price',
                 'triple_price', 'currency', 'currency_code', 'valid_until', 'is_active',
                 'created_at', 'updated_at', 'current_prices']

    def get_current_prices(self, obj):
        current = obj.get_price_for_date(timezone.now().date())
        if current:
            return HotelPriceHistorySerializer(current).data
        return None

class MuseumPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MuseumPriceHistory
        fields = ['id', 'museum', 'local_price', 'foreign_price', 'currency',
                 'valid_from', 'valid_until', 'is_active', 'created_at']

class MuseumSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    current_prices = serializers.SerializerMethodField()

    class Meta:
        model = Museum
        fields = ['id', 'company', 'name', 'city', 'city_name', 'local_price', 'foreign_price',
                 'currency', 'currency_code', 'valid_until', 'is_active', 'created_at',
                 'updated_at', 'current_prices']

    def get_current_prices(self, obj):
        current = obj.get_price_for_date(timezone.now().date())
        if current:
            return MuseumPriceHistorySerializer(current).data
        return None

class ActivitySerializer(serializers.ModelSerializer):
    cities_names = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'company', 'name', 'cities', 'cities_names', 'is_active', 'created_at', 'updated_at']

    def get_cities_names(self, obj):
        return [city.name for city in obj.cities.all()]

class GuideSerializer(serializers.ModelSerializer):
    cities_names = serializers.SerializerMethodField()

    class Meta:
        model = Guide
        fields = ['id', 'company', 'name', 'phone', 'document_no', 'cities', 'cities_names',
                 'is_active', 'created_at', 'updated_at']

    def get_cities_names(self, obj):
        return [city.name for city in obj.cities.all()]

class VehicleSupplierSerializer(serializers.ModelSerializer):
    cities_names = serializers.SerializerMethodField()

    class Meta:
        model = VehicleSupplier
        fields = ['id', 'company', 'name', 'cities', 'cities_names', 'is_active', 'created_at', 'updated_at']

    def get_cities_names(self, obj):
        return [city.name for city in obj.cities.all()]

class ActivitySupplierSerializer(serializers.ModelSerializer):
    cities_names = serializers.SerializerMethodField()

    class Meta:
        model = ActivitySupplier
        fields = ['id', 'company', 'name', 'cities', 'cities_names', 'is_active', 'created_at', 'updated_at']

    def get_cities_names(self, obj):
        return [city.name for city in obj.cities.all()]

class VehicleCostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleCostHistory
        fields = ['id', 'vehicle_cost', 'car_cost', 'minivan_cost', 'minibus_cost', 'midibus_cost',
                 'bus_cost', 'currency', 'valid_from', 'valid_until', 'is_active', 'created_at']

class VehicleCostSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    current_prices = serializers.SerializerMethodField()

    class Meta:
        model = VehicleCost
        fields = ['id', 'company', 'supplier', 'supplier_name', 'tour', 'transfer', 'car_cost',
                 'minivan_cost', 'minibus_cost', 'midibus_cost', 'bus_cost', 'currency',
                 'currency_code', 'valid_until', 'is_active', 'created_at', 'updated_at',
                 'current_prices']

    def get_current_prices(self, obj):
        current = obj.get_price_for_date(timezone.now().date())
        if current:
            return VehicleCostHistorySerializer(current).data
        return None

class ActivityCostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCostHistory
        fields = ['id', 'activity_cost', 'price', 'currency', 'valid_from', 'valid_until',
                 'is_active', 'created_at']

class ActivityCostSerializer(serializers.ModelSerializer):
    activity_name = serializers.CharField(source='activity.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    current_prices = serializers.SerializerMethodField()

    class Meta:
        model = ActivityCost
        fields = ['id', 'company', 'activity', 'activity_name', 'supplier', 'supplier_name',
                 'price', 'currency', 'currency_code', 'valid_until', 'is_active',
                 'created_at', 'updated_at', 'current_prices']

    def get_current_prices(self, obj):
        current = obj.get_price_for_date(timezone.now().date())
        if current:
            return ActivityCostHistorySerializer(current).data
        return None