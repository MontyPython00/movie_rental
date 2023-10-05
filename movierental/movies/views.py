from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from movies.forms import MovieForm, RequestedMovieForm
from movies.models import Movie, RequestedMovie, RentedMovie
from django.contrib.auth.models import User
from django.http import Http404

# Create your views here.


class MovieListView(generic.ListView):
    template_name = 'movies/home.html'
    model = Movie

    def get_queryset(self) -> QuerySet[Any]:
        value = self.request.GET.get('q')
        if value:
            qs = Movie.objects.search(value)
        else:
            qs = Movie.objects.all()
        
        return qs


class UserProfileView(generic.ListView):
    model = Movie
    template_name = 'movies/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        requested_movies = RequestedMovie.objects.filter(owner=self.request.user)
        context['requested_movies'] = requested_movies
        context['user_name'] = self.username
        return context

    def get(self, request, *args, **kwargs):
        self.username = self.kwargs.get('username')
        return super().get(request, *args, **kwargs)
    

    def get_queryset(self, **kwargs):
        user_name = self.username
        user = get_object_or_404(User, username=user_name)
        if user is not None:
            qs = super().get_queryset().filter(owner=user)
        else:
            #User not defined
            qs = super().get_queryset().none()
        return qs
    
class RequestedMovieUpdateView(generic.UpdateView):
    model = RequestedMovie
    fields = ['approved']
    
    def get_success_url(self):
        return reverse('movie:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['movie_title'] = self.object.movie.title
        context['request_of_user'] = self.object.user_request
        return context

class MovieCreateView(generic.CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movie:home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return redirect(obj)


class MovieDetailView(FormMixin, generic.DetailView):
    model = Movie
    form_class = RequestedMovieForm
    success_url = reverse_lazy('movie:home')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_requested = RequestedMovie.objects.filter(user_request=self.request.user).exists()
        #dodaj rented movies
        #popraw funkcje movie.objects.all
        context['is_requested'] = True if is_requested else False
        return context

    def get_success_url(self):
        return reverse('movie:detail', kwargs={'pk': self.object.id})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = self.object.owner
            form.movie = self.object
            form.user_request = self.request.user
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)
    
    

class MovieUpdateView(generic.UpdateView):
    model = Movie
    fields = ['title', 'description', 'age', 'category']
    success_url = reverse_lazy('movie:home')


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy('movie:home')

