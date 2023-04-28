from django.urls import path
from todo import views

urlpatterns = [
    path('', views.TodoView.as_view(), name='todo_view'),
    path('<int:todo_id>/', views.TodoUpdateView.as_view(), name='todo_update_view'),
]
