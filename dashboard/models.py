"""
App Models
"""
from mongoengine import Document, StringField, IntField, FloatField
# Create your models here.

class movies(Document):
    """
    Movies Collection
    """
    movieId = StringField()
    title = StringField()
    genres = StringField()
    
class ratings(Document):
    """
    Ratings Collection
    """
    userId = IntField()
    movieId = StringField()
    rating = FloatField()
    timestamp = StringField()

class sortedmovies(Document):
    """
    SortedMovies Collection
    """
    title = StringField()
    sum_rating = FloatField()
    count_rating = IntField()
    average_rating = FloatField()
    genres = StringField()

class recs(Document):
    """
    Recommends Collection
    """
    userId = StringField()
    movieId = StringField()
    rating = IntField()

class tags(Document):
    """
    Tags Collection
    """
    userId = StringField()
    movieId = StringField()
    tag = StringField()
    timestamp = StringField()

class links(Document):
    """
    Links Collection
    """
    movieId = StringField()
    imdbId = StringField() 
    tmdbId = StringField()      

class genome_tags(Document):
    """
    Genome Tags Collection
    """
    tagId = StringField()
    tag = StringField()

class genome_scores(Document):
    """
    Genome Scores Collection
    """
    movieId = StringField()
    tagId = StringField()
    relevance = StringField()