from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=30)


class Country(models.Model):
    name = models.CharField(max_length=50)
    currency = models.ForeignKey()


class Conta(models.Model):
    name = models.CharField(max_length=100)
    currency = models.ForeignKey()


class Category(models.Model):
    name = models.CharField(max_length=100)


class Transfer(models.Model):
    date = models.DateField()
    from_acc = models.ForeignKey()
    to_acc = models.ForeignKey()
    value_from = models.FloatField()
    value_to = models.FloatField()
    spending = models.ForeignKey()
    details = models.CharField()


class Spending(models.Model):
    date = models.DateField()
    country = models.ForeignKey()
    account = models.ForeignKey()
    currency = models.ForeignKey()
    amount = models.FloatField() 
    description = models.CharField() 
    category = models.ForeignKey() 
    date_from = models.DateField()
    date_to = models.DateField()
