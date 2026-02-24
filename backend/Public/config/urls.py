
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps_.users.urls')),
    path('category/', include('apps_.categories.urls')),
    path('seller/', include('apps_.sellers.urls')),
    path('product/', include('apps_.products.urls')),
    path('promotions/', include('apps_.promotions.urls')),
    path('cart/', include('apps_.cart.urls')),
    path('order/', include('apps_.orders.urls')),
    path('payment/', include('apps_.payments.urls')),
    path('review/', include('apps_.reviews.urls')),
    path('analytics/', include('apps_.analytics.urls')),
    path('seller-analytics/', include('apps_.sellers.urls_analytics')),
   
    
    # swager
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
