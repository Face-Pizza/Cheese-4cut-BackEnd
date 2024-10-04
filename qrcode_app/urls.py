from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet, qr_code_view

router = DefaultRouter()
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
    path('qr/<str:encrypted_id>/', qr_code_view, name='qr_code_view'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)