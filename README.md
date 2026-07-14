# MoodStudy

MoodStudy is a Streamlit-based study productivity app that recommends Spotify playlists based on the user's current mood and study subject. It combines mood tracking with music discovery to help students find the right playlist for focused study sessions.

Underneath the simple UI, MoodStudy behaves like a lightweight **agent**: it perceives the user's state (mood + subject), decides on a search strategy, acts by querying the Spotify API, and adapts its behavior based on feedback — falling back to a safe default playlist after repeated rejections instead of searching endlessly. Every decision it makes (searches, rejections, fallbacks, errors) is recorded automatically through a logging system, so its behavior can be traced and debugged after the fact.

- Asks the user to select their current mood and the subject they're studying
- Uses mood + subject together to determine which type of playlist to recommend
- Connects to Spotify via OAuth to search and retrieve playlist recommendations
- Displays playlist results with name, link, and track count
- Allows the user to reject a suggested playlist and get a new one
- Defaults to a chill playlist after 3 rejections to avoid endless searching
- Automatically logs key events (logins, searches, rejections, errors) to `logs/app.log`

## Files

- **`aa.py`** — Main application file. Contains the Spotify OAuth flow, the playlist search and rejection/fallback logic, the logging setup, and the Streamlit UI. This is the file you run to start the app.
- **`requirements.txt`** — Python dependencies needed to run the app: `streamlit`, `spotipy`, `python-dotenv`.
- **`.gitignore`** — Tells Git to ignore files that shouldn't be shared, like your local `.env` (Spotify credentials) and Spotify's token cache.
- **`logs/`** — Contains `app.log`, an audit log generated automatically by the app. It records authentication events, playlist searches, rejections/fallbacks, and API errors with timestamps.
- **`README.md`** — This file.

## Setup

1. Install dependencies:
   ```
   pip3 install -r requirements.txt --break-system-packages
   ```
2. Create a `.env` file in the same folder as `aa.py` with your Spotify credentials:
   ```
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8501
   ```
3. Run the app:
   ```
   python3 -m streamlit run aa.py
   ```
