import threading

from gemini_handler import GeminiManager
from LastFMManager import LastFMManager
from ImageManager import ImageManager


# Threading & Pipeline Architecture
# Yiğit Gürel Mora



class AlbumController:

    def __init__(self, app):

        # Reference to the main Tkinter application
        self.app = app

        # Manager classes responsible for external services
        self.gemini = GeminiManager("YOUR_GEMINI_API_KEY")
        self.lastfm = LastFMManager("YOUR_LASTFM_API_KEY")
        self.image_manager = ImageManager()

    # Starts album generation in a background thread
    # to prevent Tkinter GUI freezing
    def start_generation(self):

        # Disable generate button during processing
        self.app.gen_btn.config(state="disabled")

        # Run long operations asynchronously
        threading.Thread(
            target=self.generate_album_pipeline,
            daemon=True
        ).start()

    # Main album generation workflow / orchestration pipeline
    def generate_album_pipeline(self):

        try:

            # Step 1 - Generate fictional album metadata using Gemini
            self.app.update_status("Gemini is thinking...")

            journal = self.app.journal_text.get("1.0", "end").strip()
            genre = self.app.genre_combo.get()
            era = self.app.era_combo.get()
            track_count = int(self.app.track_spin.get())

            album_data = self.gemini.generate_album_metadata(
                journal,
                genre,
                era
            )

            # Step 2 - Fetch real tracks from Last.fm
            self.app.update_status("Fetching tracks...")

            tracks = self.lastfm.get_curated_tracklist(
                album_data["lastfm_tags"],
                track_count
            )

            # Step 3 - Generate AI album cover artwork
            self.app.update_status("Generating cover...")

            cover = self.image_manager.genCover(
                album_data["cover_prompt"],
                genre
            )

            # Final status update
            self.app.update_status("Album generated!")

            # Debug outputs
            print(album_data)
            print(tracks)
            print(cover)

        except Exception as e:

            # Display runtime errors safely in GUI
            self.app.update_status(f"Error: {e}")

        finally:

            # Re-enable button after processing completes
            self.app.after(
                0,
                lambda: self.app.gen_btn.config(state="normal")
            )