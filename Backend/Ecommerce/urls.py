
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from rest_framework_simplejwt.authentication import JWTAuthentication 




schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v1',
      description="API documentation for the Ecommerce platform",
      contact=openapi.Contact(email="moncefzabat37@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(JWTAuthentication,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('products.urls')),
    path('', include('cart.urls')),
    path('', include('orders.urls')),
    path('', include('reviews.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
    

]
