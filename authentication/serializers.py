from rest_framework import serializers
from .models import Company, Branch, User, Certificate, Currency, Language, UserLanguage
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

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

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    user = UserSerializer(read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError('Geçersiz kullanıcı adı veya şifre.')

            if not user.is_active:
                raise serializers.ValidationError('Hesap aktif değil.')

            return {
                'username': user.username,
                'user': UserSerializer(user).data,
                'tokens': self.get_tokens({'username': username})
            }
        
        raise serializers.ValidationError('Kullanıcı adı ve şifre gereklidir.')

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh')
        
        try:
            refresh = RefreshToken(refresh_token)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return data
        except Exception as e:
            raise serializers.ValidationError('Geçersiz veya süresi dolmuş token.') 