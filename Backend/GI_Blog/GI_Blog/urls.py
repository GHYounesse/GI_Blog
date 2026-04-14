from django.contrib import admin
from django.urls import path, include

import users.views

import blog.views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls, name='admin'),

    # API Authentication Endpoints
    path("api/", include("users.urls")),

    

    
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





