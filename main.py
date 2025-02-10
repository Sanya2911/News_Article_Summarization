import tkinter as tk
from tkinter import filedialog, messagebox
import nltk
from textblob import TextBlob
from newspaper import Article
import pyttsx3
import thread

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
stop_narration = False
paused = False

#Toggle light and dark mode
def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    colors = {'bg': '#333' if dark_mode else '#fff', 'fg': '#fff' if dark_mode else '#000', 'box': '#555' if dark_mode else '#ddd'}
    root.config(bg=colors['bg'])
    for widget in widgets:
        widget.config(bg=colors['bg'], fg=colors['fg'])
    for box in text_boxes:
        box.config(bg=colors['box'], fg=colors['fg'])


#summarize function
def summarize():
    url = utext.get('1.0', "end").strip()
    if not url:
        messagebox.showwarning("Warning", "Please enter a URL")
        return
    
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    
    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')
    
    title.delete('1.0', 'end')
    title.insert('1.0', article.title)
    
    author.delete('1.0', 'end')
    author.insert('1.0', ', '.join(article.authors))
    
    publication.delete('1.0', 'end')
    publication.insert('1.0', str(article.publish_date))
    
    summary.delete('1.0', 'end')
    summary.insert('1.0', article.summary)
    
    analysis = TextBlob(article.text)
    sentiment.delete('1.0', 'end')
    sentiment.insert('1.0', f'Polarity: {analysis.polarity}, Sentiment: {"Positive" if analysis.polarity > 0 else "Negative" if analysis.polarity < 0 else "Neutral"}')
    
    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')

#download the summarized text
def save_summary():
    text = f"Title: {title.get('1.0', 'end').strip()}\n" \
           f"Author: {author.get('1.0', 'end').strip()}\n" \
           f"Publication Date: {publication.get('1.0', 'end').strip()}\n" \
           f"Summary: {summary.get('1.0', 'end').strip()}\n" \
           f"Sentiment: {sentiment.get('1.0', 'end').strip()}\n"
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        messagebox.showinfo("Success", "Summary saved successfully!")

def clear_fields():
    for box in text_boxes:
        box.config(state='normal')
        box.delete('1.0', 'end')
        box.config(state='disabled')
    utext.delete('1.0', 'end')

#text to speech function
def read_aloud():
    global stop_narration, paused
    stop_narration = False
    paused = False
    text = summary.get('1.0', 'end').strip()
    
    def speak():
        global stop_narration
        tts_engine.say(text)
        tts_engine.runAndWait()
    
    if text:
        thread = threading.Thread(target=speak)
        thread.start()

def stop_reading():
    global stop_narration
    stop_narration = True
    tts_engine.stop()

def pause_reading():
    global paused
    if not paused:
        tts_engine.stop()
        paused = True
    else:
        paused = False
        read_aloud()

root = tk.Tk()
root.title("News Summarizer")
root.geometry('1200x700')
root.configure(bg='#fff')

dark_mode = False

# UI Elements
tk.Label(root, text="Enter URL:", bg='#fff', fg='#000').pack()
utext = tk.Text(root, height=1, width=140)
utext.pack()

btn_frame = tk.Frame(root, bg='#fff')
btn_frame.pack()
tk.Button(btn_frame, text="Summarize", command=summarize).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Download", command=save_summary).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_fields).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Toggle Dark Mode", command=toggle_mode).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Read Aloud", command=read_aloud).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Stop Reading", command=stop_reading).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Pause Reading", command=pause_reading).pack(side=tk.LEFT, padx=5)

def create_label(text):
    return tk.Label(root, text=text, bg='#fff', fg='#000')

def create_textbox(height):
    box = tk.Text(root, height=height, width=140, bg='#ddd', fg='#000', state='disabled')
    return box

titles = ["Title", "Author", "Publication Date", "Summary", "Sentiment Analysis"]
text_heights = [1, 1, 1, 20, 1]
widgets = []
text_boxes = []

for i in range(len(titles)):
    label = create_label(titles[i])
    label.pack()
    box = create_textbox(text_heights[i])
    box.pack()
    widgets.append(label)
    text_boxes.append(box)

title, author, publication, summary, sentiment = text_boxes
root.mainloop()