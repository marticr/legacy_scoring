from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableView, QHeaderView, 
                              QStyledItemDelegate, QStyleOptionViewItem)
from PySide6.QtCore import Qt, Signal, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QBrush, QFont
from src.models.category import Style, Category, AgeGroup
from src.utils.translations import TRANSLATIONS
from src.models.participant import Participant
import json
from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List

@dataclass
class RankingEntry:
    start_number: int
    name: str
    category: Category
    age_group: AgeGroup
    score: float

class RankingsModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.rankings = []
        self.headers = ['#', 'Name', 'Score']
        self.group_headers = []
        
    def rowCount(self, parent=None):
        return len(self.rankings) + len(self.group_headers)
        
    def columnCount(self, parent=None):
        return len(self.headers)
        
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        row = index.row()
        col = index.column()
        
        # Check if this is a group header row
        if row in self.group_headers:
            if role == Qt.DisplayRole and col == 1:
                return self.group_headers[row]
            elif role == Qt.BackgroundRole:
                return QBrush(QColor("#333333"))
            elif role == Qt.FontRole:
                font = QFont()
                font.setBold(True)
                return font
            return None
            
        # Regular data row
        entry = self.rankings[row - len(self.group_headers)]
        
        if role == Qt.DisplayRole:
            if col == 0:
                return str(row + 1)
            elif col == 1:
                return entry.name
            elif col == 2:
                return f"{entry.score:.1f}"
                
        elif role == Qt.TextAlignmentRole:
            if col in [0, 2]:  # Rank and Score columns
                return Qt.AlignCenter
            return Qt.AlignLeft
            
        return None
        
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

class RankingsFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.language = 'english'
        self.rankings = defaultdict(list)
        self.participants = {}
        self.age_order = ['mini', 'kids', 'juniors', 'teens', 'adults']
        self.category_order = ['solo', 'duo', 'team']
        self.setup_ui()
        self.load_participants()
        self.load_rankings()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create table view
        self.table = QTableView()
        self.model = RankingsModel()
        self.table.setModel(self.model)
        
        # Configure table appearance
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table.setSelectionMode(QTableView.NoSelection)
        self.table.setAlternatingRowColors(True)
        
        # Style the table
        self.table.setStyleSheet("""
            QTableView {
                border: 1px solid #444;
                gridline-color: #444;
                background-color: #2b2b2b;
                alternate-background-color: #333333;
            }
            QHeaderView::section {
                background-color: #444;
                padding: 6px;
                border: none;
                border-right: 1px solid #555;
            }
        """)
        
        layout.addWidget(self.table)

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
        self.model.beginResetModel()
        
        # Clear existing data
        self.model.rankings = []
        self.model.group_headers = []
        
        for style in [Style.MODERN, Style.URBAN]:
            for age in self.age_order:
                for category in self.category_order:
                    key = (style.value, category, age)
                    entries = self.rankings[key]
                    if entries:
                        # Add group header
                        self.model.group_headers.append(
                            f"{age.upper()} | {category.upper()}"
                        )
                        # Add entries
                        self.model.rankings.extend(sorted(
                            entries, 
                            key=lambda x: x.score, 
                            reverse=True
                        ))
        
        self.model.endResetModel()

    def update_top3_display(self):
        # Top 3 display is now handled by the main rankings display
        pass

    def update_highest_score_display(self):
        highest_score = 0
        highest_entry = None
        
        for entries in self.rankings.values():
            if entries and entries[0].score > highest_score:
                highest_score = entries[0].score
                highest_entry = entries[0]
        
        if highest_entry:
            print(f"Highest score: {highest_entry.name} - {highest_score:.1f}")

    def refresh_rankings(self):
        """Reload and redisplay all rankings"""
        self.rankings.clear()  # Clear existing rankings
        self.load_rankings()   # Reload from scores.json 

    def update_language(self, lang):
        self.language = lang
        # Update any text that needs translation
        self.update_rankings_display() 