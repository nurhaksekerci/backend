from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Company, Branch, User, Certificate, Currency, Language, UserLanguage
from .serializers import (
    CompanySerializer, BranchSerializer, UserSerializer,
    CertificateSerializer, CurrencySerializer, LanguageSerializer,
    UserLanguageSerializer, LoginSerializer, TokenRefreshSerializer
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def branches(self, request, pk=None):
        company = self.get_object()
        branches = Branch.objects.filter(company=company)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        company = self.get_object()
        employees = User.objects.filter(company=company)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        branch = self.get_object()
        employees = User.objects.filter(branch=branch)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def certificates(self, request, pk=None):
        user = self.get_object()
        certificates = Certificate.objects.filter(user=user)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def languages(self, request, pk=None):
        user = self.get_object()
        languages = UserLanguage.objects.filter(user=user)
        serializer = UserLanguageSerializer(languages, many=True)
        return Response(serializer.data)

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserLanguageViewSet(viewsets.ModelViewSet):
    queryset = UserLanguage.objects.all()
    serializer_class = UserLanguageSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
