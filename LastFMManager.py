import requests
import random

class LastFMManager:
    def __init__(self, api_key):
        """
        Initialize the Last.fm manager
        """
        self.api_key = api_key
        # Requirement 1: Use the specified base URL
        self.base_url = "https://ws.audioscrobbler.com/2.0/"
        self.headers = {"User-Agent": "AlbumCoverStudio/1.0"}

    def get_curated_tracklist(self, tags, target_count):
        """
        Fetches and filters tracks based on mood tags[cite: 23, 31].
        """
        all_fetched_tracks = []
        seen_tracks = set() # Requirement 5: Duplicate filter
        final_tracklist = []

        for tag in tags:
            try:
                # Requirement 1: Call tag.gettoptracks endpoint
                params = {
                    "method": "tag.gettoptracks",
                    "tag": tag,
                    "api_key": self.api_key,
                    "format": "json",
                    "limit": int(target_count) * 2
                }
                
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                tracks = data.get("tracks", {}).get("track", [])
                all_fetched_tracks.extend(tracks)
            except Exception as e:
                print(f"Last.fm API Error: {e}")

        random.shuffle(all_fetched_tracks)

        # Requirement 5: Filter duplicates and match requested track count
        for track in all_fetched_tracks:
            track_id = f"{track['name']} - {track['artist']['name']}".lower()
            
            if track_id not in seen_tracks:
                seen_tracks.add(track_id)
                final_tracklist.append({
                    "title": track['name'],
                    "artist": track['artist']['name'],
                    "url": track['url'] # Requirement 7: Clickable links
                })
            
            if len(final_tracklist) >= int(target_count):
                break

        return final_tracklist