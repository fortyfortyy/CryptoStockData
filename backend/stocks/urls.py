from django.urls import path, include

from stocks.views import get_stock_prices_view

urlpatterns = [
    path('', get_stock_prices_view, name='stock_prices')
]
