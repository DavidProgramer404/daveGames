
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#panel Admin

admin.site.site_header = "DaveGames Admin"
admin.site.site_title = "DaveGames Admin Portal"
admin.site.index_title = "Welcome to the DaveGames Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
