from django.urls import path, include
from .views import TasksViewSet, TasksAssignedToMeAsReviewerViewSet, CommentViewSet, TasksInReviewViewset
from boards_app.api.views import BoardsViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename='task')
router.register(r'boards', BoardsViewSet, basename='boards')

tasks_router = NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

review_router = NestedDefaultRouter(router, r'tasks', lookup='task')




urlpatterns = [
   path('tasks/reviewing/', TasksInReviewViewset.as_view({'get': 'list'})),
   path('tasks/assigned-to-me/', TasksAssignedToMeAsReviewerViewSet.as_view({'get': 'list'})),
   path('boards/<int:pk>/', BoardsViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}), name='board-detail'),

   path('', include(router.urls)),
   path('', include(tasks_router.urls)),
]