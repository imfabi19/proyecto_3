from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponsableViewSet, MascotaViewSet

router = DefaultRouter()
router.register(r'responsables', ResponsableViewSet)
router.register(r'mascotas', MascotaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]