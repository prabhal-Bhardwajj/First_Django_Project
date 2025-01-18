'''
URLS OF JOURNAL
'''

from .views import add_journal, journal_list
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='journal_home'),  # Homepage for the journal app
    path('add-quote/', views.add_daily_quote, name='add_daily_quote'),
    path('add-journal/', views.add_journal, name='add_journal'),
    path('journal-list/', views.journal_list, name='journal_list'),
    path('journal/<int:journal_id>/', views.journal_detail, name='journal_detail'),
    path('goal/<int:journal_id>/', views.journal_for_goal, name='journal_for_goal'),
    path('journal/delete/<int:id>/', views.delete_journal, name='delete_journal'),
    path('quotes/', views.quote_list, name='quote_list'),
    
            ]


