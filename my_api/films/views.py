from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import FilmSerializer, UserFilmLoveSerializer, UserSerializer
from django.http import Http404
from django.contrib.auth.models import User
from .models import Film


class FilmApiView(APIView):
    "Метод с pk для фильмов"

    def get_object(self, pk: int):
        "Достать фильм из БД"
        try:
            return Film.objects.get(pk=pk)
        
        except Film.DoesNotExist:
            raise Http404
    
    def get(self, request: Request, pk: int) -> Response:
        "Метод get для получения фильма"

        film = self.get_object(pk)
        serializer = FilmSerializer(film)
        
        return Response(serializer.data)
    
    def put(self, request: Request, pk: int) -> Response:
        "Метод put для изменения фильма"

        film = self.get_object(pk)
        serializer = FilmSerializer(film, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request, pk: int) -> Response:
        "Метод delete для удаления фильма"

        film = self.get_object(pk)
        film.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FilmCreateApiView(CreateModelMixin, GenericAPIView):
    "Создание фильма/ов"

    serializer_class = FilmSerializer
    model = Film
    queryset = Film.objects.get
    
    def post(self, request: Request, *args, **kwargs):
        "Создание фильма"
        
        return self.create(request, *args, **kwargs)
    

class FilmLoveApiView(APIView):
    "Для работы с избранными фильмами"

    def post(self, request: Request) -> Response:
        "Для добавления фильма в избранное к пользователю"

        serializer = UserFilmLoveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request: Request) -> Response:
        "Для удаления фильма из избранного пользователя"

        serializer = UserFilmLoveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.delete() # type: ignore
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FilmLoveByUserApiView(APIView):
    "Список фильмов по id пользователя"

    def get_object(self, pk: int):
        "Найти пользователя"

        try:
            return self.get_film(User.objects.get(pk=pk))
        
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
    
    def get_film(self, user: User):
        "Взять его список избранного"

        return Film.objects.filter(user=user).all()
    
    def get(self, request: Request, pk: int) -> Response:
        "Метод get для получения списка избранных фильмов"
        films = self.get_object(pk)
        serializer = FilmSerializer(films, many=True)
        
        return Response(serializer.data)


class UserApiViewMix(
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    GenericAPIView
):
    "Методя для создания и редактирования пользователя"

    serializer_class = UserSerializer
    model = User
    
    def post(self, request: Request, *args, **kwargs):
        "Создание пользователя"

        return self.create(request, *args, **kwargs)
        
    def put(self, request: Request, *args, **kwargs):
        "Редактирование пользователя"

        return self.update(request, *args, **kwargs)
        
    def delete(self, request: Request, *args, **kwargs):
        "Удаление пользователя"

        return self.delete(request, *args, **kwargs)


class UserApiView(APIView):
    "Для получеия пользователя"

    def get_object(self, pk: int):
        try:
            User.objects.get(pk=pk)
            
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        
    def get(self, request: Request, pk: int) -> Response:
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
