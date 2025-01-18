'''
URLS OF JOURNAL
'''

from .views import add_journal, journal_list
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='journal_home'),  # Homepage for the journal app
    #Quotes Page
    path('add-quote/', views.add_daily_quote, name='add_daily_quote'),
    path('quotes/', views.quote_list, name='quote_list'),
    #Journal-Page    
    path('add-journal/', views.add_journal, name='add_journal'),
    path('journal-list/', views.journal_list, name='journal_list'),
    path('journal/<int:journal_id>/', views.journal_detail, name='journal_detail'),
    path('journals/edit/<int:journal_id>/', views.edit_journal, name='edit_journal'),
    path('journals/category/<str:category_name>/', views.journal_by_category, name='journal_by_category'),
    path('goal/<int:journal_id>/', views.journal_for_goal, name='journal_for_goal'),
    path('journal/delete/<int:id>/', views.delete_journal, name='delete_journal'),
    path('journal/<int:journal_id>/export-pdf/', views.export_journal_pdf, name='export_journal_pdf'),
    
            ]


