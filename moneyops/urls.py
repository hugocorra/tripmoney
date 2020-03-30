from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('currency', views.CurrencyViewSet)
router.register('country', views.CountryViewSet)


urlpatterns = [
    # path(r'api-auth/', include('rest_framework.urls')),
    path('', views.index, name='index'),
    path('currency', views.CurrencyView.as_view(), name='currency'),
    path('api/', include(router.urls)),
]
