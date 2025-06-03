from django.urls import path, include
from .views import TasksViewSet, MyAssignedTasksViewSet, CommentViewSet, TasksInReviewViewset
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter


router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename='task')
router.register(r'reviewing', TasksInReviewViewset, basename='reviewing')

tasks_router = NestedDefaultRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

review_router = NestedDefaultRouter(router, r'tasks', lookup='task')
review_router.register(r'reviewing', TasksViewSet, basename='task-reviewing')



urlpatterns = [
   path('', include( router.urls)),
   path('', include(tasks_router.urls)),
   path('', include(review_router.urls)),
   path('assigned-to-me/', MyAssignedTasksViewSet.as_view({'get': 'list'})),  
]