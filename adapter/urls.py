from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
import adapter.views as ad

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),

    path('market/stocks/', ad.MarketStocksList.as_view(), name='marketall'),
    path('market/stocks/<str:ticker>/', ad.MarketStocksDetail.as_view(), name='marketstock'),
    path('market/stocks/earn/<str:ticker_name>/', ad.QuartEarnings.as_view(), name='earnings'),
    path('market/stocks/nextearns/<str:ticker_name>/', ad.NextEarns.as_view(), name='next earnings'),
    path('market/stocks/info/<str:ticker_name>/', ad.Info.as_view(), name='info'),
    path('market/stocks/dividends/<str:ticker_name>/', ad.Dividends.as_view(), name='dividends'),
    path('market/stocks/nextdivs/<str:ticker_name>/', ad.NextDivs.as_view(), name='next dividends'),
    path('market/stocks/recommendations/<str:ticker>/', ad.Recommendations.as_view(), name='Recommendations'),
    path('market/stocks/recommendations-days/<str:ticker>/<int:days>/', ad.RecommendationsInDays.as_view(), name='Recommendations in days'),
    path('market/stocks/major-holders/<str:ticker>/', ad.MajorHolders.as_view(), name='Major holders'),

    path('market/currencies/', ad.MarketCurrenciesList.as_view(), name='currencies'),
    path('market/currencies/<str:currency>/', ad.MarketCurrenciesDetail.as_view(), name='currencies'),

    path('insiders/<str:ticker>/', ad.Insiders.as_view(), name='insiders10days'),
    path('insiders/<str:ticker>/<int:days>/', ad.Insiders.as_view(), name='insiders'),
  
    path('sandbox/account/register/', ad.SandboxAccountRegister.as_view(), name='sandbox_register'),
    path('sandbox/account/remove/', ad.SandboxAccountRemove.as_view(), name='sandbox_remove'),
    path('sandbox/account/clear/', ad.SandboxAccountClear.as_view(), name='sandbox_clear'),
    path('sandbox/set-stock-balance/', ad.SandboxSetStocks.as_view(), name='sandbox_stock'),
    path('sandbox/set-currency-balance/', ad.SandboxSetCurrencies.as_view(), name='sandbox_currency'),

    path('operations/portfolio/stocks/', ad.CheckPortfolioStocks.as_view(), name='sandbox_stocks'),
    path('operations/portfolio/currencies/', ad.CheckPortfolioCurrencies.as_view(), name='sandbox_currencies'),
    path('operations/marketorder/stocks/', ad.StocksMarketOrder.as_view(), name='sandbox_stocks_market_order'),
    path('operations/marketorder/currencies/', ad.CurrenciesMarketOrder.as_view(), name='currencies_market_order'),

    path('news/sentiment/<str:ticker>/', ad.NewsSentiment.as_view(), name='news_sentiment'),
    path('news/company-news/<str:ticker>/', ad.NewsCompany.as_view(), name='news_company_10days'),
    path('news/company-news/<str:ticker>/<int:days>/', ad.NewsCompany.as_view(), name='news_company'),
]
