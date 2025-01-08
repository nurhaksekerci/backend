from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone

phone_validator = RegexValidator(
    regex=r'^\+?90?\d{10}$',
    message="Telefon numarası '+90' ile başlamalı ve 10 haneli olmalıdır."
)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Silinmiş mi?")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Silinme Tarihi")
    deleted_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name="%(class)s_deleted",
        verbose_name="Silen Kullanıcı"
    )

    def soft_delete(self, user=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    class Meta:
        abstract = True

class AuditModel(models.Model):
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created",
        verbose_name="Oluşturan Kullanıcı"
    )
    updated_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_updated",
        verbose_name="Güncelleyen Kullanıcı"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        abstract = True

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name="Para Birimi Kodu")  # USD, EUR, TRY
    name = models.CharField(max_length=50, verbose_name="Para Birimi Adı")  # US Dollar, Euro, Turkish Lira
    symbol = models.CharField(max_length=5, verbose_name="Sembol")  # $, €, ₺

    class Meta:
        verbose_name = "Para Birimi"
        verbose_name_plural = "Para Birimleri"

    def __str__(self):
        return f"{self.code} ({self.symbol})"

class Company(SoftDeleteModel, AuditModel):
    name = models.CharField(max_length=255, verbose_name="Şirket Adı")
    address = models.TextField(verbose_name="Şirket Adresi")
    tax_number = models.CharField(max_length=11, verbose_name="Vergi Numarası")
    tax_office = models.CharField(max_length=255, verbose_name="Vergi Dairesi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name="Şirket Logosu")
    
    # Yeni eklenen iletişim alanları
    phone = models.CharField(
        max_length=13,
        validators=[phone_validator],
        verbose_name="Telefon Numarası"
    )
    email = models.EmailField(verbose_name="E-posta Adresi")
    website = models.URLField(null=True, blank=True, verbose_name="Web Sitesi")
    facebook = models.URLField(null=True, blank=True, verbose_name="Facebook")
    instagram = models.URLField(null=True, blank=True, verbose_name="Instagram")
    twitter = models.URLField(null=True, blank=True, verbose_name="Twitter")
    linkedin = models.URLField(null=True, blank=True, verbose_name="LinkedIn")
    
    subscription_start_date = models.DateField(verbose_name="Abonelik Başlangıç Tarihi")
    subscription_end_date = models.DateField(verbose_name="Abonelik Bitiş Tarihi")
    is_subscription_active = models.BooleanField(default=True, verbose_name="Abonelik Aktif mi?")
    branch_limit = models.PositiveIntegerField(default=1, verbose_name="Şube Açma Hakkı")

    currencies = models.ManyToManyField(
        Currency,
        related_name='companies',
        verbose_name="Kullanılan Para Birimleri"
    )
    default_currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name='default_currency_companies',
        verbose_name="Varsayılan Para Birimi"
    )

    class Meta:
        verbose_name = "Şirket"
        verbose_name_plural = "Şirketler"

    def __str__(self):
        return self.name
    
    @property
    def total_employees(self):
        return self.employees.count()

class Branch(SoftDeleteModel, AuditModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='branches',
        verbose_name="Şirket"
    )
    name = models.CharField(max_length=255, verbose_name="Şube Adı")
    address = models.TextField(verbose_name="Şube Adresi")
    phone = models.CharField(
        max_length=13,
        validators=[phone_validator],
        verbose_name="Telefon Numarası"
    )
    email = models.EmailField(verbose_name="E-posta Adresi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")

    class Meta:
        verbose_name = "Şube"
        verbose_name_plural = "Şubeler"

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class Certificate(SoftDeleteModel, AuditModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name="Kullanıcı"
    )
    name = models.CharField(max_length=255, verbose_name="Sertifika Adı")
    file = models.FileField(upload_to='certificates/', verbose_name="Sertifika Dosyası")
    issue_date = models.DateField(verbose_name="Verilme Tarihi")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Geçerlilik Tarihi")

    class Meta:
        verbose_name = "Sertifika"
        verbose_name_plural = "Sertifikalar"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.name}"

class User(AbstractUser, SoftDeleteModel):
    ROLE_CHOICES = [
        # Yönetim
        ('GENEL_MUDUR', 'Genel Müdür'),
        ('SUBE_MUDURU', 'Şube Müdürü'),
        
        # Operasyon
        ('OPERASYON_MUDURU', 'Operasyon Müdürü'),
        ('OPERASYON_SEFI', 'Operasyon Şefi'),
        ('OPERASYON_UZMANI', 'Operasyon Uzmanı'),
        ('OPERASYON_ELEMANI', 'Operasyon Elemanı'),
        
        # Satış & Rezervasyon
        ('SATIS_MUDURU', 'Satış Müdürü'),
        ('SATIS_SEFI', 'Satış Şefi'),
        ('REZ_SEFI', 'Rezervasyon Şefi'),
        ('SATIS_TEMSILCI', 'Satış Temsilcisi'),
        ('REZ_GOREVLI', 'Rezervasyon Görevlisi'),
        
        # Rehberlik
        ('BAS_REHBER', 'Baş Rehber'),
        ('REHBER', 'Rehber'),
        ('STAJYER_REHBER', 'Stajyer Rehber'),
        
        # Transfer
        ('TRANSFER_KOOR', 'Transfer Koordinatörü'),
        ('SOFOR', 'Şoför'),
        ('HOSTES', 'Hostes'),
        
        # Muhasebe & Finans
        ('MUH_MUDURU', 'Muhasebe Müdürü'),
        ('MUH_UZMANI', 'Muhasebe Uzmanı'),
        ('MUH_ELEMANI', 'Muhasebe Elemanı'),
        
        # İnsan Kaynakları
        ('IK_MUDURU', 'İK Müdürü'),
        ('IK_UZMANI', 'İK Uzmanı'),
        
        # Pazarlama
        ('PAZ_MUDURU', 'Pazarlama Müdürü'),
        ('PAZ_UZMANI', 'Pazarlama Uzmanı'),
        ('SOSYAL_MEDYA', 'Sosyal Medya Uzmanı'),
        
        # Diğer
        ('STAJYER', 'Stajyer'),
    ]
    
    GENDER_CHOICES = [
        ('E', 'Erkek'),
        ('K', 'Kadın'),
        ('D', 'Diğer'),
    ]
    
    DRIVING_LICENSE_CHOICES = [
        ('YOK', 'Yok'),
        ('B', 'B Sınıfı'),
        ('D1', 'D1 Sınıfı'),
        ('D', 'D Sınıfı'),
        ('E', 'E Sınıfı'),
    ]

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name="Profil Resmi"
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Doğum Tarihi"
    )
    phone = models.CharField(
        max_length=13,
        validators=[phone_validator],
        null=True,
        blank=True,
        verbose_name="Telefon Numarası"
    )
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="İşe Başlama Tarihi"
    )
    driving_license = models.CharField(
        max_length=3,
        choices=DRIVING_LICENSE_CHOICES,
        default='YOK',
        verbose_name="Ehliyet Sınıfı"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name="Cinsiyet"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name="Şirket"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name="Şube"
    )
    is_company_admin = models.BooleanField(
        default=False,
        verbose_name="Şirket Yetkilisi mi?"
    )
    is_branch_admin = models.BooleanField(
        default=False,
        verbose_name="Şube Yetkilisi mi?"
    )
    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rolü"
    )

    BLOOD_TYPE_CHOICES = [
        ('0_pozitif', '0 Rh+'),
        ('0_negatif', '0 Rh-'),
        ('A_pozitif', 'A Rh+'),
        ('A_negatif', 'A Rh-'),
        ('B_pozitif', 'B Rh+'),
        ('B_negatif', 'B Rh-'),
        ('AB_pozitif', 'AB Rh+'),
        ('AB_negatif', 'AB Rh-'),
    ]

    LANGUAGE_PROFICIENCY = [
        ('baslangic', 'Başlangıç'),
        ('orta', 'Orta'),
        ('iyi', 'İyi'),
        ('ileri', 'İleri'),
        ('anadil', 'Anadil'),
    ]

    # Mevcut alanlar devam ediyor...

    # Yeni eklenen alanlar
    tckn = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='TCKN 11 haneli olmalıdır.'
            )
        ],
        verbose_name="TC Kimlik Numarası"
    )
    
    # Adres bilgileri
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name="Adres"
    )
    
    # Acil durum kontağı
    emergency_contact_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Acil Durumda Aranacak Kişi"
    )
    emergency_contact_phone = models.CharField(
        max_length=13,
        validators=[phone_validator],
        null=True,
        blank=True,
        verbose_name="Acil Durum Telefonu"
    )
    emergency_contact_relation = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Yakınlık Derecesi"
    )
    
    # Sağlık bilgileri
    blood_type = models.CharField(
        max_length=10,
        choices=BLOOD_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Kan Grubu"
    )
    
    # İş bilgileri
    department = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Departman"
    )
    annual_leave_days = models.PositiveIntegerField(
        default=14,
        verbose_name="Yıllık İzin Günü"
    )
    remaining_leave_days = models.PositiveIntegerField(
        default=14,
        verbose_name="Kalan İzin Günü"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Maaş"
    )
    salary_currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_salaries',
        verbose_name="Maaş Para Birimi"
    )
    
    # Performans
    performance_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        verbose_name="Performans Puanı"
    )
    
    # Sistem bilgileri
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Son Giriş IP Adresi"
    )

    # Groups ve Permissions için related_name ekleyelim
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

    def __str__(self):
        return f"{self.get_full_name()} - {self.company.name if self.company else 'Şirket Yok'}"

@receiver(post_save, sender=Company)
def create_main_branch(sender, instance, created, **kwargs):
    """Şirket oluşturulduğunda otomatik olarak merkez şubeyi oluşturur"""
    if created:
        Branch.objects.create(
            company=instance,
            name="Merkez Şube",
            address=instance.address,
            phone=instance.phone,  # Yeni eklenen alan
            email=instance.email,  # Yeni eklenen alan
            created_by=instance.created_by  # Audit için
        )
        instance.branch_limit = 0
        instance.save()

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name="Dil Adı")
    code = models.CharField(max_length=2, unique=True, verbose_name="Dil Kodu")  # EN, TR, DE

    class Meta:
        verbose_name = "Dil"
        verbose_name_plural = "Diller"

    def __str__(self):
        return self.name

class UserLanguage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='languages',
        verbose_name="Kullanıcı"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name="Dil"
    )
    proficiency = models.CharField(
        max_length=10,
        choices=User.LANGUAGE_PROFICIENCY,
        verbose_name="Yeterlilik Seviyesi"
    )
    
    class Meta:
        verbose_name = "Kullanıcı Dil Bilgisi"
        verbose_name_plural = "Kullanıcı Dil Bilgileri"
        unique_together = ['user', 'language']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.language.name} ({self.get_proficiency_display()})"
