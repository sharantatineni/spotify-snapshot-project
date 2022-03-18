import os
from flask import Flask, redirect, url_for, render_template,request,session,flash
from flask_session import Session
import spotipy
import uuid
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)
load_dotenv()

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)
def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route("/")
def home():
    if(not session.get('uuid')):
        session['uuid'] = str(uuid.uuid4())
    authenticate_manager = spotipy.oauth2.SpotifyOAuth(client_id = os.getenv("client_id"), client_secret = os.getenv("client_secret"),redirect_uri = 'https://spotify-snapshot.herokuapp.com/',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
    if(request.args.get('code')):
        authenticate_manager.get_access_token(request.args.get('code'))
        return redirect("/")
    if(not authenticate_manager.get_cached_token()):
        a_url = authenticate_manager.get_authorize_url()
        return render_template("home.html",a_url = a_url)
    return redirect("/short")

def WeightedAverage(artists):
    added = 0
    weights = 0
    n = len(artists)
    for (i,x) in enumerate(artists):
        added += (2.5*n-i)*(x['popularity'])
        weights += (2.5*n-i)
    return round(added/weights)

@app.route("/short")
def short():
    auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = os.getenv("client_id"),client_secret = os.getenv("client_secret"),redirect_uri = 'https://spotify-snapshot.herokuapp.com/',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
    if(not auth_manage.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manage)
    results = spotify.current_user_top_artists(20,0,"short_term")
    songs = spotify.current_user_top_tracks(20,0,"short_term")
    weighted = WeightedAverage(results['items'])
    songavg = WeightedAverage(songs['items'])
    total = int((weighted+songavg)/2)
    return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, total = total, time = "Last Month")

@app.route("/mid")
def mid():
    auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = os.getenv("client_id"),client_secret = os.getenv("client_secret"),redirect_uri = 'https://spotify-snapshot.herokuapp.com/',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
    if(not auth_manage.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manage)
    results = spotify.current_user_top_artists(20,0,"medium_term")
    songs = spotify.current_user_top_tracks(20,0,"medium_term")
    weighted = WeightedAverage(results['items'])
    songavg = WeightedAverage(songs['items'])
    total = int((weighted+songavg)/2)
    return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, total = total, time = "Last 6 Months")


@app.route("/long")
def long():
    auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = os.getenv("client_id"),client_secret = os.getenv("client_secret"),redirect_uri = 'https://spotify-snapshot.herokuapp.com/',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
    if(not auth_manage.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manage)
    results = spotify.current_user_top_artists(20,0,"long_term")
    songs = spotify.current_user_top_tracks(20,0,"long_term")
    weighted = WeightedAverage(results['items'])
    songavg = WeightedAverage(songs['items'])
    total = int((weighted+songavg)/2)
    return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, total = total, time = "All Time")


@app.route("/index")
def test():
    auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = os.getenv("client_id"),client_secret = os.getenv("client_secret"),redirect_uri = 'https://spotify-snapshot.herokuapp.com/',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
    if(not auth_manage.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manage)
    results = spotify.current_user_top_artists(20,0,"long_term")
    songs = spotify.current_user_top_tracks(20,0,"long_term")
    weighted = WeightedAverage(results['items'])
    songavg = WeightedAverage(songs['items'])
    total = int((weighted+songavg)/2)
    return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, total = total)

@app.route("/logout")
def logout():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')




if (__name__ == "__main__"):
        app.run(debug = True)