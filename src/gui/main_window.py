from PySide6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                              QMenuBar, QMenu, QComboBox)
from PySide6.QtCore import Qt
from .style_frame import StyleFrame
from .rankings_frame import RankingsFrame
from src.models.category import Style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Legacy Scoring Application")
        self.resize(1024, 768)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create menu bar
        menu_bar = self.menuBar()
        
        # Add theme menu
        theme_menu = menu_bar.addMenu("Theme")
        light_action = theme_menu.addAction("Light")
        dark_action = theme_menu.addAction("Dark")
        
        # Connect theme actions
        light_action.triggered.connect(lambda: self.change_theme(False))
        dark_action.triggered.connect(lambda: self.change_theme(True))
        
        # Create language actions
        language_menu = menu_bar.addMenu("Language")
        english_action = language_menu.addAction("English")
        dutch_action = language_menu.addAction("Nederlands")
        
        # Connect language actions
        english_action.triggered.connect(lambda: self.change_language("EN"))
        dutch_action.triggered.connect(lambda: self.change_language("NL"))

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Create frames
        self.rankings_frame = RankingsFrame()
        self.modern_frame = StyleFrame(Style.MODERN)
        self.urban_frame = StyleFrame(Style.URBAN)

        # Add tabs
        self.tab_widget.addTab(self.modern_frame, "Modern")
        self.tab_widget.addTab(self.urban_frame, "Urban")
        self.tab_widget.addTab(self.rankings_frame, "Rankings")

        # Set dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #444;
            }
            QTabBar::tab {
                background: #333;
                color: #fff;
                padding: 8px 20px;
                border: 1px solid #444;
            }
            QTabBar::tab:selected {
                background: #444;
            }
            QMenuBar {
                background-color: #333;
                color: #fff;
            }
            QMenuBar::item:selected {
                background-color: #444;
            }
            QComboBox {
                background-color: #333;
                color: #fff;
                border: 1px solid #555;
                padding: 5px;
            }
        """)

    def load_data(self):
        # Connect frames
        self.modern_frame.scores_updated.connect(self.rankings_frame.refresh_rankings)
        self.urban_frame.scores_updated.connect(self.rankings_frame.refresh_rankings)

    def change_language(self, lang_code):
        lang = 'dutch' if lang_code == 'NL' else 'english'
        self.modern_frame.update_language(lang)
        self.urban_frame.update_language(lang)
        self.rankings_frame.update_language(lang)

    def change_theme(self, is_dark: bool):
        """Change application theme"""
        if is_dark:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                }
                QTabBar::tab {
                    background: #333;
                    color: #fff;
                    padding: 8px 20px;
                    border: 1px solid #444;
                }
                QTabBar::tab:selected {
                    background: #444;
                }
                QMenuBar {
                    background-color: #333;
                    color: #fff;
                }
                QMenuBar::item:selected {
                    background-color: #444;
                }
            """)
        else:
            self.setStyleSheet("")
        
        # Update theme in frames
        self.modern_frame.update_theme(is_dark)
        self.urban_frame.update_theme(is_dark)
        self.rankings_frame.update_theme(is_dark) 