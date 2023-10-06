from typing import Any
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

# Create your models here.


class MoviesQuerySet(models.QuerySet):
    def is_rented(self):
        return self.filter(rented=False)

    def  search(self, query):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_rented().filter(lookup)
        return qs
    
    
    


class MoviesManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return MoviesQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
    def all_without_rented(self):
        return self.get_queryset().filter(rented=False)


class Movie(models.Model):
    
    cat_age = [(2, 'Kids'),
               (12, 'Young'),
               (18, 'Adult')]
    categories = [(12, 'Action'), (2, 'Comedy'), (18, 'Stand-Up')]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=64, null=False, blank=False, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=128, null=False, blank=False, validators=[MinLengthValidator(16)])
    category = models.IntegerField(choices=categories, blank=False, null=False)
    age = models.IntegerField(choices=cat_age, blank=False, null=False)
    rented = models.BooleanField(default=False)
    objects = MoviesManager()
    

    def get_absolute_url(self):
        return reverse('movie:detail', kwargs={'pk': self.id})
    
    def delete_url(self):
        return reverse('movie:delete', kwargs={'pk': self.id})



class RentedMovie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movie_owner')
    holder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=False)
    valid_to = models.DateTimeField(null=True)
    expired_movie = models.BooleanField(default=False)

#Zamiast tworzyc nowy model mozna dodac pozycje automatyczna przy approved A/D i czytac jako historia 
class RequestedMovie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_request = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_request')
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    approved_choices = [('A', 'Approved'), ('Q', 'Queue',), ('D', 'Declined')]
    approved = models.CharField(max_length=16 ,choices=approved_choices, default='Q')
    time = models.DateTimeField()
    

@receiver(post_save, sender=RequestedMovie)
def updated_request(sender, instance, **kwargs):
    if instance.approved == 'Q':
        pass
    elif instance.approved == 'A':
        RentedMovie.objects.create(owner=instance.owner, holder=instance.user_request, movie=instance.movie, valid_to=instance.time)
        instance.movie.rented = True
        instance.movie.save()
        instance.delete()
    else:
        instance.delete()






