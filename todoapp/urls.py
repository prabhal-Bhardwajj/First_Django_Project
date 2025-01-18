'''
URLS OF TODOAPP
'''
from django.urls import path
from . import views


urlpatterns = [
    # Homepage of Todoapp
    path('', views.todo_list, name='todo_list'),

    # Tasks
    path('tasks/', views.view_all_tasks, name='view_all_tasks'),  # All tasks
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/complete/<int:id>/', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),

    # Long-Term Goals
    path('goals/', views.view_all_long_term_goals, name='view_all_long_term_goals'), # All goals
    path('goals/add/', views.add_long_term_goal, name='add_long_term_goal'),
    path('goals/delete/<int:id>/', views.delete_long_term_goal, name='delete_long_term_goal'),
    
    # link that integrates the Journalapp with this 
    path('goal/<int:journal_id>/', views.journal_for_goal, name='journal_for_goal'),

    
]