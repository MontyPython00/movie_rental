from movies.models import RentedMovie
from django.db.models import BooleanField, Q, ExpressionWrapper
from django.db.models.functions import Now

class SimpleMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        qs = RentedMovie.objects.filter(expired_movie=ExpressionWrapper(Q(valid_to__gte=Now()), output_field=BooleanField()))
        if qs.exists():
            for rented_movie in qs:
                rented_movie.expired_movie = True
                rented_movie.save()
                rented_movie.movie.rented = False
                rented_movie.movie.save()
        response = self.get_response(request)

        
        return response