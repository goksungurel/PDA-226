import threading

from gemini_handler import GeminiManager
from LastFMManager import LastFMManager
from ImageManager import ImageManager
from ExportManager import ExportManager

# Threading & Pipeline Architecture
# Yiğit Gürel Mora
class AlbumController:
    def __init__(self, app):
        # Reference to the main Tkinter application
        self.app = app
        # Manager classes responsible for external services
        self.gemini = GeminiManager("YOUR_GEMİNİ_API_KEY")
        self.lastfm = LastFMManager("YOUR_LASTFM_API_KEY")
        self.image_manager = ImageManager()

        self.export_manager = ExportManager(app)

        self.current_album_data = None
        self.current_tracks = None
        self.current_cover = None

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

            if not album_data:
                raise Exception("Could not retrieve Gemini data. Please check your internet connection or API quota.")

            # Step 2 - Fetch real tracks from Last.fm
            self.app.update_status("Fetching tracks...")
            tracks = self.lastfm.get_curated_tracklist(
                album_data["lastfm_tags"],
                track_count
            )

            if not tracks:
                raise Exception("No songs found from Last.fm.")

            # Step 3 - Generate AI album cover artwork
            self.app.update_status("Generating cover...")
            cover = self.image_manager.genCover(
                album_data["cover_prompt"],
                genre
            )
            # Final status update
            self.app.update_status("Album generated!")
            # Debug outputs

            self.current_album_data = album_data
            self.current_tracks = tracks
            self.current_cover = cover
            self.app.after(0, lambda: self.app.display_album(cover, album_data, tracks))

        except Exception as e:
            # Display runtime errors safely in GUI
            self.app.update_status(f"Error: {e}")
        finally:
            # Re-enable button after processing completes
            self.app.after(
                0,
                lambda: self.app.gen_btn.config(state="normal")
            )

    def save_current_album(self):
        self.export_manager.export_album(
            self.current_album_data,
            self.current_tracks,
            self.current_cover
        )