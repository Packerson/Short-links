from django.contrib import admin
from django.urls import path, include

# apps urls
api_urlpatterns = [
    path('short/', include('short.urls', namespace='short')),
]

# main urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_urlpatterns, 'api'), namespace='api')),
]
