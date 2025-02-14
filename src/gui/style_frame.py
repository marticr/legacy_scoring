from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                              QLabel, QSpinBox, QPushButton, QGroupBox,
                              QFrame, QMessageBox, QSizePolicy)
from PySide6.QtCore import Signal, Qt
from src.models.category import Style
from src.models.jury import JuryMember
from src.models.participant import Participant
from src.utils.translations import TRANSLATIONS
import json

class ScoreInput(QSpinBox):
    def __init__(self, max_value=30, parent=None):
        super().__init__(parent)
        self.setRange(0, max_value)
        self.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                min-width: 60px;
            }
            QSpinBox:focus {
                border: 1px solid #666;
            }
        """)

class StyleFrame(QWidget):
    scores_updated = Signal()

    def __init__(self, style: Style, parent=None):
        super().__init__(parent)
        self.style = style
        self.current_participant_idx = 0
        self.participants = []
        self.jury_members = []
        self.scores = {}
        
        self.load_jury_members()
        self.load_participants()
        self.setup_ui()
        self.load_scores()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Navigation
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_button.clicked.connect(self.previous_participant)
        self.next_button.clicked.connect(self.next_participant)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        layout.addLayout(nav_layout)

        # Participant Info
        info_group = QGroupBox("Participant Info")
        info_layout = QGridLayout()
        self.start_number_label = QLabel("-")
        self.name_label = QLabel("-")
        self.category_label = QLabel("-")
        self.age_group_label = QLabel("-")
        
        info_layout.addWidget(QLabel("Start Number:"), 0, 0)
        info_layout.addWidget(self.start_number_label, 0, 1)
        info_layout.addWidget(QLabel("Name:"), 1, 0)
        info_layout.addWidget(self.name_label, 1, 1)
        info_layout.addWidget(QLabel("Category:"), 2, 0)
        info_layout.addWidget(self.category_label, 2, 1)
        info_layout.addWidget(QLabel("Age Group:"), 3, 0)
        info_layout.addWidget(self.age_group_label, 3, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Scoring Panel
        scoring_group = QGroupBox("Scores")
        scoring_layout = QGridLayout()

        # Headers
        headers = ['Jury', 'Technique (30)', 'Choreography (30)', 
                  'Performance (30)', 'Expression (10)', 'Total']
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setAlignment(Qt.AlignCenter)
            scoring_layout.addWidget(label, 0, col)

        # Score inputs
        self.score_inputs = {}  # {jury_id: [technique, choreography, performance, expression, total]}
        for row, jury in enumerate(self.jury_members, 1):
            scoring_layout.addWidget(QLabel(jury.name), row, 0)
            
            row_inputs = []
            for col in range(4):
                max_score = 10 if col == 3 else 30
                score_input = ScoreInput(max_score)
                score_input.valueChanged.connect(self.calculate_scores)
                scoring_layout.addWidget(score_input, row, col + 1)
                row_inputs.append(score_input)
            
            total_label = QLabel("0.0")
            total_label.setAlignment(Qt.AlignCenter)
            scoring_layout.addWidget(total_label, row, 5)
            row_inputs.append(total_label)
            
            self.score_inputs[jury.id] = row_inputs

        # Add spacer at bottom
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer)

        scoring_group.setLayout(scoring_layout)
        layout.addWidget(scoring_group)

        # Style
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #444;
                margin-top: 1ex;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QLabel {
                color: white;
            }
        """)

        self.update_display()

    def load_jury_members(self):
        try:
            with open('data/jury_config.json', 'r') as f:
                data = json.load(f)
                self.jury_members = [
                    JuryMember(member['id'], member['name'])
                    for member in data.get('jury_members', [])
                ]
        except Exception as e:
            print(f"Error loading jury members: {e}")
            self.jury_members = []

    def load_participants(self):
        try:
            with open('data/participants.csv', 'r') as f:
                self.participants = []
                for line in f:
                    participant = Participant.from_csv_line(line.strip())
                    if participant.style == self.style:
                        self.participants.append(participant)
            self.update_navigation()
        except Exception as e:
            print(f"Error loading participants: {e}")

    def load_scores(self):
        try:
            with open('data/scores.json', 'r') as f:
                data = json.load(f)
                self.scores = data.get(self.style.value, {})
        except FileNotFoundError:
            self.scores = {}
        except Exception as e:
            print(f"Error loading scores: {e}")
            self.scores = {}
        
        self.update_display()

    def save_scores(self):
        try:
            # Load existing scores
            try:
                with open('data/scores.json', 'r') as f:
                    all_scores = json.load(f)
            except FileNotFoundError:
                all_scores = {}

            # Update scores for this style
            all_scores[self.style.value] = self.scores

            # Save back to file
            with open('data/scores.json', 'w') as f:
                json.dump(all_scores, f, indent=2)

            self.scores_updated.emit()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save scores: {str(e)}")

    def calculate_scores(self):
        if not self.participants:
            return

        participant = self.participants[self.current_participant_idx]
        participant_scores = {}

        for jury_id, inputs in self.score_inputs.items():
            if all(input.value() > 0 for input in inputs[:-1]):  # Exclude total label
                total = sum(input.value() for input in inputs[:-1])
                inputs[-1].setText(f"{total:.1f}")  # Update total label
                participant_scores[str(jury_id)] = {
                    'technique': inputs[0].value(),
                    'choreography': inputs[1].value(),
                    'performance': inputs[2].value(),
                    'expression': inputs[3].value(),
                    'total': total
                }

        if participant_scores:
            # Calculate final total if all jury members have scored
            if len(participant_scores) == len(self.jury_members):
                final_total = sum(s['total'] for s in participant_scores.values()) / len(participant_scores)
                participant_scores['final_total'] = final_total

            self.scores[str(participant.start_number)] = participant_scores
            self.save_scores()

    def update_display(self):
        if not self.participants:
            self.clear_display()
            return

        participant = self.participants[self.current_participant_idx]
        
        # Update info labels
        self.start_number_label.setText(str(participant.start_number))
        self.name_label.setText(participant.name)
        self.category_label.setText(participant.category.value)
        self.age_group_label.setText(participant.age_group.value)

        # Load existing scores
        participant_scores = self.scores.get(str(participant.start_number), {})
        
        # Update score inputs
        for jury_id, inputs in self.score_inputs.items():
            jury_scores = participant_scores.get(str(jury_id), {})
            inputs[0].setValue(jury_scores.get('technique', 0))
            inputs[1].setValue(jury_scores.get('choreography', 0))
            inputs[2].setValue(jury_scores.get('performance', 0))
            inputs[3].setValue(jury_scores.get('expression', 0))

    def clear_display(self):
        self.start_number_label.setText("-")
        self.name_label.setText("-")
        self.category_label.setText("-")
        self.age_group_label.setText("-")
        
        for inputs in self.score_inputs.values():
            for input in inputs:
                input.setValue(0)

    def update_navigation(self):
        self.prev_button.setEnabled(self.current_participant_idx > 0)
        self.next_button.setEnabled(self.current_participant_idx < len(self.participants) - 1)

    def previous_participant(self):
        if self.current_participant_idx > 0:
            self.current_participant_idx -= 1
            self.update_display()
            self.update_navigation()

    def next_participant(self):
        if self.current_participant_idx < len(self.participants) - 1:
            self.current_participant_idx += 1
            self.update_display()
            self.update_navigation()

    def update_language(self, lang):
        t = TRANSLATIONS[lang]
        self.prev_button.setText(t['previous'])
        self.next_button.setText(t['next'])