import tkinter as tk
from tkinter import ttk
from theme import DebateTheme

class SettingsManager:
    def __init__(self, root, agents):
        self.agents = agents
        
        # Create settings window
        self.window = tk.Toplevel(root)
        self.window.title("Debate Settings")
        self.window.geometry("500x600")
        self.window.configure(bg=DebateTheme.BACKGROUND)
        
        # Set theme
        DebateTheme.setup_styles()
        
        # Create main frame with padding and style
        main_frame = ttk.Frame(self.window, style="Settings.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_frame, text="Debate Settings", style="SettingsHeader.TLabel").pack(fill=tk.X)
        
        # Create sections frame
        sections_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        sections_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Mode Selection Section
        mode_frame = self._create_section(sections_frame, "Interaction Mode")
        self.mode_var = tk.StringVar(value="debate")
        ttk.Radiobutton(mode_frame, text="Debate Mode", 
                       variable=self.mode_var, value="debate",
                       style="Settings.TRadiobutton").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="Collaboration Mode", 
                       variable=self.mode_var, value="collaborate",
                       style="Settings.TRadiobutton").pack(anchor=tk.W, pady=2)
        
        # Personality Section
        personality_frame = self._create_section(sections_frame, "Agent Personality")
        self.personality_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(personality_frame, text="Enable Agent Personalities and Backstories",
                       variable=self.personality_var,
                       style="Settings.TCheckbutton").pack(anchor=tk.W, pady=2)
        ttk.Label(personality_frame, 
                 text="Disable to make agents focus purely on facts without personality traits.",
                 style="Settings.TLabel",
                 wraplength=400).pack(anchor=tk.W, pady=(0, 10))
        
        # Research Mode Section
        research_frame = self._create_section(sections_frame, "Research Mode", warning=True)
        self.unrestricted_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(research_frame, text="Enable Unrestricted Mode",
                       variable=self.unrestricted_var,
                       style="Settings.TCheckbutton").pack(anchor=tk.W, pady=2)
        
        # Warning box for unrestricted mode
        warning_frame = ttk.Frame(research_frame, style="Card.TFrame")
        warning_frame.pack(fill=tk.X, pady=10, padx=5)
        warning_icon = ttk.Label(warning_frame, text="⚠️", style="Warning.TLabel")
        warning_icon.pack(side=tk.LEFT, padx=10, pady=10)
        warning_text = "Unrestricted mode removes ALL ethical and content filters.\nFor academic research purposes only."
        ttk.Label(warning_frame, text=warning_text, 
                 style="Warning.TLabel", wraplength=300).pack(side=tk.LEFT, pady=10)
        
        # Web Research Section
        web_frame = self._create_section(sections_frame, "Web Research")
        self.web_research_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(web_frame, text="Enable Web Research",
                       variable=self.web_research_var,
                       style="Settings.TCheckbutton").pack(anchor=tk.W, pady=2)
        ttk.Label(web_frame,
                 text="Allow agents to search the web for relevant information during debates.",
                 style="Settings.TLabel",
                 wraplength=400).pack(anchor=tk.W, pady=(0, 10))
        
        # Apply Button with padding
        button_frame = ttk.Frame(main_frame, style="Settings.TFrame")
        button_frame.pack(fill=tk.X, pady=20)
        apply_button = ttk.Button(button_frame, text="Apply Settings",
                                command=self.apply_settings,
                                style="Primary.TButton")
        apply_button.pack(pady=10)
        
        # Status message (hidden initially)
        self.status_label = ttk.Label(button_frame, text="",
                                    style="Success.TLabel")
        self.status_label.pack(pady=(0, 10))
        
    def _create_section(self, parent, title, warning=False):
        """Helper method to create consistent section frames"""
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill=tk.X, pady=10, padx=5)
        
        header_style = "Warning.TLabel" if warning else "Settings.TLabel"
        ttk.Label(frame, text=title, style=header_style).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        content_frame = ttk.Frame(frame, style="Settings.TFrame")
        content_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        return content_frame
        
    def apply_settings(self):
        try:
            # Apply settings to all agents
            for agent in self.agents:
                agent.set_mode(self.mode_var.get())
                agent.set_unrestricted(self.unrestricted_var.get())
                agent.set_personality_enabled(self.personality_var.get())
            
            # Store web research setting for access
            self.web_research_enabled = self.web_research_var.get()
            
            # Show success message with checkmark
            self.status_label.configure(
                text="✓ Settings applied successfully!",
                style="Success.TLabel"
            )
            
            # Hide message after 2 seconds
            self.window.after(2000, lambda: self.status_label.configure(text=""))
            
        except Exception as e:
            # Show error message
            self.status_label.configure(
                text=f"⚠️ Error: {str(e)}",
                style="Warning.TLabel"
            )
            self.window.after(3000, lambda: self.status_label.configure(text=""))
        
    def get_web_research_enabled(self):
        return getattr(self, 'web_research_enabled', False)
