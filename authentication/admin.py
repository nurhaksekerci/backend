from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Company, Branch, User, Certificate, 
    Currency, Language, UserLanguage
)

class BranchInline(admin.TabularInline):
    model = Branch
    extra = 0
    fields = ('name', 'address', 'phone', 'email', 'is_active')
    show_change_link = True

class UserInline(admin.TabularInline):
    model = User
    extra = 0
    fields = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active')
    show_change_link = True
    verbose_name = "Çalışan"
    verbose_name_plural = "Çalışanlar"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0
    fields = ('name', 'file', 'issue_date', 'expiry_date')
    show_change_link = True
    fk_name = 'user'

class UserLanguageInline(admin.TabularInline):
    model = UserLanguage
    extra = 0
    fields = ('language', 'proficiency')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_number', 'is_active', 'total_branches', 'total_employees', 'subscription_status')
    list_filter = ('is_active', 'is_subscription_active', 'created_at')
    search_fields = ('name', 'tax_number', 'email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    inlines = [BranchInline, UserInline]
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': (('name', 'logo'), ('tax_number', 'tax_office'), 'address')
        }),
        ('İletişim Bilgileri', {
            'fields': (('phone', 'email'), 'website', ('facebook', 'instagram', 'twitter', 'linkedin'))
        }),
        ('Abonelik Bilgileri', {
            'fields': (('subscription_start_date', 'subscription_end_date'), 
                      ('is_subscription_active', 'branch_limit'))
        }),
        ('Para Birimi Ayarları', {
            'fields': ('currencies', 'default_currency')
        }),
        ('Sistem Bilgileri', {
            'fields': (('created_at', 'created_by'), ('updated_at', 'updated_by')),
            'classes': ('collapse',)
        }),
    )

    def total_branches(self, obj):
        return obj.branches.count()
    total_branches.short_description = "Şube Sayısı"

    def subscription_status(self, obj):
        if obj.is_subscription_active:
            return format_html('<span style="color: green;">Aktif</span>')
        return format_html('<span style="color: red;">Pasif</span>')
    subscription_status.short_description = "Abonelik Durumu"

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone', 'email', 'is_active', 'total_employees')
    list_filter = ('is_active', 'company', 'created_at')
    search_fields = ('name', 'company__name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    inlines = [UserInline]

    def total_employees(self, obj):
        return obj.employees.count()
    total_employees.short_description = "Çalışan Sayısı"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'company', 'branch', 'role', 'is_active')
    list_filter = ('is_active', 'company', 'branch', 'role', 'gender')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'tckn')
    inlines = [CertificateInline, UserLanguageInline]
    
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': (('username', 'password'), ('first_name', 'last_name'), 
                      ('email', 'phone'), 'profile_picture')
        }),
        ('Kişisel Bilgiler', {
            'fields': (('tckn', 'gender'), ('birth_date', 'blood_type'), 
                      'address', 'driving_license')
        }),
        ('İş Bilgileri', {
            'fields': (('company', 'branch'), ('role', 'department'), 
                      ('is_company_admin', 'is_branch_admin'), 'hire_date')
        }),
        ('İzin Bilgileri', {
            'fields': (('annual_leave_days', 'remaining_leave_days'),)
        }),
        ('Maaş Bilgileri', {
            'fields': (('salary', 'salary_currency'), 'performance_score'),
            'classes': ('collapse',)
        }),
        ('Acil Durum Bilgileri', {
            'fields': (('emergency_contact_name', 'emergency_contact_phone'), 
                      'emergency_contact_relation')
        }),
        ('Yetkiler', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'issue_date', 'expiry_date')
    list_filter = ('issue_date', 'expiry_date')
    search_fields = ('name', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')
    search_fields = ('code', 'name')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'proficiency')
    list_filter = ('language', 'proficiency')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'language__name')
