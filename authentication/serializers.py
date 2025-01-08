from rest_framework import serializers
from .models import Company, Branch, User, Certificate, Currency, Language, UserLanguage

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']

class BranchSerializer(serializers.ModelSerializer):
    total_employees = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            'id', 'company', 'name', 'address', 'phone', 'email',
            'is_active', 'total_employees', 'created_at', 'updated_at'
        ]

    def get_total_employees(self, obj):
        return obj.employees.count()

class CompanySerializer(serializers.ModelSerializer):
    total_employees = serializers.SerializerMethodField()
    total_branches = serializers.SerializerMethodField()
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'address', 'tax_number', 'tax_office',
            'is_active', 'logo', 'phone', 'email', 'website',
            'facebook', 'instagram', 'twitter', 'linkedin',
            'subscription_start_date', 'subscription_end_date',
            'is_subscription_active', 'branch_limit',
            'currencies', 'default_currency',
            'total_employees', 'total_branches', 'branches',
            'created_at', 'updated_at'
        ]

    def get_total_employees(self, obj):
        return obj.employees.count()

    def get_total_branches(self, obj):
        return obj.branches.count()

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id', 'user', 'name', 'file', 'issue_date',
            'expiry_date', 'created_at', 'updated_at'
        ]

class UserLanguageSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name', read_only=True)

    class Meta:
        model = UserLanguage
        fields = ['id', 'language', 'language_name', 'proficiency']

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    certificates = CertificateSerializer(many=True, read_only=True)
    languages = UserLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'profile_picture', 'birth_date', 'phone',
            'hire_date', 'driving_license', 'gender', 'company',
            'branch', 'is_company_admin', 'is_branch_admin', 'role',
            'tckn', 'address', 'emergency_contact_name',
            'emergency_contact_phone', 'emergency_contact_relation',
            'blood_type', 'department', 'annual_leave_days',
            'remaining_leave_days', 'salary', 'salary_currency',
            'performance_score', 'certificates', 'languages',
            'is_active', 'date_joined', 'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'tckn': {'write_only': True}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 