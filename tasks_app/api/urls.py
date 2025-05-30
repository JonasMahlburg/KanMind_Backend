from django.urls import path, include
from .views import TasksViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TasksViewSet)



urlpatterns = [
   path('', include( router.urls))
]