from django import forms


from movies.models import Movie, RequestedMovie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'age', 'category']



class RequestedMovieForm(forms.ModelForm):
    class Meta:
        model = RequestedMovie
        fields = []
