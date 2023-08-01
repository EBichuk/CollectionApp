from django.contrib import admin
from django.urls import path, include
from collection.views import page_not_found
from django.conf.urls.static import static
from collectionsite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collection.urls')),
]\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found