import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ..models.category import Style, Category, AgeGroup
from ..models.participant import Participant
from ..models.score import Score

class ScoringApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Legacy Scoring Application")
        self.geometry("1024x768")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main notebook for styles
        self.style_notebook = ttk.Notebook(self)
        self.style_notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs for Modern and Urban
        self.modern_frame = ttk.Frame(self.style_notebook)
        self.urban_frame = ttk.Frame(self.style_notebook)
        
        self.style_notebook.add(self.modern_frame, text="Modern")
        self.style_notebook.add(self.urban_frame, text="Urban")
        
        # Create scoring frames for both styles
        self.create_scoring_frame(self.modern_frame, Style.MODERN)
        self.create_scoring_frame(self.urban_frame, Style.URBAN)
        
    def create_scoring_frame(self, parent, style):
        # Participant Info Frame
        info_frame = ttk.LabelFrame(parent, text="Participant Information")
        info_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(info_frame, text="Start Number:").grid(row=0, column=0, padx=5, pady=5)
        start_number = ttk.Entry(info_frame)
        start_number.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(info_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        name = ttk.Entry(info_frame)
        name.grid(row=0, column=3, padx=5, pady=5)
        
        # Category Selection
        category_frame = ttk.LabelFrame(parent, text="Category")
        category_frame.pack(fill='x', padx=5, pady=5)
        
        categories = [c.value for c in Category]
        age_groups = [ag.value for ag in AgeGroup]
        
        ttk.Label(category_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        category_cb = ttk.Combobox(category_frame, values=categories)
        category_cb.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(category_frame, text="Age Group:").grid(row=0, column=2, padx=5, pady=5)
        age_group_cb = ttk.Combobox(category_frame, values=age_groups)
        age_group_cb.grid(row=0, column=3, padx=5, pady=5)
        
        # Scoring Frame
        scoring_frame = ttk.LabelFrame(parent, text="Scores")
        scoring_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create headers
        headers = ["Jury Member", "Technique (30)", "Choreography (30)", 
                  "Performance (30)", "Expression (10)", "Total"]
        
        for col, header in enumerate(headers):
            ttk.Label(scoring_frame, text=header).grid(row=0, column=col, padx=5, pady=5)
        
        # Create entry fields for 4 jury members
        self.score_entries = []
        for jury in range(4):
            row_entries = []
            ttk.Label(scoring_frame, text=f"Jury {jury+1}").grid(row=jury+1, column=0, padx=5, pady=5)
            
            for col in range(4):
                entry = ttk.Entry(scoring_frame, width=10)
                entry.grid(row=jury+1, column=col+1, padx=5, pady=5)
                row_entries.append(entry)
            
            total_label = ttk.Label(scoring_frame, text="0")
            total_label.grid(row=jury+1, column=5, padx=5, pady=5)
            row_entries.append(total_label)
            
            self.score_entries.append(row_entries)
        
        # Results Frame
        results_frame = ttk.LabelFrame(parent, text="Results")
        results_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(results_frame, text="Average Score:").grid(row=0, column=0, padx=5, pady=5)
        self.average_label = ttk.Label(results_frame, text="0")
        self.average_label.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_scores).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_scores).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side='left', padx=5)
    
    def calculate_scores(self):
        for row in self.score_entries:
            try:
                total = sum(float(entry.get()) for entry in row[:-1])
                row[-1].configure(text=f"{total:.1f}")
            except ValueError:
                row[-1].configure(text="Error")
        
        self.calculate_average()
    
    def calculate_average(self):
        try:
            totals = [float(row[-1].cget("text")) for row in self.score_entries]
            average = sum(totals) / len(totals)
            self.average_label.configure(text=f"{average:.1f}")
        except ValueError:
            self.average_label.configure(text="Error")
    
    def save_scores(self):
        # TODO: Implement save functionality
        pass
    
    def clear_form(self):
        for row in self.score_entries:
            for entry in row[:-1]:
                entry.delete(0, tk.END)
            row[-1].configure(text="0")
        self.average_label.configure(text="0") 