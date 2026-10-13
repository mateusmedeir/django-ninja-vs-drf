from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import SimpleRouter

from apps.donation.drf_api.views import DonationViewSet

app_name = 'drf'

router = SimpleRouter()
router.register(r'donation', DonationViewSet, basename='donation')

urlpatterns = [
    *router.urls,
    path('openapi.json', SpectacularAPIView.as_view(), name='schema'),
    path('docs', SpectacularSwaggerView.as_view(url_name='drf:schema'), name='docs'),
]
