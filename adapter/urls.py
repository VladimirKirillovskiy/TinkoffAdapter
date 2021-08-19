from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
import adapter.views as ad

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/stocks/', ad.MarketStocksList.as_view(), name='marketall'),
    path('market/stocks/<str:ticker>', ad.MarketStocksDetail.as_view(), name='marketstock'),
    path('market/stocks/earn/<str:ticker_name>', ad.QuartEarnings.as_view(), name='earnings'),
    path('market/stocks/nextearns/<str:ticker_name>', ad.NextEarns.as_view(), name='next earnings'),
    path('market/stocks/info/<str:ticker_name>', ad.Info.as_view(), name='info'),
    path('market/stocks/dividends/<str:ticker_name>', ad.Dividends.as_view(), name='dividends'),
    path('market/stocks/nextdivs/<str:ticker_name>', ad.NextDivs.as_view(), name='next dividends'),
    path('market/currencies/', ad.MarketCurrenciesList.as_view(), name='currencies'),
    path('market/currencies/<str:currency>', ad.MarketCurrenciesDetail.as_view(), name='currencies'),
    path('insiders/<str:ticker>', ad.Insiders.as_view(), name='insiders10days'),
    path('insiders/<str:ticker>/<int:days>', ad.Insiders.as_view(), name='insiders'),

    path('operations/portfolio/stocks/', ad.CheckPortfolioStocks.as_view(), name='stocks'),
    path('operations/portfolio/currencies/', ad.CheckPortfolioCurrencies.as_view(), name='currencies'),
    path('operations/marketorder/stocks/', ad.StocksMarketOrder.as_view(), name='Stocks Market Order'),
    path('operations/marketorder/currencies/', ad.CurrenciesMarketOrder.as_view(), name='Currencies Market Order'),
]
