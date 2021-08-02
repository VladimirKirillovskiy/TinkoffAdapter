from django.urls import path
from adapter.views import (MarketDetail, Insiders)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/<str:ticker>', MarketDetail.as_view(), name='first')
]

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/<str:ticker>', MarketDetail.as_view(), name='market'),
    path('insiders/<str:ticker>&<int:days>', Insiders.as_view(), name='insiders'),
    path('insiders/<str:ticker>', Insiders.as_view(), name='insidersT'),  # вызов за последние 7 дней по умол.
]
