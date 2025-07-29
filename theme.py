import tkinter as tk
from tkinter import ttk

class DebateTheme:
    # Colors
    PRIMARY = "#2C3E50"  # Dark blue-gray
    SECONDARY = "#3498DB"  # Bright blue
    ACCENT = "#E74C3C"  # Red
    BACKGROUND = "#ECF0F1"  # Light gray
    TEXT = "#2C3E50"  # Dark blue-gray
    TEXT_LIGHT = "#7F8C8D"  # Light gray
    SUCCESS = "#27AE60"  # Green
    WARNING = "#F39C12"  # Orange
    
    # Fonts
    FONT_LARGE = ("Segoe UI", 12, "bold")
    FONT_MEDIUM = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 10)
    
    @classmethod
    def setup_styles(cls):
        style = ttk.Style()
        
        # Configure main styles
        style.configure("Main.TFrame", background=cls.BACKGROUND)
        style.configure("Control.TFrame", background=cls.BACKGROUND, padding=5)
        
        # Button styles
        style.configure("Primary.TButton",
            font=cls.FONT_MEDIUM,
            padding=(10, 5),
            background=cls.PRIMARY
        )
        
        style.configure("Secondary.TButton",
            font=cls.FONT_MEDIUM,
            padding=(10, 5),
            background=cls.SECONDARY
        )
        
        style.configure("Warning.TButton",
            font=cls.FONT_MEDIUM,
            padding=(10, 5),
            background=cls.WARNING
        )
        
        # Label styles
        style.configure("Title.TLabel",
            font=cls.FONT_LARGE,
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY
        )
        
        style.configure("Subtitle.TLabel",
            font=cls.FONT_MEDIUM,
            background=cls.BACKGROUND,
            foreground=cls.TEXT
        )
        
        # Frame styles
        style.configure("Card.TFrame",
            background=cls.BACKGROUND,
            relief="raised",
            borderwidth=1
        )
        
        # Settings window specific styles
        style.configure("Settings.TFrame",
            background=cls.BACKGROUND,
            padding=15
        )
        
        style.configure("Settings.TLabel",
            font=cls.FONT_MEDIUM,
            background=cls.BACKGROUND,
            foreground=cls.TEXT,
            padding=(0, 10, 0, 5)
        )
        
        style.configure("SettingsHeader.TLabel",
            font=cls.FONT_LARGE,
            background=cls.BACKGROUND,
            foreground=cls.PRIMARY,
            padding=(0, 0, 0, 10)
        )
        
        # Warning text style
        style.configure("Warning.TLabel",
            font=cls.FONT_SMALL,
            background=cls.BACKGROUND,
            foreground=cls.ACCENT,
            padding=(0, 5)
        )
        
        # Success text style
        style.configure("Success.TLabel",
            font=cls.FONT_SMALL,
            background=cls.BACKGROUND,
            foreground=cls.SUCCESS,
            padding=(0, 5)
        )
