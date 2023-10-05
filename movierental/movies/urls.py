from django.urls import path

from movies import views

app_name = 'movie'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='home'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='profile'),
    path('create/', views.MovieCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.MovieUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.MovieDeleteView.as_view(), name='delete'),
    path('profile/ruquests/<int:pk>/', views.RequestedMovieUpdateView.as_view(), name='requests_update'),
    ]