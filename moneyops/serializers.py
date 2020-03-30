from rest_framework import serializers

from moneyops.models import Currency, Country


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        #fields = ['url', 'username', 'email', 'groups']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
