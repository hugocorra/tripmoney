from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework import permissions

from moneyops.models import Currency, Country
from moneyops.serializers import CurrencySerializer, CountrySerializer


def index(request):
    context = {}
    return render(request, 'moneyops/index.html', context)


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.AllowAny]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class CurrencyView(TemplateView):
    template_name = "moneyops/currency.html"
