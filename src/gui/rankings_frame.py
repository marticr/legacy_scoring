from tkinter import ttk
import tkinter as tk
from src.models.category import Style, Category, AgeGroup
from src.utils.translations import TRANSLATIONS
import json
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict
from src.models.participant import Participant

@dataclass
class RankingEntry:
    start_number: int
    name: str
    category: Category
    age_group: AgeGroup
    score: float

class RankingsFrame(ttk.Frame):
    def __init__(self, parent, language='english'):
        super().__init__(parent)
        self.language = language
        self.rankings = defaultdict(list)
        self.age_order = ['mini', 'kids', 'juniors', 'teens', 'adults']
        self.category_order = ['solo', 'duo', 'team']
        self.participants = {}  # Cache for participant info
        self.create_widgets()
        self.load_participants()
        self.load_rankings()

    def load_participants(self):
        try:
            with open('data/participants.csv', 'r') as file:
                for line in file:
                    participant = Participant.from_csv_line(line.strip())
                    self.participants[participant.start_number] = participant
            print(f"Loaded {len(self.participants)} participants")
        except Exception as e:
            print(f"Error loading participants: {str(e)}")

    def get_participant_info(self, participant_id: int) -> Participant:
        return self.participants.get(int(participant_id))

    def create_widgets(self):
        # Create notebook for Modern/Urban tabs
        self.style_notebook = ttk.Notebook(self)
        self.style_notebook.pack(fill='both', expand=True)

        # Create frames for each style
        self.modern_frame = self.create_style_frame(Style.MODERN)
        self.urban_frame = self.create_style_frame(Style.URBAN)

        self.style_notebook.add(self.modern_frame, text="Modern Rankings")
        self.style_notebook.add(self.urban_frame, text="Urban Rankings")

        # Create Top 3 frame
        self.create_top3_frame()
        
        # Create Overall Highest Score frame
        self.create_highest_score_frame()

    def create_style_frame(self, style: Style) -> ttk.Frame:
        frame = ttk.Frame(self.style_notebook)
        
        # Create treeview for rankings
        tree = ttk.Treeview(frame, columns=('rank', 'name', 'score'),
                           show='headings')
        
        tree.heading('rank', text='Rank')
        tree.heading('name', text='Name')
        tree.heading('score', text='Score')
        
        # Set column widths and alignment
        tree.column('rank', width=50, anchor='center')
        tree.column('name', width=200)
        tree.column('score', width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack with scrollbar
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Store treeview reference
        setattr(self, f"{style.value}_tree", tree)
        
        return frame

    def create_top3_frame(self):
        self.top3_frame = ttk.LabelFrame(self, text="Top 3 Per Category")
        self.top3_frame.pack(fill='x', padx=5, pady=5)
        
        # Create treeview for top 3
        self.top3_tree = ttk.Treeview(self.top3_frame, columns=('rank', 'name', 'category', 'age', 'score'),
                                     show='headings', height=20)
        
        # Configure columns
        self.top3_tree.heading('rank', text='Rank')
        self.top3_tree.heading('name', text='Name')
        self.top3_tree.heading('category', text='Category')
        self.top3_tree.heading('age', text='Age Group')
        self.top3_tree.heading('score', text='Score')
        
        # Set column widths and alignment
        self.top3_tree.column('rank', width=50, anchor='center')
        self.top3_tree.column('name', width=200)
        self.top3_tree.column('category', width=100, anchor='center')
        self.top3_tree.column('age', width=100, anchor='center')
        self.top3_tree.column('score', width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.top3_frame, orient="vertical", command=self.top3_tree.yview)
        self.top3_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack with scrollbar
        scrollbar.pack(side='right', fill='y')
        self.top3_tree.pack(fill='both', expand=True, padx=5, pady=5)

    def create_highest_score_frame(self):
        self.highest_frame = ttk.LabelFrame(self, text="Overall Highest Score")
        self.highest_frame.pack(fill='x', padx=5, pady=5)
        
        self.highest_label = ttk.Label(self.highest_frame, text="-")
        self.highest_label.pack(padx=5, pady=5)

    def load_rankings(self):
        try:
            with open('data/scores.json', 'r') as file:
                data = json.load(file)
                print("\nLoaded scores:")
                for style, scores in data.items():
                    for pid, score_data in scores.items():
                        if 'final_total' in score_data:
                            print(f"ID {pid}: {score_data['final_total']}")
                
            # Process rankings for each style
            for style in [Style.MODERN, Style.URBAN]:
                style_scores = data.get(style.value, {})
                print(f"\nProcessing {style.value} scores:")
                self.process_style_rankings(style, style_scores)
                
            # Update displays
            self.update_rankings_display()
            self.update_top3_display()
            self.update_highest_score_display()
                
        except FileNotFoundError:
            print("No scores file found")
        except Exception as e:
            print(f"Error loading rankings: {str(e)}")

    def process_style_rankings(self, style: Style, scores: Dict):
        # Group scores by category and age group
        for participant_id, score_data in scores.items():
            try:
                participant_id = int(participant_id)
                print(f"\nProcessing participant {participant_id}")
                print(f"Score data: {score_data}")
            except ValueError:
                continue
            
            if 'final_total' in score_data:
                # Get participant info from participants.csv
                participant = self.get_participant_info(participant_id)
                if participant:
                    key = (style.value, participant.category.value.lower(), participant.age_group.value.lower())
                    final_score = float(score_data['final_total'])
                    print(f"Adding ranking for {participant.name}:")
                    print(f"  Category: {participant.category.value}")
                    print(f"  Age Group: {participant.age_group.value}")
                    print(f"  Final Score: {final_score}")
                    self.rankings[key].append(RankingEntry(
                        start_number=participant_id,
                        name=participant.name,
                        category=participant.category,
                        age_group=participant.age_group,
                        score=final_score
                    ))

        # Sort rankings
        for rankings in self.rankings.values():
            rankings.sort(key=lambda x: x.score, reverse=True)
            print(f"Sorted rankings: {[(e.name, e.score) for e in rankings]}")

    def update_rankings_display(self):
        for style in [Style.MODERN, Style.URBAN]:
            tree = getattr(self, f"{style.value}_tree")
            tree.delete(*tree.get_children())
            
            # Display rankings by age group and category
            for age in self.age_order:
                tree.insert('', 'end', values=('', f'{age.upper()}', ''))
                
                for category in self.category_order:
                    tree.insert('', 'end', values=('', f'{category.upper()}', ''))
                    
                    # Get and sort entries for this age/category
                    key = (style.value, category, age)
                    entries = self.rankings[key]
                    entries.sort(key=lambda x: x.score, reverse=True)
                    
                    for rank, entry in enumerate(entries, 1):
                        tree.insert('', 'end', values=(
                            rank,
                            entry.name,
                            f"{entry.score:.1f}"
                        ))

    def update_top3_display(self):
        # Clear existing entries
        self.top3_tree.delete(*self.top3_tree.get_children())
        
        for style in [Style.MODERN, Style.URBAN]:
            # Add style header
            style_id = self.top3_tree.insert('', 'end', values=('', f'=== {style.value.upper()} ===', '', '', ''))
            
            for age in self.age_order:
                # Add age group header
                age_id = self.top3_tree.insert('', 'end', values=('', f'--- {age.upper()} ---', '', '', ''))
                
                for category in self.category_order:
                    key = (style.value, category, age)
                    entries = self.rankings[key]
                    entries.sort(key=lambda x: x.score, reverse=True)
                    
                    if entries:
                        # Add category header
                        cat_id = self.top3_tree.insert('', 'end', values=('', f'> {category.upper()}', '', '', ''))
                        
                        for rank, entry in enumerate(entries[:3], 1):
                            self.top3_tree.insert('', 'end', values=(
                                rank,
                                entry.name,
                                entry.category.value,
                                entry.age_group.value,
                                f"{entry.score:.1f}"
                            ))

    def update_highest_score_display(self):
        highest_score = 0
        highest_entry = None
        
        for entries in self.rankings.values():
            if entries and entries[0].score > highest_score:
                highest_score = entries[0].score
                highest_entry = entries[0]
        
        if highest_entry:
            self.highest_label.config(
                text=f"Highest Score: {highest_entry.name} ({highest_entry.start_number}) "
                     f"- {highest_score:.1f}")

    def refresh_rankings(self):
        """Reload and redisplay all rankings"""
        self.rankings.clear()  # Clear existing rankings
        self.load_rankings()   # Reload from scores.json 