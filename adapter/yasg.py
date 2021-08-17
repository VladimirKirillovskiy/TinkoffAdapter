from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path


schema_view = get_schema_view(
   openapi.Info(
      title="Tinkoff Adapter",
      default_version='v1',
      description="Test description",
     
      
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
 #  path(r'^swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  # path(r'^redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
]