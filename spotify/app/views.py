from django.shortcuts import render, redirect
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.parse
import os
from django.contrib import messages
import lyricsgenius as lg
from .models import Playlist, Track
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login():
    author_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")        
    )
    sp = spotipy.Spotify(auth_manager=author_manager)
    return sp

def login_genius():
    genius = lg.Genius(os.getenv("GENIUS_CLIENT_ACCESS_TOKEN"))
    return genius

def get_lyrics(genius, artist, song):
    try:
        song = genius.search_song(song, artist)
        return song.lyrics if song else "Lyrics not found."
    except Exception as e:
        return f"Error fetching lyrics: {str(e)}"


def display_playlist(request):
    if request.method == 'POST':
        playlist_url = request.POST.get('playlist_url')
        # Extraemos el id en https://open.spotify.com/playlist/1KN7c1hI3Ej7hxRXaWcd1s?si=f19aa53db1464764
        # verificamos si es una url
        if 'open.spotify.com' not in playlist_url:
            # Mostramos una advertencia que no es una url
            messages.warning(request, 'La URL proporcionada no es una URL de Spotify válida.')

            return redirect('index')
        
        parsed = urllib.parse.urlparse(playlist_url)
        playlist_id = parsed.path.split('/')[-1]

        playlist, created = Playlist.objects.get_or_create(spotify_id=playlist_id)
        
        if not created and playlist.tracks.exists():
            tracks = playlist.tracks.all()
        else:            
            # Logearse en Spotify
            sp = login()
            # Logearse en Genius
            genius = login_genius()
            # Obtenemos las canciones de la playlist
            dic_playlist = sp.playlist(playlist_id)
            # Almacenamos el nombre de la playlist
            playlist.name = dic_playlist.get('name', '')

            # Recorremos cada canción de la playlist
            tracks = []
            for track_dic in dic_playlist['tracks']['items']:
                track = track_dic['track']
                # Obtenemos el id del track
                track_id = track['id']
                # Obtenemos la popularidad
                popularity = track['popularity']
                # Obtener las caracteristicas del audio por ID_track
                features_audio = sp.audio_features(track_id)[0]
                # Almacenamos las caracteristicas del audio en el diccionario de la canción
                # Obtenemos la letra de las canciones  
                try:
                    lyrics = get_lyrics(genius, track['artists'][0]['name'], track['name'])
                except Exception as e:
                    lyrics = "Error fetching lyrics."
                
                track_obj, _ = Track.objects.update_or_create(
                    spotify_id=track_id,
                    defaults={
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'image_url': track['album']['images'][0]['url'],
                        'lyrics': lyrics,
                        'danceability': features_audio.get('danceability'),
                        'energy': features_audio.get('energy'),
                        'tempo': features_audio.get('tempo'),
                        'valence': features_audio.get('valence'),
                        'speechiness': features_audio.get('speechiness'),
                        'acousticness': features_audio.get('acousticness'),
                        'playlist': playlist,
                        'popularity': popularity
                    }
                )
                tracks.append(track_obj)
            playlist.save()
                    

            return render(request, 'index.html', {'tracks': tracks})
        return render(request, 'index.html', {'tracks': tracks})


