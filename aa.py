import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-read-private playlist-read-collaborative"

MOODS = ["Happy", "Focused", "Relaxed", "Energetic", "Stressed"]
SUBJECTS = ["Math", "Programming", "Reading", "Writing", "Science"]

MAX_REJECTIONS = 3
FALLBACK_QUERY = "chill study lofi"


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=".spotify_cache"
    )


def get_spotify_client():
    """Handles the OAuth flow and returns an authenticated spotipy client."""
    sp_oauth = get_spotify_oauth()

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        params = st.query_params
        code = params.get("code")

        if code:
            token_info = sp_oauth.get_access_token(code, as_dict=True)
            st.query_params.clear()
        else:
            auth_url = sp_oauth.get_authorize_url()
            st.markdown(f"[Log in with Spotify]({auth_url})")
            st.stop()

    return spotipy.Spotify(auth=token_info["access_token"])


def search_playlist(sp, mood, subject, attempt=0):
    """Search Spotify for a playlist matching mood + subject.
    Falls back to a chill playlist after MAX_REJECTIONS attempts."""
    if attempt >= MAX_REJECTIONS:
        query = FALLBACK_QUERY
    else:
        query = f"{mood} {subject} study playlist"

    results = sp.search(q=query, type="playlist", limit=1)
    items = results.get("playlists", {}).get("items", [])

    if not items:
        return None

    playlist = items[0]
    return {
        "name": playlist["name"],
        "url": playlist["external_urls"]["spotify"],
        "track_count": playlist["tracks"]["total"]
    }


def main():
    st.title("MoodStudy")

    sp = get_spotify_client()

    if "rejections" not in st.session_state:
        st.session_state.rejections = 0
    if "current_result" not in st.session_state:
        st.session_state.current_result = None

    mood = st.selectbox("How are you feeling?", MOODS)
    subject = st.selectbox("What are you studying?", SUBJECTS)

    if st.button("Find playlist"):
        st.session_state.rejections = 0
        st.session_state.current_result = search_playlist(sp, mood, subject, 0)

    if st.session_state.current_result:
        r = st.session_state.current_result
        st.write(r["name"])
        st.write(r["url"])
        st.write(f"{r['track_count']} tracks")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Not this one"):
                st.session_state.rejections += 1
                st.session_state.current_result = search_playlist(
                    sp, mood, subject, st.session_state.rejections
                )
        with col2:
            if st.button("Use this playlist"):
                st.success("Enjoy studying!")


if __name__ == "__main__":
    main()

