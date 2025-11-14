import requests
import json
import tkinter as tk
from tkinter import scrolledtext
import webbrowser

# Dictionary to store the URL for each headline's starting index
article_urls = {}


def open_url(event):
    """Opens the URL associated with the clicked text."""
    click_index = text_area.index(tk.CURRENT)

    for start_index, url in article_urls.items():
        title_end_index = text_area.search("\n", start_index, stopindex=tk.END, regexp=False)

        if text_area.compare(click_index, ">=", start_index) and text_area.compare(click_index, "<", title_end_index):
            webbrowser.open_new(url)
            break


# --- NEW FUNCTIONS FOR CURSOR FIX ---
def on_enter(event):
    """Change cursor to hand2 if hovering over a 'title' tag."""
    # tk.CURRENT gets the text index currently under the mouse pointer
    tag_names = text_area.tag_names(tk.CURRENT)
    if "title" in tag_names:
        text_area.config(cursor="hand2")
    else:
        # Set back to the default text cursor
        text_area.config(cursor="arrow")


def on_leave(event):
    """Set cursor back to default when mouse leaves the text area."""
    text_area.config(cursor="arrow")


# ------------------------------------

def fetch_news():
    global article_urls
    query = entry.get().strip()

    if not query:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Please enter a topic to search.\n", "desc")
        return

    #url = (f"https://newsapi.org/v2/everything?q={query}&from=2025-10-04&sortBy=publishedAt&apiKey=b39f734639ba49c498f06705c2bc05fd")
    url = (f"https://newsapi.org/v2/everything?q=apple&from=2025-11-03&to=2025-11-03&sortBy=popularity&apiKey=b39f734639ba49c498f06705c2bc05fd")
    #url = (f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=b39f734639ba49c498f06705c2bc05fd")


    try:
        r = requests.get(url)
        r.raise_for_status()
        news = json.loads(r.text)
    except Exception as e:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Error fetching news: {e}\n", "desc")
        return

    text_area.delete(1.0, tk.END)  # Clear previous results
    article_urls.clear()

    articles = news.get("articles", [])
    if not articles:
        text_area.insert(tk.END, "No articles found.\n", "desc")
        return

    for article in articles:
        title = article.get("title") or "No title available"
        description = article.get("description") or "No description available"
        link_url = article.get("url")

        start_index = text_area.index(tk.END + "-1c")

        text_area.insert(tk.END, title + "\n", "title")
        text_area.insert(tk.END, description + "\n", "desc")
        text_area.insert(tk.END, "-" * 40 + "\n", "line")

        if link_url:
            article_urls[start_index] = link_url


# ---------------- UI Window ---------------- #
root = tk.Tk()
root.title("News App")
root.geometry("600x800")
root.configure(bg="#003277")

label = tk.Label(
    root,
    text="What type of news are you interested in?",
    bg="#4B5D97",
    fg="#ffffff",
    font=("Arial", 14)
)
label.pack(pady=5)

entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 14),
    bg="#2e2e3e",
    fg="#ffffff",
    insertbackground="white"
)
entry.pack(pady=5)
entry.insert(0, "tesla")

btn = tk.Button(
    root,
    text="Get News",
    command=fetch_news,
    bg="#ff9800",
    fg="#ffffff",
    font=("Arial", 14),
    activebackground="#ffb74d"
)
btn.pack(pady=5)

text_area = scrolledtext.ScrolledText(
    root,
    width=70,
    height=25,
    bg="#2e2e3e",
    fg="#ffffff",
    font=("Arial", 12)
)
text_area.pack(pady=10)

# FIX APPLIED HERE: Removed 'cursor="hand2"'
text_area.tag_config("title", foreground="#00ffea", font=("Arial", 14, "bold"))
text_area.tag_config("desc", foreground="#ffffff")
text_area.tag_config("line", foreground="#ff9800")

# Bind the mouse movement (hover) to manually manage the cursor
text_area.bind("<Motion>", on_enter)

# Bind a click event to the "title" tag to open the URL
text_area.tag_bind("title", "<Button-1>", open_url)

root.mainloop()