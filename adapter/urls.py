from django.urls import path
from adapter.views import MarketDetail

urlpatterns = [
    path('market/<str:ticker>', MarketDetail.as_view(), name='first')
]