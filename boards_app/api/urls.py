from django.urls import path, include
from .views import BoardsViewSet, BoardsDetailView
from rest_framework.routers import DefaultRouter
from user_auth_app.api.serializers import EmailCheckView

router = DefaultRouter()
router.register(r'boards', BoardsViewSet)



urlpatterns = [
   path('', include( router.urls)),
   path('boards/<int:pk>/', BoardsDetailView.as_view(), name='board-detail'),
   path('email-check/', EmailCheckView.as_view(), name='email-check'),
]