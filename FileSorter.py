import os
import shutil
import logging
import tkinter as tk
from tkinter import Tk, Label, Button, Entry, filedialog

# Configure logging to record file movements
logging.basicConfig(filename='file_sorter.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class FileSorterApp:
    def __init__(self, master):
        self.master = master
        master.title("File Sorter")  # Set the window title

         # Label with copyright notice
        self.copyright_label = tk.Label(master, text="© 2024 Faisal Al Busaidi Product line. All Rights Reserved.", fg="green")
        self.copyright_label.pack(side=tk.BOTTOM, pady=10)

        # Label to prompt user to select a directory
        self.label = Label(master, text="Select the directory to sort:")
        self.label.pack()

        # Button to browse and select the directory
        self.browse_button = Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        # Entries for custom folder names
        self.folder_entries = {}
        self.default_file_types = ['jpg', 'jpeg', 'png', 'pdf', 'txt', 'mp3', 'mp4']
        self.default_folder_names = {
            'jpg': 'Downloaded Images',
            'jpeg': 'Downloaded Images',
            'png': 'Downloaded Images',
            'pdf': 'Downloaded PDFs',
            'txt': 'Downloaded TextFiles',
            'mp3': 'Downloaded Sounds',
            'mp4': 'Downloaded Videos'
        }

        for file_type in self.default_file_types:
            self.add_folder_entry(file_type)

        # Button to start sorting files
        self.sort_button = Button(master, text="Sort Files", command=self.sort_files)
        self.sort_button.pack()

        # Button to reset folder names to default
        self.reset_button = Button(master, text="Reset Folder Names to Default", command=self.reset_to_default)
        self.reset_button.pack()

        # Button to backup sorted files
        self.backup_button = Button(master, text="Backup Files", command=self.backup_files)
        self.backup_button.pack()

        # Button to restore files from backup
        self.restore_button = Button(master, text="Restore Backed Files", command=self.restore_files)
        self.restore_button.pack()

        # Variable to store the selected directory path
        self.selected_dir = ""

    def add_folder_entry(self, file_type):
        # Add an entry for each file type to allow customization of folder names
        label = Label(self.master, text=f"Folder name for .{file_type} files:")
        label.pack()
        entry = Entry(self.master)
        entry.pack()
        entry.insert(0, self.default_folder_names[file_type])  # Set default folder name
        self.folder_entries[file_type] = entry

    def browse_directory(self):
        # Open a dialog to select a directory and update the label with the selected path
        self.selected_dir = filedialog.askdirectory()
        self.label.config(text=f"Selected Directory: {self.selected_dir}")

    def sort_files(self):
       # Check if a directory has been selected
        if self.selected_dir:
            # Check if directory is already sorted
            if self.is_directory_sorted(self.selected_dir):
                self.label.config(text="Directory is already sorted!")
                return

            # Perform sorting if directory is selected and not already sorted
            self.perform_sorting(self.selected_dir)
            self.label.config(text="Files sorted successfully!")
        else:
            # Prompt user to select a directory if none is selected
            self.label.config(text="Please select a directory first.")

    def perform_sorting(self, download_dir):
        # Define a dictionary to map file extensions to custom or default folder names
        file_types = {file_type: self.folder_entries[file_type].get() for file_type in self.default_file_types}

        # Create a backup directory
        backup_dir = os.path.join(download_dir, 'Backup')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Iterate over all files in the selected directory
        for filename in os.listdir(download_dir):
            # Get the full file path
            file_path = os.path.join(download_dir, filename)

            # Skip if it's a directory
            if os.path.isdir(file_path):
                continue

            # Extract the file extension
            file_extension = filename.split('.')[-1].lower()

            # Check if the file extension is in the predefined dictionary
            if file_extension in file_types:
                # Determine the target folder based on the file extension
                target_folder = os.path.join(download_dir, file_types[file_extension])

                # Create the target folder if it doesn't exist
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                # Define the destination path for the file
                destination = os.path.join(target_folder, filename)

                # Copy the file to the backup directory before moving
                backup_path = os.path.join(backup_dir, filename)
                shutil.copy2(file_path, backup_path)

                # Move the file to the target folder
                shutil.move(file_path, destination)

                # Log the file movement
                logging.info(f'Moved {filename} to {target_folder}')
                print(f'Moved {filename} to {target_folder}')

    def backup_files(self):
        # Backup sorted files if the selected directory is sorted
        if self.selected_dir:
            # Define the backup directory
            backup_dir = os.path.join(self.selected_dir, 'Backup')

            # Create the backup directory if it doesn't exist
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Copy all files from the selected directory to the backup directory
            for filename in os.listdir(self.selected_dir):
                file_path = os.path.join(self.selected_dir, filename)
                if os.path.isdir(file_path) and filename != 'Backup':
                    continue
                backup_path = os.path.join(backup_dir, filename)
                shutil.copy2(file_path, backup_path)

            self.label.config(text="Backup completed successfully!")
        else:
            self.label.config(text="Please select a directory first.")

    def restore_files(self):
        # Restore files from the backup directory to the selected directory
        if self.selected_dir:
            backup_dir = os.path.join(self.selected_dir, 'Backup')
            if not os.path.exists(backup_dir):
                self.label.config(text="No backup found.")
                return

            # Move all files from the backup directory to the selected directory
            for filename in os.listdir(backup_dir):
                backup_path = os.path.join(backup_dir, filename)
                original_path = os.path.join(self.selected_dir, filename)
                shutil.move(backup_path, original_path)

            self.label.config(text="Files restored successfully!")
        else:
            self.label.config(text="Please select a directory first.")

    def reset_to_default(self):
        # Reset folder names to default values
        for file_type in self.default_file_types:
            self.folder_entries[file_type].delete(0, 'end')
            self.folder_entries[file_type].insert(0, self.default_folder_names[file_type])
    
    def is_directory_sorted(self, directory):
        # Check if all files are already in their respective folders
        file_types = {file_type: self.folder_entries[file_type].get() for file_type in self.default_file_types}
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                continue
            file_extension = filename.split('.')[-1].lower()
            if file_extension in file_types:
                target_folder = os.path.join(directory, file_types[file_extension])
                if not os.path.exists(target_folder):
                    return False
                if not filename in os.listdir(target_folder):
                    return False
        return True

if __name__ == "__main__":
    # Initialize and run the Tkinter GUI
    root = Tk()
    my_gui = FileSorterApp(root)
    root.mainloop()
