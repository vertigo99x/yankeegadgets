from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

#from base.views import Logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')), 
    path('',include('base.urls')),
    #path('api/v1/person/logout/',Logout.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


