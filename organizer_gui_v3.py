import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil

# -------------------------
# App Settings
# -------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Automated File Organizer")
app.geometry("900x650")

selected_folder = ""

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "ZIP Files": [".zip", ".rar", ".7z"],
    "Applications": [".exe", ".msi"]
}

# -------------------------
# Select Folder
# -------------------------
def select_folder():
    global selected_folder

    folder = filedialog.askdirectory()

    if folder:
        selected_folder = folder
        folder_label.configure(text=folder)
        progress.set(0)
        textbox.delete("1.0", "end")
        textbox.insert("end", "Folder Selected Successfully!\n")

# -------------------------
# Organize Files
# -------------------------
def organize_files():
    global selected_folder

    if selected_folder == "":
        messagebox.showwarning(
            "Warning",
            "Please select a folder first!"
        )
        return

    textbox.delete("1.0", "end")

    stats = {
        "Images": 0,
        "Documents": 0,
        "Audio": 0,
        "Videos": 0,
        "ZIP Files": 0,
        "Applications": 0,
        "Others": 0
    }

    count = 0

    files = os.listdir(selected_folder)

    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo(
            "Information",
            "Selected folder is empty."
        )
        return

    processed = 0

    for file in files:

        file_path = os.path.join(selected_folder, file)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for folder_name, extensions in file_types.items():

            if extension in extensions:

                destination = os.path.join(
                    selected_folder,
                    folder_name
                )

                os.makedirs(destination, exist_ok=True)

                shutil.move(
                    file_path,
                    os.path.join(destination, file)
                )

                textbox.insert(
                    "end",
                    f"✅ {file} ➜ {folder_name}\n"
                )

                stats[folder_name] += 1
                count += 1
                moved = True
                break

        if not moved:

            destination = os.path.join(
                selected_folder,
                "Others"
            )

            os.makedirs(destination, exist_ok=True)

            shutil.move(
                file_path,
                os.path.join(destination, file)
            )

            textbox.insert(
                "end",
                f"✅ {file} ➜ Others\n"
            )

            stats["Others"] += 1
            count += 1

        processed += 1

        progress.set(processed / total_files)
        app.update()