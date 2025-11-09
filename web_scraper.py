import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

# --- Constants ---
DEFAULT_URL = "https://old.reddit.com/"

# --- Core Functions ---

def scrape():
    """Fetches a URL, scrapes text from elements matching a specific tag,
    and displays the results in the GUI's text area."""

    url = url_entry.get().strip()
    tag = tag_entry.get().strip()

    # Simple validation for non-empty fields
    if not url or not tag:
        messagebox.showwarning("Input Required", "Please enter both the Target URL and the HTML Tag.")
        return

    # More robust URL check
    if not url.startswith("http://") and not url.startswith("https://"):
        messagebox.showerror("Invalid URL", "The URL must start with http:// or https://.")
        return

    result_text.config(state=tk.NORMAL) # Enable editing before clearing
    result_text.delete('1.0', tk.END)  # Clear previous text
    result_text.insert(tk.END, f"Scraping {url} for tag <{tag}>...\n", 'info')
    result_text.config(state=tk.DISABLED) # Disable editing

    try:
        # 1. Fetch the content
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        # 2. Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Find all elements
        elements = soup.find_all(tag)

        # 4. Display results
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)

        if elements:
            found_count = 0
            for elem in elements:
                # Get text, strip whitespace, and replace multiple newlines/spaces with a single space
                text = ' '.join(elem.get_text(strip=True).split())
                if text:
                    # Apply tag styling for emphasis
                    result_text.insert(tk.END, f"[{tag.upper()}]: ", 'tag_label')
                    result_text.insert(tk.END, f"{text}\n\n", 'result_text')
                    found_count += 1

            if found_count == 0:
                result_text.insert(tk.END, f"No *non-empty* text found for tag <{tag}> in the elements collected.", 'warning')
            else:
                result_text.insert(tk.END, f"--- Scrape Complete: Found {found_count} element(s) with content. ---\n", 'success')
        else:
            result_text.insert(tk.END, f"No elements found for tag <{tag}>.", 'warning')

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Could not connect or fetch data: {e}")
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"ERROR: Network or HTTP issue. Check the URL and connection.\n{e}", 'error')
    except Exception as e:
        messagebox.showerror("Scraping Error", f"An unexpected error occurred: {e}")
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, f"ERROR: An unexpected error occurred.\n{e}", 'error')
    finally:
        result_text.config(state=tk.DISABLED)


def clear_fields():
    """Clears all input fields and resets the URL to the default value."""
    # Clear and set default URL
    url_entry.delete(0, tk.END)
    url_entry.insert(0, DEFAULT_URL)

    # Clear the tag entry
    tag_entry.delete(0, tk.END)

    # Clear the result area
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, f"Input fields refreshed. Default URL set to: {DEFAULT_URL}\nReady to scrape!", 'info')
    result_text.config(state=tk.DISABLED)


# --- GUI Setup ---

root = tk.Tk()
root.title("Presentation-Ready Web Scraper (Modern Light Theme)")
root.geometry("850x850")
root.config(bg='#F8F8F8') # Very light background

# Define Styles using ttk
style = ttk.Style()
style.theme_use('clam')

# Configure General Styles
style.configure('TFrame', background='#F8F8F8')

# Configure Labels for light theme, using a clean system font
style.configure('TLabel', background='#F8F8F8', foreground='#333333', font=('Arial', 12))
style.configure('Title.TLabel', font=('Arial', 14, 'bold'))

# Configure Entry Fields - slightly lighter border/background
style.configure('TEntry', font=('Arial', 11), padding=5, fieldbackground='#FFFFFF')

# Define Custom Button Styles for a flatter, modern look
# Primary Button Style (Blue)
style.configure('Primary.TButton',
                font=('Arial', 12, 'bold'),
                background='#007BFF', foreground='#FFFFFF',
                borderwidth=0, relief="flat", padding=[20, 10])

style.map('Primary.TButton',
          foreground=[('active', 'white'), ('!disabled', 'white')],
          background=[('active', '#0056b3'), ('pressed', '#004085')])

# Secondary Button Style (Orange)
style.configure('Secondary.TButton',
                font=('Arial', 12, 'bold'),
                background='#FF6F00', foreground='#FFFFFF',
                borderwidth=0, relief="flat", padding=[20, 10])

style.map('Secondary.TButton',
          foreground=[('active', 'white'), ('!disabled', 'white')],
          background=[('active', '#CC5900'), ('pressed', '#994500')])


# Configure Frame for inputs
input_frame = ttk.Frame(root, padding="20 20 20 10")
input_frame.pack(pady=15, padx=20, fill='x')

# --- Input Widgets ---

# URL Widgets
ttk.Label(input_frame, text="Target URL:", style='TLabel').grid(row=0, column=0, padx=10, pady=5, sticky='w')
url_entry = ttk.Entry(input_frame, width=80)
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew', columnspan=2)
url_entry.insert(0, DEFAULT_URL)

# Tag Widgets
ttk.Label(input_frame, text="HTML Tag (e.g., h1, p):", style='TLabel').grid(row=1, column=0, padx=10, pady=5, sticky='w')
tag_entry = ttk.Entry(input_frame, width=20)
tag_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Configure grid weight for better resizing
input_frame.grid_columnconfigure(1, weight=1)

# --- Button Frame ---
button_frame = ttk.Frame(root, padding="0 10 0 10")
button_frame.pack(pady=10, padx=20, fill='x')

# Scrape Button - Primary Action Blue (Now ttk.Button)
scrape_btn = ttk.Button(button_frame, text="🚀 SCRAPE CONTENT", command=scrape, style='Primary.TButton')
scrape_btn.pack(side=tk.LEFT, padx=10, expand=True, fill='x')

# Refresh Button - Secondary Action Orange (Now ttk.Button)
refresh_btn = ttk.Button(button_frame, text="🔄 REFRESH INPUTS", command=clear_fields, style='Secondary.TButton')
refresh_btn.pack(side=tk.RIGHT, padx=10, expand=True, fill='x')


# --- Results Area ---
ttk.Label(root, text="Scraping Results:", style='Title.TLabel').pack(pady=(10, 2), padx=20, fill='x')

# ScrolledText for light theme (simulating a code/log window)
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=30,
                                        font=('Courier New', 10), bg='#FFFFFF', fg='#333333',
                                        insertbackground='black', relief=tk.GROOVE, bd=1, padx=10, pady=10)
result_text.pack(pady=10, padx=20, fill='both', expand=True)

# Define Tags for styled output (adjusted for light background)
result_text.tag_config('info', foreground='#007BFF', font=('Courier New', 10, 'italic'))
result_text.tag_config('success', foreground='#28A745', font=('Courier New', 10, 'bold'))
result_text.tag_config('warning', foreground='#FF6F00', font=('Courier New', 10, 'bold'))
result_text.tag_config('error', foreground='#DC3545', font=('Courier New', 10, 'bold'))
result_text.tag_config('tag_label', foreground='#6C757D', font=('Courier New', 10, 'bold')) # Dark gray for contrast
result_text.tag_config('result_text', foreground='#333333', font=('Courier New', 10)) # Main text

# Initial text setup
result_text.insert(tk.END, f"Welcome to the Advanced Scraper. Default URL set to: {DEFAULT_URL}\nPress 'Scrape' to begin!", 'info')
result_text.config(state=tk.DISABLED) # Prevent user editing of results


# --- Main Loop ---
if __name__ == "__main__":
    # Ensure initial state for light theme compatibility
    try:
        # Attempt to load a modern theme like 'azure' and set to light mode
        root.tk.call('source', 'azure.tcl')
        root.tk.call("set_theme", "light")
    except:
        # Fallback if tcl theme is not available, using custom styles defined above
        pass
    root.mainloop()
