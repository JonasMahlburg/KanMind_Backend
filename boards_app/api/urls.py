from django.urls import path, include
from .views import BoardsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'boards', BoardsViewSet)



urlpatterns = [
   path('', include( router.urls))
]