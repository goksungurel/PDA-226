import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# GUI - GÖKSUN GÜREL
class AlbumCoverStudio(tk.Tk):
    # ── Color Palette (Spotify Aesthetic) ──────────────────────────
    BG = "#0d0d0d"  # Main background color
    PANEL = "#161616"  # Sidebar color
    CARD = "#1c1c1c"  # Widget and result background
    ACCENT = "#1ed760"  # Spotify green for branding
    ACCENT2 = "#ff6b35"  # Secondary accent for distinct features
    TEXT = "#ffffff"  # Primary white text
    SUBTEXT = "#b3b3b3"  # Secondary gray text
    BORDER = "#282828"  # UI divider color

    def __init__(self):
        super().__init__()
        self.title("Album Cover Studio ✦ PDA-226")
        self.configure(bg=self.BG)
        self.geometry("1100x780")
        self.minsize(900, 680)

        # Initialize UI components
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam") # Modern base theme (Requirement 2)

        # Global Styles
        style.configure(".", background=self.BG, foreground=self.TEXT,
                        fieldbackground=self.CARD, font=("Segoe UI", 10))

        # Labels
        style.configure("Title.TLabel", background=self.BG, font=("Segoe UI", 22, "bold"))
        style.configure("Sub.TLabel", foreground=self.SUBTEXT, font=("Segoe UI", 9))
        style.configure("Accent.TLabel", foreground=self.ACCENT, font=("Segoe UI", 9, "bold"))

        # --- SPINBOX MODERNIZATION (Requirement 2 & 3) ---
        # Enhanced visibility for arrow buttons and text readability
        style.configure("TSpinbox",
                        fieldbackground=self.CARD,
                        background=self.CARD,
                        foreground=self.TEXT,
                        arrowcolor=self.ACCENT,
                        arrowsize=18,
                        font=("Segoe UI", 11))

        # Input Widgets
        style.configure("TCombobox", fieldbackground=self.CARD, background=self.CARD,
                        foreground=self.TEXT, arrowcolor=self.ACCENT)

        # Buttons (Requirement 7)
        style.configure("Generate.TButton", background=self.ACCENT, foreground="#000000",
                        font=("Segoe UI", 11, "bold"), padding=(0, 12), borderwidth=0)
        style.map("Generate.TButton", background=[("active", "#17b84d")])

    def _build_ui(self):
        # Main Layout Grid
        self.columnconfigure(0, weight=0, minsize=340)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- LEFT PANEL (User Inputs) ---
        left = tk.Frame(self, bg=self.PANEL, width=340)
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_propagate(False)
        self._build_left_panel(left)

        # --- RIGHT PANEL (Results Area) ---
        self.right_frame = tk.Frame(self, bg=self.BG)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self._build_placeholder(self.right_frame)

    def _build_left_panel(self, parent):
        pad = {"padx": 20}

        # Application Branding Header
        ttk.Label(parent, text="Album Cover Studio", style="Title.TLabel", background=self.PANEL).pack(anchor="w", pady=(20, 0), **pad)
        ttk.Label(parent, text="Describe your mood · get your album", style="Sub.TLabel", background=self.PANEL).pack(anchor="w", **pad)
        tk.Frame(parent, bg=self.BORDER, height=1).pack(fill="x", pady=(15, 12))

        # AGP1: Journal Entry Text Area (Requirement 3)
        ttk.Label(parent, text="Your Mood (English or Turkish)", style="Accent.TLabel", background=self.PANEL).pack(anchor="w", **pad)
        text_frame = tk.Frame(parent, bg=self.ACCENT, padx=1, pady=1)
        text_frame.pack(fill="x", **pad, pady=5)
        self.journal_text = tk.Text(text_frame, height=7, bg=self.CARD, fg=self.TEXT,
                                    insertbackground=self.ACCENT, relief="flat", bd=0, padx=8, pady=6, wrap="word")
        self.journal_text.insert("1.0", "I was looking at the sea in İzmir...")
        self.journal_text.pack(fill="x")

        # AGP2: Genre Selection (Requirement 3)
        ttk.Label(parent, text="Genre", style="Accent.TLabel", background=self.PANEL).pack(anchor="w", **pad, pady=(10, 0))
        genres = ["Pop", "Rock", "Hip-Hop / Rap", "Electronic", "Indie", "R&B / Soul", "Jazz", "Metal", "Türk Pop", "Klasik"]
        self.genre_combo = ttk.Combobox(parent, values=genres, state="readonly")
        self.genre_combo.set("Indie")
        self.genre_combo.pack(fill="x", **pad, pady=5)

        # AGP3: Era Selection (Requirement 3)
        ttk.Label(parent, text="Era", style="Accent.TLabel", background=self.PANEL).pack(anchor="w", **pad, pady=(10, 0))
        eras = ["1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
        self.era_combo = ttk.Combobox(parent, values=eras, state="readonly")
        self.era_combo.set("2000s")
        self.era_combo.pack(fill="x", **pad, pady=5)

        # AGP4: Track Count (Requirement 3)
        ttk.Label(parent, text="Track Count", style="Accent.TLabel", background=self.PANEL).pack(anchor="w", **pad, pady=(10, 0))
        self.track_spin = ttk.Spinbox(parent, from_=6, to=14, width=5, style="TSpinbox")
        self.track_spin.set(10)
        self.track_spin.pack(anchor="w", **pad, pady=8)

        # Generate Button (Requirement 4)
        self.gen_btn = ttk.Button(parent, text="GENERATE ALBUM", style="Generate.TButton")
        self.gen_btn.pack(fill="x", padx=20, pady=(20, 10))

        # --- STATUS LABEL (Requirement 9) ---
        self.status_var = tk.StringVar(value="Ready to create.")
        self.status_lbl = ttk.Label(parent, textvariable=self.status_var, style="Sub.TLabel",
                                    background=self.PANEL, foreground=self.ACCENT)
        self.status_lbl.pack(anchor="w", padx=20, pady=5)

    def _build_placeholder(self, parent):
        self.placeholder_frame = tk.Frame(parent, bg=self.BG)
        self.placeholder_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Center Music Icon Placeholder
        canvas = tk.Canvas(self.placeholder_frame, width=120, height=120, bg=self.BG, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 110, 110, outline=self.BORDER, width=2)
        canvas.create_text(60, 60, text="♪", fill=self.BORDER, font=("Segoe UI", 38))

        ttk.Label(self.placeholder_frame, text="Generated album will appear here.",
                  style="Sub.TLabel", background=self.BG).pack(pady=12)

    def update_status(self, message):
        self.status_var.set(f"● {message}")

if __name__ == "__main__":
    app = AlbumCoverStudio()
    app.mainloop()