from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import Http404
from .models import Film


class FilmSerializer(serializers.ModelSerializer):
    "Описывыает фильм"

    class Meta:
        model = Film
        fields = ["id", "name", "description"]


class UserFilmSerializer(serializers.Serializer):
    "Вложенность с id пользователя"

    id = serializers.IntegerField()


class FilmLoveSerializer(serializers.Serializer):
    "Вложенность с id фильма"
    id = serializers.IntegerField()

    
class UserFilmLoveSerializer(serializers.Serializer):
    "Для взаимосвязи между фильмом и пользователем"
    
    user = UserFilmSerializer()
    film = FilmLoveSerializer()

    def get_user(self, pk: int):
        "Достаем пользователя"

        try:
            return User.objects.get(pk=pk)
        
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")

    def get_film(self, pk: int):
        "Достаем фильм"

        try:
            return Film.objects.get(pk=pk)
        
        except Film.DoesNotExist:
            raise Http404("Фильм не найден")
        
    def save(self, **kwargs):
        "Для добавления фильма в избранное пользователю"
        
        user_id = self.validated_data["user"]["id"] # type: ignore
        film_id = self.validated_data["film"]["id"] # type: ignore
        
        user = self.get_user(user_id)
        film=self.get_film(film_id)
        film.user.add(user)
        film.save()
        
    def delete(self, **kwargs):
        "Для удаления фильма из избранного пользователя"

        user_id = self.validated_data["user"]["id"] # type: ignore
        film_id = self.validated_data["film"]["id"] # type: ignore
        
        user = self.get_user(user_id)
        film=self.get_film(film_id)
        film.user.remove(user)
        film.save()
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
    

    