import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import threading
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard History Manager")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configuration
        self.max_history = 50
        self.poll_interval = 1.0  # seconds
        self.history: List[Dict] = []
        self.last_clipboard = ""
        self.is_monitoring = False
        
        # Load existing history
        self.load_history()
        
        # Setup UI
        self.setup_ui()
        
        # Start clipboard monitoring
        self.start_monitoring()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title and controls
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(title_frame, text="📋 Clipboard History Manager", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Control buttons
        control_frame = ttk.Frame(title_frame)
        control_frame.pack(side=tk.RIGHT)
        
        self.monitor_btn = ttk.Button(control_frame, text="⏸️ Pause", 
                                     command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="🗑️ Clear All", 
                  command=self.clear_all_history).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="⚙️ Settings", 
                  command=self.show_settings).pack(side=tk.LEFT)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_history)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # History list
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for history
        columns = ('Time', 'Content', 'Type')
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.history_tree.heading('Time', text='Time')
        self.history_tree.heading('Content', text='Content')
        self.history_tree.heading('Type', text='Type')
        
        self.history_tree.column('Time', width=120, minwidth=100)
        self.history_tree.column('Content', width=300, minwidth=200)
        self.history_tree.column('Type', width=80, minwidth=60)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        self.history_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind events
        self.history_tree.bind('<Double-1>', self.copy_selected)
        self.history_tree.bind('<Return>', self.copy_selected)
        self.history_tree.bind('<Delete>', self.delete_selected)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready - Monitoring clipboard...")
        self.status_label.pack(side=tk.LEFT)
        
        # Right-click context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy to clipboard", command=self.copy_to_clipboard)
        
        self.history_tree.bind('<Button-3>', self.show_context_menu)
        
        # Populate initial history
        self.refresh_history_display()
        
    def start_monitoring(self):
        """Start clipboard monitoring in a separate thread"""
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.monitor_thread.start()
        
    def monitor_clipboard(self):
        """Monitor clipboard for changes"""
        while self.is_monitoring:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard and current_clipboard.strip():
                    self.add_to_history(current_clipboard)
                    self.last_clipboard = current_clipboard
                    
                    # Update status on main thread
                    self.root.after(0, self.update_status, f"New item added: {current_clipboard[:50]}...")
                    
            except Exception as e:
                print(f"Error monitoring clipboard: {e}")
                
            time.sleep(self.poll_interval)
    
    def add_to_history(self, content: str):
        """Add new content to history"""
        # Check if content already exists (avoid duplicates)
        if any(item['content'] == content for item in self.history):
            return
            
        # Determine content type
        content_type = self.detect_content_type(content)
        
        # Create history item
        item = {
            'content': content,
            'type': content_type,
            'timestamp': datetime.now().isoformat(),
            'time_display': datetime.now().strftime('%H:%M:%S')
        }
        
        # Add to beginning of list
        self.history.insert(0, item)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
        
        # Save and refresh display
        self.save_history()
        self.root.after(0, self.refresh_history_display)
    
    def detect_content_type(self, content: str) -> str:
        """Detect the type of content"""
        if content.startswith('http://') or content.startswith('https://'):
            return 'URL'
        elif len(content) > 100:
            return 'Text'
        elif content.count('\n') > 2:
            return 'Multi-line'
        elif content.isdigit():
            return 'Number'
        else:
            return 'Text'
    
    def filter_history(self, *args):
        """Filter history based on search term"""
        search_term = self.search_var.get().lower()
        self.refresh_history_display(search_term)
    
    def refresh_history_display(self, filter_term: str = ""):
        """Refresh the history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add filtered items
        for item in self.history:
            if not filter_term or filter_term in item['content'].lower():
                # Truncate content for display
                display_content = item['content']
                if len(display_content) > 50:
                    display_content = display_content[:47] + "..."
                
                self.history_tree.insert('', 'end', values=(
                    item['time_display'],
                    display_content,
                    item['type']
                ))
    
    def copy_selected(self, event=None):
        """Copy selected item to clipboard"""
        selection = self.history_tree.selection()
        if selection:
            item_id = selection[0]
            item_values = self.history_tree.item(item_id, 'values')
            if item_values:
                # Find the full content from history
                time_display = item_values[0]
                content_preview = item_values[1]
                
                # Find matching item in history
                for item in self.history:
                    if (item['time_display'] == time_display and 
                        (item['content'].startswith(content_preview.replace("...", "")) or 
                         content_preview == item['content'])):
                        pyperclip.copy(item['content'])
                        self.update_status(f"Copied: {item['content'][:50]}...")
                        break
    
    def copy_to_clipboard(self):
        """Copy selected item to clipboard (context menu)"""
        self.copy_selected()
    
    def delete_selected(self, event=None):
        """Delete selected item from history"""
        selection = self.history_tree.selection()
        if selection:
            item_id = selection[0]
            item_values = self.history_tree.item(item_id, 'values')
            if item_values:
                time_display = item_values[0]
                content_preview = item_values[1]
                
                # Remove from history
                self.history = [item for item in self.history 
                              if not (item['time_display'] == time_display and 
                                    (item['content'].startswith(content_preview.replace("...", "")) or 
                                     content_preview == item['content']))]
                
                self.save_history()
                self.refresh_history_display()
                self.update_status("Item deleted from history")
    
    def clear_all_history(self):
        """Clear all history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history.clear()
            self.save_history()
            self.refresh_history_display()
            self.update_status("All history cleared")
    
    def toggle_monitoring(self):
        """Toggle clipboard monitoring on/off"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.monitor_btn.config(text="▶️ Resume")
            self.update_status("Monitoring paused")
        else:
            self.is_monitoring = True
            self.monitor_btn.config(text="⏸️ Pause")
            self.start_monitoring()
            self.update_status("Monitoring resumed")
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        ttk.Label(settings_window, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Max history setting
        history_frame = ttk.Frame(settings_window)
        history_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(history_frame, text="Max History Items:").pack(side=tk.LEFT)
        history_var = tk.StringVar(value=str(self.max_history))
        history_entry = ttk.Entry(history_frame, textvariable=history_var, width=10)
        history_entry.pack(side=tk.RIGHT)
        
        # Poll interval setting
        interval_frame = ttk.Frame(settings_window)
        interval_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(interval_frame, text="Poll Interval (seconds):").pack(side=tk.LEFT)
        interval_var = tk.StringVar(value=str(self.poll_interval))
        interval_entry = ttk.Entry(interval_frame, textvariable=interval_var, width=10)
        interval_entry.pack(side=tk.RIGHT)
        
        # Save button
        def save_settings():
            try:
                new_max = int(history_var.get())
                new_interval = float(interval_var.get())
                
                if new_max > 0 and new_interval > 0:
                    self.max_history = new_max
                    self.poll_interval = new_interval
                    
                    # Trim history if needed
                    if len(self.history) > self.max_history:
                        self.history = self.history[:self.max_history]
                        self.save_history()
                        self.refresh_history_display()
                    
                    settings_window.destroy()
                    self.update_status("Settings saved")
                else:
                    messagebox.showerror("Error", "Values must be positive numbers")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        ttk.Button(settings_window, text="Save", command=save_settings).pack(pady=20)
    
    def show_context_menu(self, event):
        """Show right-click context menu"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        # Clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text="Ready - Monitoring clipboard..."))
    
    def save_history(self):
        """Save history to file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            save_data = []
            for item in self.history:
                save_item = item.copy()
                if isinstance(save_item['timestamp'], datetime):
                    save_item['timestamp'] = save_item['timestamp'].isoformat()
                save_data.append(save_item)
            
            with open('clipboard_history.json', 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists('clipboard_history.json'):
                with open('clipboard_history.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert timestamp strings back to datetime objects
                for item in data:
                    if 'timestamp' in item and isinstance(item['timestamp'], str):
                        try:
                            item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                            item['time_display'] = item['timestamp'].strftime('%H:%M:%S')
                        except ValueError:
                            # If timestamp parsing fails, use current time
                            item['timestamp'] = datetime.now()
                            item['time_display'] = datetime.now().strftime('%H:%M:%S')
                
                self.history = data
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []
    
    def on_closing(self):
        """Handle application closing"""
        self.is_monitoring = False
        self.save_history()
        self.root.destroy()

def main():
    # Check if pyperclip is available
    try:
        import pyperclip
    except ImportError:
        messagebox.showerror("Error", "pyperclip module not found. Please install it with: pip install pyperclip")
        return
    
    root = tk.Tk()
    app = ClipboardManager(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
