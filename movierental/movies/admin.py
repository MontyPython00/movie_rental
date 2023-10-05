from django.contrib import admin

from movies.models import Movie, RentedMovie, RequestedMovie

# Register your models here.

admin.site.register(Movie)
admin.site.register(RentedMovie)
admin.site.register(RequestedMovie)