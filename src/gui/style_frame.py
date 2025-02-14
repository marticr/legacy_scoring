from tkinter import ttk, messagebox
from src.models.category import Style
from src.utils.translations import TRANSLATIONS
from typing import List
from src.models.participant import Participant
from src.models.jury import JuryMember
import json

class StyleFrame(ttk.Frame):
    def __init__(self, parent, style: Style, jury_members: List[JuryMember], language='english'):
        super().__init__(parent)
        self.style = style
        self.language = language
        self.jury_members = jury_members
        self.current_participant_index = 0
        self.participants = []
        self.scores = {}  # Dict to store scores: {participant_id: {jury_id: Score}}
        self.on_scores_updated = None  # Callback for when scores change
        
        # Create all the widgets for this style
        self.create_navigation()
        self.create_info_panel()
        self.create_scoring_panel()
        self.create_results_panel()
        self.load_scores()
        
    def create_navigation(self):
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill='x', padx=5, pady=5)
        
        self.prev_button = ttk.Button(nav_frame, text=TRANSLATIONS[self.language]['previous'],
                                    command=lambda: self.navigate(-1))
        self.prev_button.configure(cursor="hand2")
        self.prev_button.pack(side='left', padx=5)
        
        self.next_button = ttk.Button(nav_frame, text=TRANSLATIONS[self.language]['next'],
                                    command=lambda: self.navigate(1))
        self.next_button.configure(cursor="hand2")
        self.next_button.pack(side='left', padx=5)
        
    def create_info_panel(self):
        self.info_frame = ttk.LabelFrame(self, text=TRANSLATIONS[self.language]['participant_info'])
        self.info_frame.pack(fill='x', padx=5, pady=5)
        
        # Create labels for participant info
        self.start_number_label = ttk.Label(self.info_frame, text="-")
        self.name_label = ttk.Label(self.info_frame, text="-")
        self.category_label = ttk.Label(self.info_frame, text="-")
        self.age_group_label = ttk.Label(self.info_frame, text="-")
        
        # Grid layout for info labels
        self.start_number_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_label.grid(row=0, column=1, padx=5, pady=5)
        self.category_label.grid(row=0, column=2, padx=5, pady=5)
        self.age_group_label.grid(row=0, column=3, padx=5, pady=5)

    def create_scoring_panel(self):
        self.scoring_frame = ttk.LabelFrame(self, text=TRANSLATIONS[self.language]['scores'])
        self.scoring_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create headers
        headers = [
            TRANSLATIONS[self.language]['jury_member'],
            TRANSLATIONS[self.language]['technique'],
            TRANSLATIONS[self.language]['choreography'],
            TRANSLATIONS[self.language]['performance'],
            TRANSLATIONS[self.language]['expression'],
            TRANSLATIONS[self.language]['jury_total']
        ]
        
        for col, header in enumerate(headers):
            ttk.Label(self.scoring_frame, text=header).grid(row=0, column=col, padx=5, pady=5)
            
        # Create entry fields for jury members
        self.score_entries = []
        for idx, jury in enumerate(self.jury_members):
            row_entries = []
            ttk.Label(self.scoring_frame, text=jury.name).grid(row=idx+1, column=0, padx=5, pady=5)
            
            for col in range(4):
                entry = ttk.Entry(self.scoring_frame, width=10)
                entry.grid(row=idx+1, column=col+1, padx=5, pady=5)
                entry.bind('<KeyRelease>', lambda e, c=col, r=idx: self.validate_and_update(e, c, r))
                row_entries.append(entry)
            
            total_label = ttk.Label(self.scoring_frame, text="0")
            total_label.grid(row=idx+1, column=5, padx=5, pady=5)
            row_entries.append(total_label)
            
            self.score_entries.append(row_entries)
            
    def create_results_panel(self):
        self.results_frame = ttk.LabelFrame(self, text=TRANSLATIONS[self.language]['results'])
        self.results_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(self.results_frame, text=TRANSLATIONS[self.language]['total_score']).grid(row=0, column=0, padx=5, pady=5)
        self.average_label = ttk.Label(self.results_frame, text="0")
        self.average_label.grid(row=0, column=1, padx=5, pady=5)

    def set_participants(self, participants: List[Participant]):
        self.participants = participants
        self.current_participant_index = 0
        self.update_display()
        self.update_navigation()

    def navigate(self, direction: int):
        if not self.participants:
            return
            
        max_index = len(self.participants) - 1
        self.current_participant_index = (self.current_participant_index + direction) % (max_index + 1)
        
        self.clear_form()
        self.update_display()
        self.update_navigation()
        
    def update_display(self):
        if not self.participants:
            self.clear_info()
            return
            
        participant = self.participants[self.current_participant_index]
        # Load saved scores if they exist
        if participant.start_number in self.scores:
            self.load_participant_scores(participant.start_number)
        
        t = TRANSLATIONS[self.language]
        
        self.start_number_label.config(text=f"{t['start_number']}: {participant.start_number}")
        self.name_label.config(text=f"{t['name']}: {participant.name}")
        self.category_label.config(text=f"{t['category']}: {participant.category.value}")
        self.age_group_label.config(text=f"{t['age_group']}: {participant.age_group.value}")
        
        self.update()
        
    def clear_info(self):
        self.start_number_label.config(text="-")
        self.name_label.config(text="-")
        self.category_label.config(text="-")
        self.age_group_label.config(text="-")
        
    def update_navigation(self):
        if not self.participants:
            self.prev_button.configure(state='disabled')
            self.next_button.configure(state='disabled')
            return
            
        self.prev_button.configure(state='normal' if self.current_participant_index > 0 else 'disabled')
        self.next_button.configure(state='normal' if self.current_participant_index < len(self.participants) - 1 else 'disabled')
        
    def validate_and_update(self, event, col, row):
        entry = event.widget
        value = entry.get().strip()
        
        if not value:  # Skip validation for empty fields
            self.calculate_scores()
            return
            
        try:
            score = int(value)
            max_score = 10 if col == 3 else 30  # Expression max is 10, others are 30
            
            if 0 <= score <= max_score:
                self.calculate_scores()
            else:
                messagebox.showerror("Invalid Input", f"Score must be between 0 and {max_score}")
                entry.delete(0, "end")
        except ValueError:
            pass
            
    def calculate_scores(self):
        for row_idx, row in enumerate(self.score_entries):
            try:
                scores = [float(entry.get() or 0) for entry in row[:-1]]
                jury_total = sum(scores)
                row[-1].configure(text=f"{jury_total:.1f}")
                
                # Save scores
                if self.participants:  # Only save if we have participants
                    participant = self.participants[self.current_participant_index]
                    jury = self.jury_members[row_idx]
                    
                    if participant.start_number not in self.scores:
                        self.scores[participant.start_number] = {}
                        
                    self.scores[participant.start_number][str(jury.id)] = {
                        'technique': scores[0],
                        'choreography': scores[1],
                        'performance': scores[2],
                        'expression': scores[3],
                        'total': jury_total
                    }
                    
                    self.save_scores()
            except ValueError:
                row[-1].configure(text="0.0")
                
        # Calculate final total after all jury scores are saved
        if self.participants:
            participant = self.participants[self.current_participant_index]
            if participant.start_number in self.scores:
                jury_totals = []
                for jury_id, jury_data in self.scores[participant.start_number].items():
                    if jury_id != 'final_total' and isinstance(jury_data, dict) and 'total' in jury_data:
                        jury_totals.append(jury_data['total'])
                
                if jury_totals:
                    participant_total = sum(jury_totals) / len(jury_totals)
                    print(f"Final total for participant {participant.start_number}: {participant_total}")
                    self.scores[participant.start_number]['final_total'] = participant_total
                    self.save_scores()
        
        self.calculate_average()
        
    def calculate_average(self):
        try:
            jury_scores = [float(row[-1].cget("text")) for row in self.score_entries]
            total_score = sum(jury_scores) / len(jury_scores)
            self.average_label.configure(text=f"{total_score:.1f}")
        except ValueError:
            self.average_label.configure(text="0.0")
            
    def clear_form(self):
        for row in self.score_entries:
            for entry in row[:-1]:
                entry.delete(0, "end")
            row[-1].configure(text="0.0")
        self.average_label.configure(text="0.0")
        
    def update_language(self, language: str):
        self.language = language
        t = TRANSLATIONS[language]
        
        # Update all text elements
        self.info_frame.configure(text=t['participant_info'])
        self.scoring_frame.configure(text=t['scores'])
        self.results_frame.configure(text=t['results'])
        self.prev_button.configure(text=t['previous'])
        self.next_button.configure(text=t['next'])
        
        # Update the current display
        self.update_display() 

    def load_scores(self):
        try:
            with open('data/scores.json', 'r') as file:
                all_scores = json.load(file)
                # Filter scores for this style
                style_scores = all_scores.get(self.style.value, {})
                self.scores = {int(k): v for k, v in style_scores.items()}
        except FileNotFoundError:
            print("No previous scores found")
        except Exception as e:
            print(f"Error loading scores: {str(e)}")

    def save_scores(self):
        try:
            # Load existing scores first
            try:
                with open('data/scores.json', 'r') as file:
                    all_scores = json.load(file)
            except FileNotFoundError:
                all_scores = {}
            
            # Update scores for this style
            all_scores[self.style.value] = self.scores
            
            # Save back to file
            with open('data/scores.json', 'w') as file:
                json.dump(all_scores, file, indent=2)
            
            # Notify that scores have been updated
            if self.on_scores_updated:
                self.on_scores_updated()
        except Exception as e:
            print(f"Error saving scores: {str(e)}")
            messagebox.showerror("Error", f"Could not save scores: {str(e)}")

    def load_participant_scores(self, participant_id: int):
        if participant_id not in self.scores:
            return
            
        participant_scores = self.scores[participant_id]
        # Skip the 'final_total' key which isn't a jury score
        for jury_id_str, score_data in participant_scores.items():
            if jury_id_str == 'final_total':
                continue
            
            jury_id = int(jury_id_str)  # Convert string ID to int
            try:
                jury_idx = next(i for i, j in enumerate(self.jury_members) if j.id == jury_id)
                row = self.score_entries[jury_idx]
                
                # Clear any existing values first
                for entry in row[:-1]:
                    entry.delete(0, "end")
                
                # Fill in the scores
                row[0].insert(0, str(score_data['technique']))
                row[1].insert(0, str(score_data['choreography']))
                row[2].insert(0, str(score_data['performance']))
                row[3].insert(0, str(score_data['expression']))
            except StopIteration:
                print(f"Warning: Jury member {jury_id} not found")
                continue
        
        self.calculate_scores() 