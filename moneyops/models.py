from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=30)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=30)


class Spending(models.Model):
    date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.FloatField() 
    description = models.CharField(max_length=100) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    date_from = models.DateField()
    date_to = models.DateField()


class Transfer(models.Model):
    date = models.DateField()
    from_acc = models.ForeignKey(Account,  related_name='transfer_from', on_delete=models.CASCADE)
    to_acc = models.ForeignKey(Account,  related_name='transfer_to', on_delete=models.CASCADE)
    value_from = models.FloatField()
    value_to = models.FloatField()
    spending = models.ForeignKey(Spending, on_delete=models.CASCADE)
    details = models.CharField(max_length=100)
