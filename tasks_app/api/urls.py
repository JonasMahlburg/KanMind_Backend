from django.urls import path, include
from .views import tasksViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', tasksViewSet)



urlpatterns = [
   path('', include( router.urls))
]