from django.db import models

class Playlist(models.Model):
    # Primary key is automatically created
    spotify_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    # Otros campos relevantes para la playlist

class Track(models.Model):
    # Foreign key to Playlist    
    spotify_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    image_url = models.URLField(max_length=300)
    lyrics = models.TextField()
    danceability = models.FloatField(null=True)
    energy = models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    playlist = models.ForeignKey(Playlist, related_name='tracks', on_delete=models.CASCADE)
    acousticness = models.FloatField(null=True)
    valence = models.FloatField(null=True)
    speechiness = models.FloatField(null=True)
    popularity = models.FloatField(null=True)
    # Otros campos de características de audio si necesarios
