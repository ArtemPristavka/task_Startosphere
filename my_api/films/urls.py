from django.urls import path
from .views import (
    FilmApiView, FilmCreateApiView, FilmLoveApiView, UserApiViewMix, 
    UserApiView, FilmLoveByUserApiView
    )


urlpatterns = [
    path("film/", FilmCreateApiView.as_view()), # Создание фильма
    path("film/<int:pk>/", FilmApiView.as_view()), # Работа с фильмами: измнение, чтение, удаление
    path("film/love/", FilmLoveApiView.as_view()), # Работа с избранными фильмами: добавление и удаление
    path("film/love/<int:pk>/", FilmLoveByUserApiView.as_view()), # Получение избранных фильмов пользователя
    path("user/", UserApiViewMix.as_view()), # Работа с пользователем: добавление, изменение, удаление
    path("user/<int:pk>/", UserApiView.as_view()), # Получить пользователя
]
