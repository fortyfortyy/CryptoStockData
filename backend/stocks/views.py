import ast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from stockapp.celery import REDIS_INSTANCE

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class GetStockPricesView(APIView):
    """
    Recieve data from the stock market.
    User has to be authenticated.
    """

    # @cache_page(CACHE_TTL)
    def get(self, request, *args, **kwargs):
        stock_desc_data = self.get_stock_prices()
        if not stock_desc_data:
            return Response({"no_data": "Updating..."}, status=status.HTTP_204_NO_CONTENT)

        return Response(stock_desc_data, status=status.HTTP_200_OK)

    def get_stock_prices(self):
        """
        Get stock data from external api
        """
        stock_data = {}
        for key in REDIS_INSTANCE.keys("*"):
            decoded_key = key.decode('utf-8')
            decoded_value = REDIS_INSTANCE.get(decoded_key).decode('utf-8')

            # ast.literal_eval to convert dict that is wrapped in string to dict e.g.
            # "{'USD': 16683.79}" -> {'USD': 16683.79}
            stock_data[decoded_key] = ast.literal_eval(decoded_value)

        if not stock_data:
            return ''

        sorted_desc_data = dict(
            sorted(stock_data.items(), key=lambda stock: stock[1]['USD'], reverse=True)
        )
        return sorted_desc_data


get_stock_prices_view = GetStockPricesView.as_view()
