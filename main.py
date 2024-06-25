from customtkinter import *
import tkinter as tk
import shutil
import os
import zipfile
import tempfile
import json

main = CTk()
main.geometry("1000x600")
main._set_appearance_mode("dark")
main.title("Skin Swapper")
font = ("Arial", 12, "italic")

def save_settings():
    settings = {
        "wt_loc": buttons.wt_loc.get(),
        "zip_loc": buttons.zip_loc.get(),
        "backup": buttons.backup.get(),
        "m_switch_state": buttons.m_switch_state
    }
    try:
        with open("settings.json", "w") as f:
            json.dump(settings, f)
        buttons.message_label.configure(text="Settings saved.", text_color="#00ff00")
    except Exception as e:
        buttons.message_label.configure(text=f"Error saving settings: {e}", text_color="#ff0000")

def load_settings():
   if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)

                buttons.wt_loc.delete(0, tk.END)
                buttons.wt_loc.insert(0, settings.get("wt_loc", ""))

                buttons.zip_loc.delete(0, tk.END)
                buttons.zip_loc.insert(0, settings.get("zip_loc", ""))

                buttons.backup.delete(0, tk.END)
                buttons.backup.insert(0, settings.get("backup", ""))

                buttons.m_switch_state = settings.get("m_switch_state", False)
                if buttons.m_switch_state:
                    buttons.m_switch.select()
                else:
                    buttons.m_switch.deselect()

                buttons.toggle_all_widgets()

                buttons.message_label.configure(text="Settings loaded.", text_color="#00ff00")
        except Exception as e:
            buttons.message_label.configure(text=f"Error loading settings: {e}", text_color="#ff0000")

def on_closing():
    save_settings()
    main.destroy()

main.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event



# Label class
class Label:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Define text color
        text_color = "#545353"

        # Add the label
        label_text = "Welcome to the War Thunder Skin Swapper"
        label1 = CTkLabel(self.parent, text=label_text, font=font, text_color=text_color)
        label1.place(x=10, y=7)  # Position top left

        label1_width = label1.winfo_reqwidth()

        # Position version number
        label2_x = 950 - label1_width - 20
        label2 = CTkLabel(self.parent, text="Version 1.2", font=font, text_color=text_color)
        label2.place(x=label2_x, y=7)  # Position top right

        # Horizontal separator line
        separator_frame = CTkFrame(self.parent, width=980, height=2, bg_color="#545353")
        separator_frame.pack(anchor=NW, padx=10)
        separator_frame.place(x=10, y=37)

        # Vertical separator line
        separator_vertical = CTkFrame(self.parent, width=2, height=500, bg_color="#545353")
        separator_vertical.pack(anchor=NW, padx=10)
        separator_vertical.place(x=520, y=47)

Label = Label(main)

# Buttons class
class Buttons:
    def __init__(self, parent):
        self.parent = parent
        self.m_switch_state = False
        self.setup_ui()

    def create_help_popup(self):
        # Create the popup window
        popup = CTkToplevel(self.parent)
        popup.geometry("500x500")
        popup.title("How to use")
        
        # Add a label with instructions
        help_text = ("How to use this Skin Swapper prorgramme:\n\n"
                 "1. Enable the Master Switch to activate input fields and buttons.\n"
                 "2. Enter the Exact skin folder path of the desired vehicle .\n"
                 "3. Save the current skin if you want to, it will create backup of the files, because the \n" "     program WILL!!! overwrite them.\n"
                 "4. Enter the location of the downloaded .zip files of the skins (copying from the address \n" "    line won't work if you want to set the Downloads folder as your .zip file location folder ).\n"
                 "5. Click 'Load Zip Files' to list available zip files in the directory.\n"
                 "6. Select a zip file from the list and click 'Load the new skin'. \n"
                 "7. Go in game, and refresh the skin template in customization tab. \n\n"
                 "How to use the reverse changes function: \n"
                 "First of all, this will only work once you create a backup of the selected folder in the \n"
                 "listbox, by using the 'save current' button, then you can use that folder \n"
                 "as a backup by selecting it in the listbox on the right side of the window  \n"
                 "make sure to use the same path as in the input field on the left, because the save \n"
                 "current button creates a backup folder in that directory, and then when you selected the \n "
                 "desired folder click the reverse changes button. \n")

        label = CTkLabel(popup, text=help_text, font=font, text_color="#ffffff", wraplength=480, justify="left")
        label.pack(pady=20, padx=10)
        
        # Add a close button
        button_close = CTkButton(popup, text="Close", command=popup.destroy, fg_color="#bd8e0d", hover_color="#bd8e0d")
        button_close.pack(pady=10)

        popup.focus_set()
        popup.grab_set()
        popup.transient(self.parent)


    def setup_ui(self):
        # Master switch
        self.m_switch = CTkSwitch(self.parent, text="Master Switch", command=self.toggle_all_widgets, progress_color="#bd8e0d")
        self.m_switch.place(x=10, y=50)

        text_color = "#ffffff"

        # Help button

        self.help = CTkButton(self.parent,state="normal", text="How to use",command=self.create_help_popup)
        self.help.place(x=150, y=51)
        self.help.configure(height = 3, fg_color="#565a5f")

        # Label for skin path input
        self.wt_loc_label = CTkLabel(self.parent, text="Enter the EXACT path to the UserSkins folder in WT files.", font=font, text_color="#ffffff")
        self.wt_loc_label.place(x=11, y=72)

        # Skin path input field
        self.wt_loc = CTkEntry(self.parent, state="normal", width=500, text_color="#bd8e0d")  # Initially disabled
        self.wt_loc.place(x=10, y=97)

        # Label for zip file path input
        self.zip_label = CTkLabel(self.parent, text="Enter the EXACT directory path containing .zip files:", font=font, text_color="#ffffff")
        self.zip_label.place(x=11, y=330)

        # Zip file path input field
        self.zip_loc = CTkEntry(self.parent, state="normal", width=500, text_color="#bd8e0d")  # Initially disabled
        self.zip_loc.place(x=10, y=352)

        # Button to load zip files
        self.load_zip_button = CTkButton(self.parent, text="Load Zip Files", command=self.load_zip_files, fg_color="#565a5f", state="normal")
        self.load_zip_button.place(x=155, y=390)

        # load backed up files
        self.backup_label = CTkLabel(self.parent, text="Enter the EXACT path where you saved files")
        self.backup_label.place(x=535, y=72)
        self.backup = CTkEntry(self.parent, state="normal", width=400,text_color="#bd8e0d")
        self.backup.place(x=535, y=97)
        
        self.setup_buttons()
        self.setup_message_label()
        self.setup_listbox()  # Setup the Listbox below the button2h label

    def setup_buttons(self):
        # Save current files button
        self.button1 = CTkButton(self.parent, text="Save current files", command=self.save_current, fg_color="#565a5f", state="normal")
        self.button1.place(x=158, y=160)
        self.button1h = CTkLabel(self.parent, text="Save the current skin, the program overwrites existing files!", font=font, text_color="#ffffff")
        self.button1h.place(x=160, y=190)

        # Upload new skin button
        self.button2 = CTkButton(self.parent, text="Load the new skin", command=self.apply_new, fg_color="#565a5f", state="normal")
        self.button2.place(x=155, y=561)
        self.button2h = CTkLabel(self.parent, text="Load the files of the new skin", font=font, text_color="#ffffff")
        self.button2h.place(x=305, y=561)

        self.button3 = CTkButton(self.parent, text="Reverse changes", fg_color="#565a5f", command=self.reverse_changes, state="normal", width=136)
        self.button3.place(x=535, y=365)

        self.button4 = CTkButton(self.parent, text="Load saved files", command=self.load_saved , fg_color="#565a5f", state="normal", height=3, width=136)
        self.button4.place(x=535, y=51)

        self.button5 = CTkButton(self.parent, text="Load Skins folders", command=self.load_skin_folders ,fg_color="#565a5f", state="normal")
        self.button5.place(x=158, y=130)

    def setup_message_label(self):
        # Label for displaying messages
        self.message_label = CTkLabel(self.parent, text="", font=font, text_color="#ffffff")
        self.message_label.place(x=535, y=400)

    def setup_listbox(self):
        # Frame to contain the Listbox and scrollbar
        listbox_frame = CTkFrame(self.parent, width=670, height=150, fg_color="#2a2d2e")
        listbox_frame.place(x=11, y=390)  # Positioned below the button2h label

        # Listbox widget
        self.listbox = tk.Listbox(listbox_frame, bg="#2a2d2e", fg="white", bd=0, highlightthickness=0, selectbackground="#565b5e", exportselection=False)
        self.listbox.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Listbox
        scrollbar = CTkScrollbar(listbox_frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Reverse changes listbox

        # Frame to contain the listbox and the scrollbar
        listbox2_label = CTkLabel(self.parent, text="Select the backup to reverse the changes.", font=font, text_color="#ffffff", padx=0, pady=0)
        listbox2_label.place(x=535, y=130)
        listbox2_frame = CTkFrame(self.parent, width=40, height=150, fg_color="#2a2d2e")
        listbox2_frame.place(x=535, y=160) 

        # Listbox widget
        self.listbox2 = tk.Listbox(listbox2_frame, bg="#2a2d2e", fg="white", bd=0, highlightthickness=0, selectbackground="#565b5e", exportselection=False)
        self.listbox2.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Listbox
        scrollbar2 = CTkScrollbar(listbox2_frame, command=self.listbox2.yview)
        scrollbar2.pack(side="right", fill="y")
        self.listbox2.config(yscrollcommand=scrollbar2.set)

        # Skins folders list 
        listbox3_frame = CTkFrame(self.parent, width=40, height=100, fg_color="#2a2d2e")
        listbox3_frame.place(x=10, y=130) 

        # Listbox widget
        self.listbox3 = tk.Listbox(listbox3_frame, bg="#2a2d2e", fg="white", bd=0, highlightthickness=0, selectbackground="#565b5e", exportselection=False)
        self.listbox3.pack(side="left", fill="both", expand=True)

        # Scrollbar for the Listbox
        scrollbar3 = CTkScrollbar(listbox3_frame, command=self.listbox3.yview)
        scrollbar3.pack(side="right", fill="y")
        self.listbox3.config(yscrollcommand=scrollbar3.set)
    

    def toggle_all_widgets(self):
        self.m_switch_state = self.m_switch.get()  # Get the current state of the switch
    
        # Enable or disable widgets based on master switch state
        state = "normal" if self.m_switch_state else "disabled"
        fg_color = "#bd8e0d" if self.m_switch_state else "#565a5f"
        
        self.wt_loc.configure(state=state, border_color=fg_color)
        self.zip_loc.configure(state=state, border_color=fg_color)
        self.backup.configure(state=state, border_color=fg_color)
        
        self.button1.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.button2.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.load_zip_button.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.help.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.button3.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.button4.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        self.button5.configure(state=state, fg_color=fg_color, hover_color=fg_color)
        
        self.listbox.config(state=state)
        self.listbox2.config(state=state)
        self.listbox3.config(state=state)

        if state == "normal":
            self.wt_loc.configure(text_color="#bd8e0d")
            self.zip_loc.configure(text_color="#bd8e0d")
            self.backup.configure(text_color="#bd8e0d")
        else:
            self.wt_loc.configure(text_color="#565a5f")
            self.zip_loc.configure(text_color="#565a5f")
            self.backup.configure(text_color="#565a5f")

        if state == "normal":
            self.wt_loc.bind("<Key>", lambda event: None)  
            self.zip_loc.bind("<Key>", lambda event: None)  
            self.backup.bind("<Key>", lambda event: None)  
        else:
            self.wt_loc.unbind("<Key>")  
            self.zip_loc.unbind("<Key>")  
            self.backup.unbind("<Key>")


    def load_skin_folders(self):
        wt_path = self.wt_loc.get().strip()
        if not os.path.isdir(wt_path):
            self.message_label.configure(text="Invalid WT skin folder path.", text_color="#ff0000")
            return

        try:
            skin_folders = [f for f in os.listdir(wt_path) if os.path.isdir(os.path.join(wt_path, f))]
            self.listbox3.delete(0, tk.END)
            self.message_label.configure(text="Skin folders loaded.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error loading skin folders: {e}", text_color="#ff0000")


    def get_unique_folder_name(self, base_path):
        counter = 0
        while True:
            folder_name = f"{base_path}_{counter}" if counter else base_path
            if not os.path.exists(folder_name):
                return folder_name
            counter += 1

    def save_current(self):
        selected_skin_index = self.listbox3.curselection()
        if not selected_skin_index:
            self.message_label.configure(text="Please select a skin folder from the list.", text_color="#ff0000")
            return

        folder_name = self.listbox3.get(selected_skin_index)
        folder_path = os.path.join(self.wt_loc.get(), folder_name)
        if not os.path.isdir(folder_path):
            self.message_label.configure(text="Invalid skin folder path.", text_color="#ff0000")
            return

        backup_folder = os.path.join(self.backup.get().strip(), folder_name + "_backup")
        backup_folder = self.get_unique_folder_name(backup_folder)  # Ensure unique backup folder name

        try:
            shutil.copytree(folder_path, backup_folder)
            self.message_label.configure(text=f"Current files saved to {backup_folder}.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error saving current files: {e}", text_color="#ff0000")

    def apply_new(self):
            selected_zip = self.listbox.get(tk.ACTIVE)
            if not selected_zip:
                self.message_label.configure(text="No zip file selected.", text_color="#ff0000")
                return

            selected_skin_index = self.listbox3.curselection()
            if not selected_skin_index:
                self.message_label.configure(text="Please select a skin folder from the list.", text_color="#ff0000")
                return

            folder_name = self.listbox3.get(selected_skin_index)
            skin_path = os.path.join(self.wt_loc.get(), folder_name)

            zip_path = self.zip_loc.get().strip()
            selected_zip_path = os.path.join(zip_path, selected_zip)
            if not os.path.isfile(selected_zip_path):
                self.message_label.configure(text="Invalid selected zip file.", text_color="#ff0000")
                return

            if not os.path.isdir(skin_path):
                self.message_label.configure(text="Invalid UserSkins path.", text_color="#ff0000")
                return

            try:
                # Extract the zip file to a temporary directory
                with tempfile.TemporaryDirectory() as tmpdir:
                    with zipfile.ZipFile(selected_zip_path, 'r') as zip_ref:
                        zip_ref.extractall(tmpdir)

                    extracted_items = os.listdir(tmpdir)

                    # Check for single folder inside the zip
                    if len(extracted_items) == 1 and os.path.isdir(os.path.join(tmpdir, extracted_items[0])):
                        folder_path = os.path.join(tmpdir, extracted_items[0])
                        for item in os.listdir(folder_path):
                            s = os.path.join(folder_path, item)
                            d = os.path.join(skin_path, item)
                            if os.path.isdir(s):
                                shutil.copytree(s, d, dirs_exist_ok=True)
                            else:
                                shutil.copy2(s, d)
                        self.message_label.configure(text=f"Skin {selected_zip} applied successfully.", text_color="#00ff00")
                        return

                    # Check if all extracted items are files
                    elif all(os.path.isfile(os.path.join(tmpdir, item)) for item in extracted_items):
                        for item in extracted_items:
                            s = os.path.join(tmpdir, item)
                            d = os.path.join(skin_path, item)
                            shutil.copy2(s, d)
                        self.message_label.configure(text=f"Skin {selected_zip} applied successfully.", text_color="#00ff00")
                        return

                    # Check for multiple folders inside the zip
                    else:
                        folders_count = sum(os.path.isdir(os.path.join(tmpdir, item)) for item in extracted_items)
                        if folders_count > 1:
                            self.message_label.configure(text="Error: Zip file contains multiple folders.", text_color="#ff0000")
                            return

                        self.message_label.configure(text="Error: Invalid zip file structure.", text_color="#ff0000")
                        return

                # Delete the existing files only after ensuring successful extraction
                for item in os.listdir(skin_path):
                    item_path = os.path.join(skin_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)

            except Exception as e:
                self.message_label.configure(text=f"Error applying new skin: {e}", text_color="#ff0000")

    def reverse_changes(self):
        selected_skin_index = self.listbox3.curselection()
        selected_backup_index = self.listbox2.curselection()

        if not selected_skin_index:
            self.message_label.configure(text="Please select a skin folder from the list.", text_color="#ff0000")
            return

        folder_name = self.listbox3.get(selected_skin_index)
        folder_path = os.path.join(self.wt_loc.get(), folder_name)

        if not selected_backup_index:
            self.message_label.configure(text="Please select a backup folder from the list.", text_color="#ff0000")
            return

        backup_folder_name = self.listbox2.get(selected_backup_index)
        backup_folder_path = os.path.join(self.backup.get().strip(), backup_folder_name)  # Use the provided backup path

        if not os.path.isdir(backup_folder_path):
            self.message_label.configure(text=f"Invalid backup folder: {backup_folder_name}", text_color="#ff0000")
            return

        try:
            # Clear the current folder contents
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

            # Copy files from the backup folder
            for item in os.listdir(backup_folder_path):
                source_item = os.path.join(backup_folder_path, item)
                destination_item = os.path.join(folder_path, item)
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                else:
                    shutil.copy2(source_item, destination_item)

            self.message_label.configure(text=f"Changes reversed using backup '{backup_folder_name}'.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error reversing changes: {e}", text_color="#ff0000")

    def load_zip_files(self):
        zip_dir = self.zip_loc.get().strip()
        if not os.path.isdir(zip_dir):
            self.message_label.configure(text="Invalid zip file directory path.", text_color="#ff0000")
            return

        try:
            zip_files = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]
            self.listbox.delete(0, tk.END)
            for zip_file in zip_files:
                self.listbox.insert(tk.END, zip_file)
            self.message_label.configure(text="Zip files loaded.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error loading zip files: {e}", text_color="#ff0000")

    def load_skin_folders(self):
        wt_path = self.wt_loc.get().strip()
        if not os.path.isdir(wt_path):
            self.message_label.configure(text="Invalid WT skin folder path.", text_color="#ff0000")
            return

        try:
            skin_folders = [f for f in os.listdir(wt_path) if os.path.isdir(os.path.join(wt_path, f)) and not f.endswith('_backup') and '_backup' not in f]
            self.listbox3.delete(0, tk.END)
            for folder in skin_folders:
                self.listbox3.insert(tk.END, folder)
            self.message_label.configure(text="Skin folders loaded.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error loading skin folders: {e}", text_color="#ff0000")

    def load_saved(self):
        backup_path = self.backup.get().strip()
        if not os.path.isdir(backup_path):
            self.message_label.configure(text="Invalid backup folder path.", text_color="#ff0000")
            return

        try:
            saved_files = [f for f in os.listdir(backup_path) if os.path.isdir(os.path.join(backup_path, f)) and f.endswith('_backup') or '_backup_' in f]
            self.listbox2.delete(0, tk.END)
            for file in saved_files:
                self.listbox2.insert(tk.END, file)
            self.message_label.configure(text="Saved files loaded.", text_color="#00ff00")
        except Exception as e:
            self.message_label.configure(text=f"Error loading saved files: {e}", text_color="#ff0000")


# Create an instance of Buttons and run the main event loop
buttons = Buttons(main)
load_settings()
main.protocol("WM_DELETE_WINDOW", lambda: [save_settings(), main.destroy()])  # Replace the existing WM_DELETE_WINDOW handler if any
main.mainloop()
