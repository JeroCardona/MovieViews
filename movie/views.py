from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot  as plt
import matplotlib
import io
import urllib, base64

# Create your views here.
def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html',{'name':'Jero Cardona'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm,'movies':movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request,'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

# Versión más eficiente
def statistics_view(request):
    # POR AÑO
    # matplotlib.use('Agg')
    # # Obtener todas las películas
    # all_movies = Movie.objects.all()

    # # Crear un diccionario para alamcenar la cantidad de películas por año
    # movie_counts_by_year = {}

    # # Filtrar las películas por año y contar la cantidad de películas por año
    # for movie in all_movies:
    #     year = movie.year if movie.year else "None"
    #     if year in movie_counts_by_year:
    #         movie_counts_by_year[year] += 1
    #     else:
    #         movie_counts_by_year[year] = 1
    
    # # Ancho de las barras 
    # bar_width = 0.5
    # # Posiciones de las barras
    # bar_positions = range(len(movie_counts_by_year))
    # # Crear la gráfica de barras
    # plt.bar(bar_positions, movie_counts_by_year.values(), width = bar_width, align = 'center')

    # # Personalizar la gráfica 
    # plt.title('Movie per year')
    # plt.xlabel('Year')
    # plt.ylabel('Number of movies')
    # plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation = 90)

    # # Ajustar el epsacio entre las barras 
    # plt.subplots_adjust(bottom = 0.3)

    # # Guardar la gráfica en un objeto BytesIO
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format = 'png')
    # buffer.seek(0)
    # plt.close()

    # # Convertir la gráfica a base64
    # image_png = buffer.getvalue()
    # buffer.close()
    # graphic = base64.b64encode(image_png)
    # graphic = graphic.decode ('utf-8')

    # # Renderizar la plantilla statistics.html con la gráfica
    # return render (request, 'statistics.html', {'graphic' : graphic})
    
    # POR GENERO
    # matplotlib.use('Agg')
    # # Obtener todas las películas de nuevo
    # all_movies = Movie.objects.all()

    # # Crear un diccionario para almacenar la cantidad de películas por género
    # movie_counts_by_genre = {}

    # # Filtrar las películas por género y contar la cantidad de películas por género
    # for movie in all_movies:
    #     # Obtener el primer género
    #     genres = movie.genre.split(',') if movie.genre else ["None"]
    #     first_genre = genres[0].strip()

    #     # Contar la cantidad de películas por género
    #     if first_genre in movie_counts_by_genre:
    #         movie_counts_by_genre[first_genre] += 1
    #     else:
    #         movie_counts_by_genre[first_genre] = 1

    # # Configuración de la gráfica de barras
    # bar_width = 0.5
    # bar_positions = range(len(movie_counts_by_genre))

    # # Crear la gráfica de barras
    # plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

    # # Personalizar la gráfica
    # plt.title('Movie per genre')
    # plt.xlabel('Genre')
    # plt.ylabel('Number of movies')
    # plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

    # # Ajustar el espacio entre las barras
    # plt.subplots_adjust(bottom=0.3)

    # # Guardar la gráfica en un objeto BytesIO
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # plt.close()

    # # Convertir la gráfica a base64
    # image_png = buffer.getvalue()
    # buffer.close()
    # graphic = base64.b64encode(image_png).decode('utf-8')

    # # Renderizar la plantilla statistics.html con la gráfica
    # return render(request, 'statistics.html', {'graphic': graphic})

    # POR AÑO Y GENERO
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}

    # Filtrar las películas y contar la cantidad por año y género
    for movie in all_movies:
        # Contar por año
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

        # Contar por género
        genres = movie.genre.split(',') if movie.genre else ["None"]
        first_genre = genres[0].strip()
        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    # Configuración de la gráfica de barras por año
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movie per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Configuración de la gráfica de barras por género
    plt.subplot(1, 2, 2)
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movie per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica combinada en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})