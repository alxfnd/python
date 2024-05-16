import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

def load_csv():
    filepath = file_entry.get()
    try:
        df = pd.read_csv(filepath)
        global original_df  # Store original DataFrame for filtering
        original_df = df.copy()
        update_treeview(df)

    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        # Clear treeview
        for item in tree.get_children():
            tree.delete(item)
        # Display error message
        tree.insert("", tk.END, values=[str(e)])


def filter_treeview():
    query = filter_entry.get().lower()
    if not query:
        update_treeview(original_df)  # If empty, show all data
        return

    filtered_df = original_df[original_df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
    update_treeview(filtered_df)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def update_treeview(df):
    # Clear existing data
    for item in tree.get_children():
        tree.delete(item)

    # Set up columns (left-aligned and dynamic width)
    tree["columns"] = list(df.columns)
    total_width = 0  
    for col in df.columns:
        tree.heading(col, text=col, anchor="w", command=lambda _col=col: treeview_sort_column(tree, _col, False))  
        col_width = max(df[col].astype(str).map(len).max(), len(col)) * 10  # Adjust scaling factor as needed
        tree.column(col, width=col_width, anchor="w")  # Left align content
        total_width += col_width

    # Insert data
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Create main window
root = tk.Tk()
root.title("CSV Viewer")

# File entry
file_entry = ttk.Entry(root, width=50)
file_entry.pack(padx=10, pady=10)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=load_csv)
submit_button.pack(pady=5)

# Filter entry
filter_entry = ttk.Entry(root, width=50)
filter_entry.pack(padx=10, pady=(0, 10))  # Add some top padding
filter_entry.bind("<KeyRelease>", lambda event: filter_treeview())  # Filter on each key press

# Treeview with scrollbars
tree_frame = ttk.Frame(root)
tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(tree_frame, show="headings")  # Show headings only
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.config(yscrollcommand=scrollbar_y.set)

scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
scrollbar_x.pack(fill=tk.X)
tree.config(xscrollcommand=scrollbar_x.set)

#
#
#
#
#
#
#
#
#
#
#
#
#
# PART 2

from tkinter import messagebox

output_data = None

user_data = {"name": "John Doe", "email": "johndoe@example.com","eyes":"blue"} 

def open_info_dialog(parent_window=root, data=user_data):
    """
    Creates and displays a dialog window to show information from the main app.
    
    Args:
        parent_window: The main application window (Tk object).
        data: The information (dictionary) to display in the dialog.
    """
    
    global output_data

    dialog = tk.Toplevel(parent_window)
    dialog.title("Information")
    dialog.transient(parent_window)

    entry_vars = {}  # Dictionary to hold Entry widget variables

    for key, value in data.items():
        ttk.Label(dialog, text=key + ":").grid(row=list(data.keys()).index(key), column=0, sticky="w")
        var = tk.StringVar(value=value)
        entry = ttk.Entry(dialog, textvariable=var)
        entry.grid(row=list(data.keys()).index(key), column=1, sticky="ew", padx=5, pady=5)  # Added padding
        entry_vars[key] = var

    # Configure column to expand
    dialog.columnconfigure(1, weight=1) 

    ttk.Separator(dialog, orient="horizontal").grid(row=len(data), columnspan=2, sticky="ew", pady=10)

    button_frame = ttk.Frame(dialog)
    button_frame.grid(row=len(data) + 1, columnspan=2, pady=10)

    back_button = ttk.Button(button_frame, text="Cancel", command=lambda: handle_cancel(dialog))
    back_button.pack(side="left", padx=5)

    ok_button = ttk.Button(button_frame, text="OK", command=lambda: handle_ok(dialog, entry_vars))
    ok_button.pack(side="right", padx=5)

    dialog.protocol("WM_DELETE_WINDOW", lambda: handle_cancel(dialog))

def handle_ok(dialog, entry_vars):
    global output_data
    
    output_data = {key: var.get() for key, var in entry_vars.items()}  # Get values from Entry widgets
    print("Output data:", output_data)
    dialog.destroy()


def handle_cancel(dialog):
    global output_data
    output_data = None  # Clear the global variable
    print("Output data cleared.")  # Optional: Print a message to the console
    dialog.destroy()

info_button = tk.Button(root, text="Show Info", command=open_info_dialog)
info_button.pack()

root.mainloop()