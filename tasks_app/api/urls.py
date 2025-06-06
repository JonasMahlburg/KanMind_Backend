from django.urls import path, include
from .views import TasksViewSet, MyAssignedTasksViewSet, CommentViewSet, TasksInReviewViewset
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename='task')

tasks_router = NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

review_router = NestedDefaultRouter(router, r'tasks', lookup='task')




urlpatterns = [
   path('tasks/reviewing/', TasksInReviewViewset.as_view({'get': 'list'})),
   path('tasks/assigned-to-me/', MyAssignedTasksViewSet.as_view({'get': 'list'})),
   
   path('', include(router.urls)),
   path('', include(tasks_router.urls)),
]