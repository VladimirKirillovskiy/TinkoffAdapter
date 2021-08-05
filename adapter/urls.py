from django.urls import path
import adapter.views as ad
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/currencies', ad.MarketCurrencies.as_view(), name='currencies'),
    path('stock/earn/<str:ticker_name>', ad.QuartEarnings.as_view(), name='earnings'),
    path('stock/nextearns/<str:ticker_name>', ad.NextEarns.as_view(), name='next earnings'),
    path('stock/info/<str:ticker_name>', ad.Info.as_view(), name='info'),
    path('stock/dividends/<str:ticker_name>', ad.Dividends.as_view(), name='dividends'),
    path('stock/nextdivs/<str:ticker_name>', ad.NextDivs.as_view(), name='next dividends'),
    path('market/<str:ticker>', ad.MarketDetail.as_view(), name='first')
]
