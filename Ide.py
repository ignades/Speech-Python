import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import sys
import traceback
import re

class AtomPythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Atom-like Python IDE")
        self.root.geometry("1200x800")

        # Main container
        self.main_container = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # File Tree Panel
        self.file_tree_frame = tk.Frame(self.main_container, width=250, borderwidth=1, relief=tk.SUNKEN)
        self.main_container.add(self.file_tree_frame)

        # File Tree Title
        self.file_tree_label = tk.Label(self.file_tree_frame, text="Project Files", font=('Arial', 10, 'bold'))
        self.file_tree_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # File Tree
        self.file_tree = ttk.Treeview(self.file_tree_frame)
        self.file_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_tree.bind('<Double-1>', self.open_selected_file)

        # Editor Notebook (Tabs)
        self.editor_notebook = ttk.Notebook(self.main_container)
        self.main_container.add(self.editor_notebook)

        # Bottom Console
        self.console_frame = tk.Frame(root, height=200)
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.console_label = tk.Label(self.console_frame, text="Console Output", font=('Arial', 10, 'bold'))
        self.console_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.console_text = tk.Text(self.console_frame, wrap=tk.WORD, height=10,
                                    font=('Courier', 10))
        self.console_text.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Menu Bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Folder", command=self.open_project_folder)
        self.file_menu.add_command(label="New File", command=self.new_file)
        self.file_menu.add_command(label="Save", command=self.save_current_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Run Menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Current File", command=self.run_current_file)

        # Tracked files and current project
        self.open_files = {}
        self.current_project_path = None

        # Syntax Highlighting Configuration
        self.configure_syntax_highlighting()

    def configure_syntax_highlighting(self):
        """Configure syntax highlighting for code"""
        self.syntax_patterns = {
            'keyword': r'\b(def|class|if|else|elif|for|while|import|from|return|try|except|finally)\b',
            'builtin': r'\b(print|len|range|str|int|float|list|dict|set|tuple)\b',
            'string': r'(\'.*?\'|".*?")',
            'comment': r'#.*$',
            'number': r'\b(\d+|\d*\.\d+)\b'
        }

        self.syntax_colors = {
            'keyword': 'blue',
            'builtin': 'purple',
            'string': 'green',
            'comment': 'gray',
            'number': 'red'
        }

    def open_project_folder(self):
        """Open and display project folder contents"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_project_path = folder_path
            self.populate_file_tree(folder_path)

    def populate_file_tree(self, root_path):
        """Populate file tree with project files"""
        self.file_tree.delete(*self.file_tree.get_children())

        for root, dirs, files in os.walk(root_path):
            relative_path = os.path.relpath(root, root_path)
            parent = '' if relative_path == '.' else self.file_tree.insert('', 'end', text=os.path.basename(root), open=True)

            for file in files:
                if file.endswith(('.py', '.txt', '.md')):
                    full_path = os.path.join(root, file)
                    self.file_tree.insert(parent, 'end', text=file, values=(full_path,))

    def open_selected_file(self, event):
        """Open selected file from file tree"""
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.file_tree.item(selected_item[0])['values']
            if file_path:
                self.open_file(file_path[0])

    def new_file(self):
        """Create a new file tab"""
        new_file_tab = self.create_editor_tab()
        new_file_tab['text_widget'].focus_set()

    def create_editor_tab(self, filename='Untitled'):
        """Create a new editor tab"""
        # Frame to hold text widget and line numbers
        frame = tk.Frame(self.editor_notebook)

        # Line numbers
        line_numbers = tk.Text(frame, width=4, padx=3, pady=3,
                               background='lightgrey', state='disabled',
                               font=('Courier', 12))
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Text widget
        text_widget = tk.Text(frame, wrap=tk.WORD, undo=True,
                              font=('Courier', 12))
        text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Bind events for line numbers and syntax highlighting
        text_widget.bind('<KeyRelease>', lambda e: self.update_line_numbers(text_widget, line_numbers))
        text_widget.bind('<KeyRelease>', self.apply_syntax_highlighting, add='+')

        # Add to notebook
        self.editor_notebook.add(frame, text=filename)
        self.editor_notebook.select(frame)

        return {
            'frame': frame,
            'text_widget': text_widget,
            'line_numbers': line_numbers,
            'filename': filename
        }

    def update_line_numbers(self, text_widget, line_numbers):
        """Update line numbers for a text widget"""
        lines = text_widget.get('1.0', tk.END).split('\n')
        line_count = len(lines)

        line_numbers.config(state='normal')
        line_numbers.delete('1.0', tk.END)

        for i in range(1, line_count + 1):
            line_numbers.insert(tk.END, f'{i}\n')

        line_numbers.config(state='disabled')

    def apply_syntax_highlighting(self, event=None):
        """Apply syntax highlighting to the current text widget"""
        text_widget = event.widget if event else self.get_current_text_widget()

        # Remove existing tags
        for tag_name in self.syntax_colors.values():
            text_widget.tag_remove(tag_name, '1.0', tk.END)

        # Apply syntax highlighting
        content = text_widget.get('1.0', tk.END)
        for syntax_type, pattern in self.syntax_patterns.items():
            for match in re.finditer(pattern, content, re.MULTILINE):
                start = text_widget.index(f'1.0 + {match.start()}c')
                end = text_widget.index(f'1.0 + {match.end()}c')
                text_widget.tag_add(self.syntax_colors[syntax_type], start, end)

        # Configure tag colors
        for color_name, color in self.syntax_colors.items():
            text_widget.tag_config(color, foreground=color)

    def open_file(self, file_path):
        """Open a file in a new tab"""
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            # Create new tab
            tab = self.create_editor_tab(os.path.basename(file_path))
            tab['text_widget'].insert(tk.END, content)

            # Associate file path with tab
            tab['text_widget'].file_path = file_path

            # Apply initial syntax highlighting
            self.apply_syntax_highlighting(type('Event', (), {'widget': tab['text_widget']}))

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def get_current_text_widget(self):
        """Get the currently active text widget"""
        current_tab = self.editor_notebook.select()
        for child in current_tab.winfo_children():
            if isinstance(child, tk.Text) and not child.winfo_name().startswith('!text'):
                return child
        return None

    def save_current_file(self):
        """Save the currently open file"""
        text_widget = self.get_current_text_widget()
        if text_widget:
            file_path = getattr(text_widget, 'file_path', None)

            if not file_path:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".py",
                    filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
                )

            if file_path:
                try:
                    content = text_widget.get('1.0', tk.END)
                    with open(file_path, 'w') as file:
                        file.write(content)

                    # Update tab title
                    text_widget.file_path = file_path
                    tab_index = self.editor_notebook.index(self.editor_notebook.select())
                    self.editor_notebook.tab(tab_index, text=os.path.basename(file_path))

                    messagebox.showinfo("Save", "File saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save file: {e}")

    def run_current_file(self):
        """Run the currently open Python file"""
        # Save current file first
        self.save_current_file()

        text_widget = self.get_current_text_widget()
        if text_widget and hasattr(text_widget, 'file_path'):
            file_path = text_widget.file_path

            # Clear console
            self.console_text.delete('1.0', tk.END)

            # Redirect stdout and stderr
            class OutputRedirector:
                def __init__(self, text_widget):
                    self.text_widget = text_widget

                def write(self, text):
                    self.text_widget.insert(tk.END, text)
                    self.text_widget.see(tk.END)

                def flush(self):
                    pass

            old_stdout = sys.stdout
            old_stderr = sys.stderr

            try:
                sys.stdout = OutputRedirector(self.console_text)
                sys.stderr = OutputRedirector(self.console_text)

                # Execute the script
                with open(file_path, 'r') as file:
                    exec(file.read())

            except Exception as e:
                traceback.print_exc(file=sys.stderr)
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

def main():
    root = tk.Tk()
    ide = AtomPythonIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
