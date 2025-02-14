from tkinter import ttk
import ttkbootstrap as ttk

class BaseFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.style = ttk.Style()
        
    def create_treeview(self, columns, show='headings'):
        """Create a consistently styled treeview"""
        tree = ttk.Treeview(self, columns=columns, show=show, selectmode='none')
        
        # Configure base styling
        bg_color = self.style.lookup('TFrame', 'background')
        fg_color = self.style.lookup('TFrame', 'foreground')
        
        # Configure treeview style
        self.style.configure('Custom.Treeview',
            background=bg_color,
            foreground=fg_color,
            fieldbackground=bg_color,
            borderwidth=1,
            relief='solid',
            rowheight=30)
            
        self.style.configure('Custom.Treeview.Heading',
            background=bg_color,
            foreground=fg_color,
            relief='solid',
            borderwidth=1,
            font=('TkDefaultFont', 9, 'bold'))
            
        tree.configure(style='Custom.Treeview')
        return tree
        
    def add_scrollbar(self, tree):
        """Add a scrollbar to a treeview"""
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        return scrollbar 