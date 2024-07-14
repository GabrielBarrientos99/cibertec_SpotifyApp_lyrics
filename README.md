# Spotify Lyrics App
Aplicación que utiliza la API de Spotify para obtener las características de las canciones de una playlist, y la API de Genius para recuperar las letras de las canciones.

![image](https://github.com/user-attachments/assets/01dfff3b-cb36-4bbb-8218-2223423f36c3)

## Requisitos

- Python 3.x
- pip (Python package installer)
- Cuenta en [Spotify Developer](https://developer.spotify.com/dashboard/applications) para obtener las credenciales de la API.
- Cuenta en [Genius](https://genius.com/api-clients) para obtener el token de acceso de la API.

## Instalación

### Crear un archivo .env

```python
SPOTIPY_CLIENT_ID='ID_CLIENT_HERE'
SPOTIPY_CLIENT_SECRET='CLIENT_SECRET_HERE'
GENIUS_CLIENT_ACCESS_TOKEN='TOKEN_ACCESS_HERE'
