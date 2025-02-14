import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox
from src.models.category import Style, Category, AgeGroup
from src.models.participant import Participant
from src.models.score import Score
from src.models.jury import JuryMember
from src.utils.translations import TRANSLATIONS
from typing import List, Dict
import json
from itertools import count
from src.gui.style_frame import StyleFrame
from src.gui.rankings_frame import RankingsFrame

class ScoreValidator:
    def __init__(self, language='english'):
        self.language = language

    def validate_main_score(self, value: str) -> tuple[bool, str]:
        try:
            score = int(value)
            if 0 <= score <= 30:
                return True, ""
            return False, TRANSLATIONS[self.language]['score_range_error'].format(max=30)
        except ValueError:
            return False, TRANSLATIONS[self.language]['number_error']

    def validate_expression(self, value: str) -> tuple[bool, str]:
        try:
            score = int(value)
            if 0 <= score <= 10:
                return True, ""
            return False, "Expression score must be between 0 and 10"
        except ValueError:
            return False, "Score must be a whole number"

class ScoringApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.geometry("1024x768")
        self.title("Legacy Scoring Application")
        
        self.language = 'english'
        
        self.load_jury_members()
        self.load_participants()
        self.create_widgets()
        
    def create_widgets(self):
        # Initialize language variable first
        self.language_var = tk.StringVar(value='EN')
        self.theme_var = tk.StringVar(value='darkly')
        
        # Create menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        # Create theme menu
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Theme", menu=self.theme_menu)
        
        # Add theme options (ttkbootstrap themes with good contrast)
        themes = [
            ('Darkly', 'darkly'),
            ('Superhero', 'superhero'),
            ('Solar', 'solar'),
            ('Cyborg', 'cyborg'),
            ('Vapor', 'vapor'),
            ('Morph', 'morph'),
            ('Cosmo', 'cosmo'),
            ('Journal', 'journal'),
            ('Litera', 'litera'),
            ('Flatly', 'flatly'),
        ]
        
        for theme_name, theme_id in themes:
            self.theme_menu.add_radiobutton(
                label=theme_name,
                variable=self.theme_var,
                value=theme_id,
                command=lambda t=theme_id: self.change_theme(t),
                selectcolor='white'
            )
        
        # Create language menu
        self.language_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Language", menu=self.language_menu)
        self.language_menu.add_radiobutton(label="English", 
                                         command=lambda: self.switch_language('english'),
                                         variable=self.language_var,
                                         selectcolor='white',
                                         value='EN')
        self.language_menu.add_radiobutton(label="Nederlands", 
                                         command=lambda: self.switch_language('dutch'),
                                         variable=self.language_var,
                                         selectcolor='white',
                                         value='NL')
        
        # Set initial checkmark
        self.language_menu.invoke(0)
        
        # Create a frame for the tab area
        tab_area = ttk.Frame(self)
        tab_area.pack(fill='x', padx=10, pady=5)
        
        # Create notebook and pack it to the left of tab area
        self.style_notebook = ttk.Notebook(tab_area)
        self.style_notebook.pack(fill='both', expand=True)
        
        # Create rankings frame first so we can pass the callback
        self.rankings_frame = RankingsFrame(self.style_notebook, self.language)
        
        # Create style frames
        self.modern_frame = StyleFrame(self.style_notebook, Style.MODERN, 
                                     self.jury_members[Style.MODERN], self.language)
        self.urban_frame = StyleFrame(self.style_notebook, Style.URBAN,
                                    self.jury_members[Style.URBAN], self.language)
        
        # Set up callbacks for score updates
        self.modern_frame.on_scores_updated = self.rankings_frame.refresh_rankings
        self.urban_frame.on_scores_updated = self.rankings_frame.refresh_rankings
        
        self.style_notebook.add(self.modern_frame, text="Modern")
        self.style_notebook.add(self.urban_frame, text="Urban")
        self.style_notebook.add(self.rankings_frame, text="Rankings")
        
        # Initialize to English
        self.language = 'english'
        
        # Initialize with participants
        self.modern_frame.set_participants(self.participants[Style.MODERN])
        self.urban_frame.set_participants(self.participants[Style.URBAN])
    
    def on_language_change(self, event):
        # Map dropdown value to language code
        lang_map = {'EN': 'english', 'NL': 'dutch'}
        new_language = lang_map[self.language_var.get()]
        self.switch_language(new_language)

    def switch_language(self, lang):
        self.language = lang
        self.modern_frame.update_language(lang)
        self.urban_frame.update_language(lang)

    def load_jury_members(self):
        # TODO: Load from config file
        self.jury_members = {
            Style.MODERN: [
                JuryMember(1, "Sarah Johnson", "Modern"),
                JuryMember(2, "Michael Chen", "Modern"),
                JuryMember(3, "Emma Davis", "Modern"),
                JuryMember(4, "James Wilson", "Modern")
            ],
            Style.URBAN: [
                JuryMember(1, "Alex Rodriguez", "Urban"),
                JuryMember(2, "Maya Patel", "Urban"),
                JuryMember(3, "David Kim", "Urban"),
                JuryMember(4, "Sophie Martin", "Urban")
            ]
        }
        
    def load_participants(self):
        self.participants = {
            Style.MODERN: [],
            Style.URBAN: []
        }
        
        try:
            with open('data/participants.csv', 'r') as file:
                csv_lines = file.readlines()
                for line in csv_lines:
                    participant = Participant.from_csv_line(line.strip())
                    self.participants[participant.style].append(participant)
            
            print(f"Successfully loaded {len(csv_lines)} participants")
            print(f"Modern: {len(self.participants[Style.MODERN])}")
            print(f"Urban: {len(self.participants[Style.URBAN])}")
        except FileNotFoundError:
            print("Error: participants.csv not found in data directory")
            messagebox.showerror("Error", "Could not load participants data")
        except Exception as e:
            print(f"Error loading participants: {str(e)}")
            messagebox.showerror("Error", f"Error loading participants: {str(e)}")
        
    def on_tab_change(self, event):
        pass  # Each style frame handles its own state 

    def change_theme(self, theme_name: str):
        """Change the application theme"""
        self.style.theme_use(theme_name) 