"""
App Views
"""
import re
import json
from math import ceil
from django.http import HttpResponse
from django.template import loader
from dashboard.models import movies, sortedmovies, recs



def index(request):
    """
    index view
    shows main page
    """
    template = loader.get_template('dashboard/index.html')

    page = request.GET.get('page', 1)

    countof_movies = movies.objects().count()
    total_pages = ceil(countof_movies/10)
    skip = (int(page)-1)*10
    movies_objects = movies.objects[skip:skip+10]

    pipeline = [{"$project" : {"movieId" : 1,
                               "title" : 1,
                               "genres" : {"$replaceAll" : \
                              {"input" : "$genres", "find" : "|", "replacement" : " "}}}}]

    movies_objects = movies_objects.aggregate(pipeline)
    movie_json = json.dumps(list(movies_objects), default=str)
    json_data = json.loads(movie_json)

    context = {'data': json_data, 'page' : page, 'totalPage' : total_pages}

    return HttpResponse(template.render(context, request))


def search(request):
    """
    search view
    searches by movie name
    """
    template = loader.get_template('dashboard/index.html')

    search_val = request.GET.get('value')
    page = request.GET.get('page', 1)

    regex = re.compile('.*'+search_val+'.*', re.IGNORECASE)
    countof_movies = movies.objects(title=regex).count()
    total_pages = ceil(countof_movies/10)
    skip = (int(page)-1)*10
    movies_objects = movies.objects(title=regex)[skip:skip+10]

    pipeline = [{"$project" : {"movieId" : 1,
                               "title" : 1,
                               "genres" : {"$replaceAll" : \
                              {"input" : "$genres", "find" : "|", "replacement" : " "}}}}]

    movies_objects = movies_objects.aggregate(pipeline)
    movie_json = json.dumps(list(movies_objects), default=str)
    json_data = json.loads(movie_json)

    context = {'data': json_data, 'page' : page, 'totalPage' : total_pages, 'searchValue' : search_val}

    return HttpResponse(template.render(context, request))

def top10(request):
    """
    top10 view
    shows top10 movies by selected genre
    """
    template = loader.get_template('dashboard/top10.html')

    search_genre = request.GET.get('genre')

    regex = re.compile('.*'+search_genre+'.*', re.IGNORECASE)

    pipeline = [{"$match" : {"genres": regex}}, {"$limit" : 10}, \
        {"$project" :{"title" : 1,
                      "sum_rating" : 1,
                      "count_rating":1,
                      "average_rating" : {"$round" : ["$average_rating", 2]},
                      "genres" : {"$replaceAll" : \
                     {"input" : "$genres", "find" : "|", "replacement" : " "}}}}]

    sortedmovies_objects = sortedmovies.objects().aggregate(pipeline)
    sortedmovies_objects = json.dumps(list(sortedmovies_objects), default=str)
    json_data = json.loads(sortedmovies_objects)

    context = {"data" : json_data}

    return HttpResponse(template.render(context, request))

def recommend(request):
    """
    recommends movies to a specific user
    input user as userid into searchbar
    """
    template = loader.get_template('dashboard/recommend.html')

    search_userid = request.GET.get('userId')

    pipeline = []
    if search_userid  is not None:
        pipeline.append({"$match":{"userId":search_userid}})

    pipeline.append({"$lookup":{"from":"movies",
                                "localField":"movieId",
                                "foreignField":"movieId",
                                "as":"movie"}})
    pipeline.append({"$unwind":"$movie"})
    pipeline.append({"$project" :{"userId" : 1,
                                  "movieId" : 1,
                                  "movie.title" : 1,
                                  "rating" : 1,
                                  "movie.genres" : {"$replaceAll" : \
                    {"input" : "$movie.genres", "find" : "|", "replacement" : " "}}}})

    pipeline.append({"$limit":10})

    recs_objects = recs.objects().aggregate(pipeline)
    recs_objects = json.dumps(list(recs_objects), default=str)
    json_data = json.loads(recs_objects)
    
    context = {"data" : json_data}

    return HttpResponse(template.render(context, request))
