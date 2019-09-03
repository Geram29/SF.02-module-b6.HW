# Импортируем необходимые библиотеки
import os
import json
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
# подключаем свой модуль album.py
import album


# GET-запрос на исполнителя:
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        err_message = "Альбомов исполнителя {} не найдено!".format(artist)
        result = HTTPError(404, err_message)
    else:
        album_names = [album.album + " - " + str(album.year) for album in albums_list]
        cnt_albums = str(len(album_names))
        result = "Список альбомов {}:<br>---------------------------------------------------------<br>".format(artist)
        result += "<br>".join(album_names)
        result += "<br>---------------------------------------------------------<br>Всего альбомов: {}<br>".format(cnt_albums)
    return result


# POST-запрос на новый альбом:
@route("/albums", method="POST")
def new_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # блок валидации запроса пользователя
    if album_data:
        
        result = ""
        separline ="\n*******************************************************************************************************\n"
        # проверка корректности параметров запроса
        if album_data["album"] == None or album_data["artist"] == None or album_data["genre"] == None or album_data["year"] == None:
            err_message = separline + "   ОТСУТСТВУЮТ НЕОБХОДИМЫЕ ПАРАМЕТРЫ ЗАПРОСА  Код ошибки: 500   " + separline
            result = HTTPError(500, err_message)
        else:
        # проверка корректности данных
            if album_data["album"].replace(" ", "") == "":
                # result = "\n****************************************************\n   НЕКОРРЕКТНЫЕ ДАННЫЕ  =album=  Код ошибки: 400  \n****************************************************\n"
                err_message = separline + "   НЕКОРРЕКТНЫЕ ДАННЫЕ  album=  Код ошибки: 400  " + separline
                result = HTTPError(400, err_message)
            elif album_data["artist"].replace(" ", "") == "": 
                # result = "\n****************************************************\n   НЕКОРРЕКТНЫЕ ДАННЫЕ  =artist=  Код ошибки: 400  \n****************************************************\n"
                err_message = separline + "   НЕКОРРЕКТНЫЕ ДАННЫЕ  artist=  Код ошибки: 400  " + separline
                result = HTTPError(400, err_message)
            elif album_data["genre"].replace(" ", "") == "":
                # result = "\n****************************************************\n   НЕКОРРЕКТНЫЕ ДАННЫЕ  =genre=  Код ошибки: 400  \n****************************************************\n"
                err_message = separline + "   НЕКОРРЕКТНЫЕ ДАННЫЕ  genre=  Код ошибки: 400  " + separline
                result = HTTPError(400, err_message)
            elif album_data["year"].replace(" ", "") == "" or album.is_int(album_data["year"]) == False or int(album_data["year"]) <= 0:
                # result = "\n****************************************************\n   НЕКОРРЕКТНЫЕ ДАННЫЕ  =year=  Код ошибки: 400  \n****************************************************\n"
                err_message = separline + "   НЕКОРРЕКТНЫЕ ДАННЫЕ  year=  Код ошибки: 400  " + separline
                result = HTTPError(400, err_message)
        # если валидация ОК - добавление нового альбома в БД
        if result == "":
            if album.add(album_data):
                result = ">>> Альбом <{}> исполнителя {} успешно сохранен!".format(album_data["album"].title(), album_data["artist"].title())
            else:
                err_message = (separline + "   АЛЬБОМ НЕ СОХРАНЕН! {} УЖЕ ЕСТЬ В БАЗЕ ДАННЫХ! Код ошибки: 409   " + separline).format(album_data["album"].title())
                result = HTTPError(409, err_message)
                # result = err_message
        return result

    else:
        err_message = ">>> *** ЗАПРОС К СЕРВЕРУ НЕ СРАБОТАЛ ***"
        result = HTTPError(500, err_message)

    return result



if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

# http -f POST http://localhost:8080/albums year=1968 artist="Deep Purple" genre="Hard Rock" album="Shades of Deep Purple"
