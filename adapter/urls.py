from django.urls import path
import adapter.views as ad
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('market/stocks/', ad.MarketAll.as_view(), name='marketall'),
    path('market/stocks/<str:ticker>', ad.MarketDetail.as_view(), name='marketstock'),
    path('insiders/<str:ticker>', ad.Insiders.as_view(), name='insiders10days'),
    path('insiders/<str:ticker>/<int:days>', ad.Insiders.as_view(), name='insiders'),
    path('insiders/codes/', ad.InsidersCodes.as_view(), name='ins_codes_all'),
    path('insiders/codes/<str:code>', ad.InsidersCodes.as_view(), name='ins_codes'),
]
