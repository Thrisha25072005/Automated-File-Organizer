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
        textbox.insert("end", f"Selected Folder:\n{folder}\n\n")
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

    if len(files) == 0:
        messagebox.showinfo(
            "Information",
            "Selected folder is empty."
        )
        return

    total_files = len(files)
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

    textbox.insert("end", "\n")
    textbox.insert("end", "========== Organization Summary ==========\n\n")

    for folder_name, total in stats.items():
        textbox.insert("end", f"{folder_name:<15}: {total}\n")

    textbox.insert("end", "\n")
    textbox.insert("end", f"🎉 Total Files Organized : {count}\n")

    messagebox.showinfo(
        "Success",
        f"{count} files organized successfully!"
    )
# -------------------------
# Open Folder
# -------------------------
def open_folder():

    if selected_folder == "":
        messagebox.showwarning(
            "Warning",
            "Please select a folder first!"
        )
        return

    os.startfile(selected_folder)
# -------------------------
# Title
# -------------------------
title = ctk.CTkLabel(
    app,
    text="📁 Smart Automated File Organizer",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

# -------------------------
# Folder Label
# -------------------------
folder_label = ctk.CTkLabel(
    app,
    text="No Folder Selected",
    width=700,
    font=("Arial", 14)
)
folder_label.pack(pady=10)

# -------------------------
# Buttons
# -------------------------
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

select_btn = ctk.CTkButton(
    button_frame,
    text="📂 Select Folder",
    command=select_folder,
    width=180
)
select_btn.grid(row=0, column=0, padx=10, pady=10)

organize_btn = ctk.CTkButton(
    button_frame,
    text="📦 Organize Files",
    command=organize_files,
    width=180
)
organize_btn.grid(row=0, column=1, padx=10, pady=10)

open_btn = ctk.CTkButton(
    button_frame,
    text="📁 Open Folder",
    command=open_folder,
    width=180
)
open_btn.grid(row=0, column=2, padx=10, pady=10)

# -------------------------
# Progress Bar
# -------------------------
progress = ctk.CTkProgressBar(app, width=700)
progress.pack(pady=15)
progress.set(0)

# -------------------------
# Results Textbox
# -------------------------
textbox = ctk.CTkTextbox(
    app,
    width=760,
    height=250
)
textbox.pack(pady=20)

textbox.insert(
    "end",
    "Welcome to Smart Automated File Organizer\n\n"
)

# -------------------------
# Footer
# -------------------------
footer = ctk.CTkLabel(
    app,
    text="Developed by Thrisha | Python + CustomTkinter",
    text_color="gray"
)
footer.pack(pady=10)

# -------------------------
# Run App
# -------------------------
app.mainloop()