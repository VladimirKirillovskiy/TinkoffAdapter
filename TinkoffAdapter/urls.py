from django.contrib import admin
from django.urls import path, include 
from adapter.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('adapter.urls'))
]

urlpatterns += doc_urls
