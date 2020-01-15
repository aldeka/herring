from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('resources/', views.get_resources, name='resources'),
    path('puzzles/', views.get_puzzles, name='get'),
    path('webhook/', views.update_puzzle_hook, name='webhook'),
    path('run_scraper/', views.run_scraper, name='run_scraper'),
    path('puzzles/<int:puzzle_id>/', views.one_puzzle, name='one_puzzle'),
    path('s/<int:puzzle_id>', views.puzzle_spreadsheet, name='puzzle_spreadsheet'),
]
