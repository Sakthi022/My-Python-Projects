import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame.mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import io

# Initialize tkinter
root = tk.Tk()
root.title("Audio Player")

# Initialize mixer
pygame.mixer.init()

# Function to play audio
def play_audio():
    global paused, current_file
    if paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.load(current_file)
        pygame.mixer.music.play()
    paused = False

# Function to pause audio
def pause_audio():
    global paused
    pygame.mixer.music.pause()
    paused = True

# Function to toggle play/pause
def toggle_audio():
    if paused:
        play_button.config(text="Pause")
    else:
        pause_button.config(text="Play")
    if current_file:
        play_audio()

# Function to open file
def open_file():
    global current_file, audio_length
    current_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if current_file:
        artist, album, album_art = get_metadata(current_file)
        display_metadata(artist, album, album_art)
        play_audio()
        audio_length = MP3(current_file).info.length
        progress_bar.config(to=audio_length)

# Function to get metadata
def get_metadata(file_path):
    audio = MP3(file_path, ID3=ID3)
    artist = audio.get("TPE1", "Unknown Artist").text[0]
    album = audio.get("TALB", "Unknown Album").text[0]
    album_art = None

    if "APIC:" in audio.tags:
        for tag in audio.tags.getall("APIC"):
            album_art = ImageTk.PhotoImage(Image.open(io.BytesIO(tag.data)))

    return artist, album, album_art

# Function to display metadata
def display_metadata(artist, album, album_art):
    artist_label.config(text="Artist: " + artist)
    album_label.config(text="Album: " + album)
    if album_art:
        album_art_label.config(image=album_art)
        album_art_label.image = album_art

# Function to update progress bar
def update_progress():
    current_time = pygame.mixer.music.get_pos() / 1000
    progress_bar.set(current_time)
    if not paused:
        root.after(1000, update_progress)

# Function to handle seeking
def seek_audio(value):
    pygame.mixer.music.set_pos(int(value))

# Initialize variables
paused = False
current_file = ""
audio_length = 0

# Create GUI elements
open_button = tk.Button(root, text="Open", command=open_file)
play_button = tk.Button(root, text="Play", command=toggle_audio)
pause_button = tk.Button(root, text="Pause", command=pause_audio)
artist_label = tk.Label(root, text="Artist: ")
album_label = tk.Label(root, text="Album: ")
album_art_label = tk.Label(root)
progress_bar = tk.Scale(root, from_=0, to=0, orient=tk.HORIZONTAL, length=300, command=seek_audio)

# Place GUI elements
open_button.pack()
play_button.pack()
pause_button.pack()
artist_label.pack()
album_label.pack()
album_art_label.pack()
progress_bar.pack()

# Start progress bar updater
update_progress()

# Start tkinter main loop
root.mainloop()
