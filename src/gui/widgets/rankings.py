from ..base import BaseFrame
from tkinter import ttk

class RankingsTable(BaseFrame):
    def __init__(self, parent, headers, **kwargs):
        super().__init__(parent, **kwargs)
        self.headers = headers
        self.setup_table()
        
    def setup_table(self):
        # Create treeview with consistent styling
        self.tree = self.create_treeview(
            columns=list(self.headers.keys())
        )
        
        # Configure grid lines
        style = ttk.Style()
        style.configure('Custom.Treeview', 
                       rowheight=30,
                       borderwidth=1,
                       relief='solid')
        
        # Configure grid colors
        bg_color = style.lookup('TFrame', 'background')
        fg_color = style.lookup('TFrame', 'foreground')
        style.configure('Custom.Treeview', 
                       background=bg_color,
                       foreground=fg_color,
                       fieldbackground=bg_color,
                       bordercolor=fg_color,  # Grid line color
                       lightcolor=fg_color,   # Highlight color
                       darkcolor=fg_color)    # Shadow color
        
        # Configure headers
        for col, header in self.headers.items():
            self.tree.heading(col, text=header['text'])
            self.tree.column(col, width=header['width'], 
                           anchor=header.get('anchor', 'w'),
                           stretch=header.get('stretch', False))
        
        # Add scrollbar
        scrollbar = self.add_scrollbar(self.tree)
        
        # Pack widgets
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)
        
    def add_header(self, text):
        """Add a section header"""
        return self.tree.insert('', 'end', values=(text, '', ''), 
                              tags=('header',))
                              
    def add_group(self, title, entries):
        """Add a group of entries with title"""
        self.add_header(title)
        self.tree.insert('', 'end', values=tuple(self.headers.keys()),
                        tags=('subheader',))
        
        for rank, entry in enumerate(entries, 1):
            self.tree.insert('', 'end',
                values=(rank, entry.name, f"{entry.score:.1f}"),
                tags=('entry',))
        
        # Add spacing
        self.tree.insert('', 'end', values=('', '', '')) 