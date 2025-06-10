from django.urls import path, include
from .views import BoardsViewSet
from rest_framework.routers import DefaultRouter
from user_auth_app.api.views import EmailCheckView

router = DefaultRouter()
router.register(r'boards', BoardsViewSet)


urlpatterns = [
   path('', include( router.urls)),
   path('email-check/', EmailCheckView.as_view(), name='email-check'),
]