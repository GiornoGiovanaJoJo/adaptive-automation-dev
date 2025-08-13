from django.contrib import admin
from django.urls import path, include
from .views import home, dashboard

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/metrics/', include('metrics.urls')),
    path('api/integrations/', include('integrations.urls')),
    path('api/analyzer/', include('analyzer.urls')),
]
