#!/usr/bin/env python3
"""
PDF Combiner with Automatic Bookmark Generation
A utility to combine multiple PDFs into a single file with automatic bookmark creation.
"""

import os
import sys
import glob
from pathlib import Path
from typing import List, Tuple
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re


def natural_sort_key(path: str):
    name = os.path.basename(path).lower()
    parts = re.split(r"(\d+)", name)
    return [int(p) if p.isdigit() else p for p in parts]


class PDFCombiner:
    def __init__(self):
        self.combined_pdf = None
        self.output_path = None
        
    def find_pdf_files(self, folder_path: str) -> List[str]:
        """Find all PDF files in the specified folder."""
        pdf_pattern = os.path.join(folder_path, "*.pdf")
        pdf_files = glob.glob(pdf_pattern)
        # Sort files naturally (1.pdf, 2.pdf, 10.pdf instead of 1.pdf, 10.pdf, 2.pdf)
        pdf_files.sort(key=natural_sort_key)
        return pdf_files
    
    def get_pdf_info(self, pdf_path: str) -> Tuple[str, int]:
        """Get PDF filename and page count."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                page_count = len(reader.pages)
                filename = os.path.basename(pdf_path)
                return filename, page_count
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return os.path.basename(pdf_path), 0
    
    def combine_pdfs_with_bookmarks(self, pdf_files: List[str], output_path: str) -> bool:
        """Combine PDFs and create bookmarks for each file."""
        try:
            writer = PdfWriter()
            current_page = 0
            
            # Process each PDF file
            for pdf_path in pdf_files:
                if not os.path.exists(pdf_path):
                    print(f"Warning: {pdf_path} not found, skipping...")
                    continue
                    
                try:
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        
                        # Add all pages from this PDF
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        # Create bookmark for this PDF
                        filename = os.path.basename(pdf_path)
                        # Remove .pdf extension for cleaner bookmark names
                        bookmark_name = filename.replace('.pdf', '')
                        
                        # Add bookmark pointing to the first page of this PDF
                        writer.add_outline_item(
                            title=bookmark_name,
                            page_number=current_page
                        )
                        
                        current_page += len(reader.pages)
                        
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
                    return False
            
            # Write the combined PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            self.combined_pdf = output_path
            return True
            
        except Exception as e:
            print(f"Error combining PDFs: {e}")
            return False


class PDFCombinerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Combiner with Bookmarks")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.combiner = PDFCombiner()
        self.selected_folder = ""
        self.pdf_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Combiner with Automatic Bookmarks", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection
        ttk.Label(main_frame, text="Select Folder:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_folder)
        browse_btn.grid(row=1, column=2, pady=5)
        
        # Scan button
        scan_btn = ttk.Button(main_frame, text="Scan for PDFs", command=self.scan_pdfs)
        scan_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # PDF files list
        ttk.Label(main_frame, text="Found PDF Files:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create treeview for PDF files
        columns = ("Filename", "Pages", "Path")
        self.pdf_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.pdf_tree.heading("Filename", text="Filename")
        self.pdf_tree.heading("Pages", text="Pages")
        self.pdf_tree.heading("Path", text="Full Path")
        
        self.pdf_tree.column("Filename", width=200)
        self.pdf_tree.column("Pages", width=80)
        self.pdf_tree.column("Path", width=400)
        
        self.pdf_tree.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.pdf_tree.yview)
        scrollbar.grid(row=4, column=3, sticky=(tk.N, tk.S))
        self.pdf_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights for the treeview
        main_frame.rowconfigure(4, weight=1)
        
        # Selection options
        selection_frame = ttk.LabelFrame(main_frame, text="Selection Options", padding="10")
        selection_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.select_all_var = tk.BooleanVar(value=True)
        select_all_cb = ttk.Checkbutton(selection_frame, text="Select all PDFs", 
                                       variable=self.select_all_var, command=self.toggle_selection)
        select_all_cb.grid(row=0, column=0, sticky=tk.W)
        
        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="10")
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(output_frame, text="Output Filename:").grid(row=0, column=0, sticky=tk.W)
        
        self.output_var = tk.StringVar(value="combined_pdfs.pdf")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=40)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        
        # Combine button
        self.combine_btn = ttk.Button(main_frame, text="Combine PDFs", command=self.combine_pdfs, state="disabled")
        self.combine_btn.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to scan for PDFs")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=9, column=0, columnspan=3, pady=5)
        
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(title="Select folder containing PDFs")
        if folder:
            self.selected_folder = folder
            self.folder_var.set(folder)
            self.status_var.set(f"Selected folder: {folder}")
            
    def scan_pdfs(self):
        """Scan the selected folder for PDF files."""
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select a folder first!")
            return
            
        self.status_var.set("Scanning for PDF files...")
        self.progress.start()
        
        # Clear existing items
        for item in self.pdf_tree.get_children():
            self.pdf_tree.delete(item)
        
        # Find PDF files
        self.pdf_files = self.combiner.find_pdf_files(self.selected_folder)
        
        if not self.pdf_files:
            self.status_var.set("No PDF files found in the selected folder")
            self.progress.stop()
            messagebox.showinfo("No PDFs", "No PDF files were found in the selected folder.")
            return
        
        # Populate treeview
        for pdf_path in self.pdf_files:
            filename, page_count = self.combiner.get_pdf_info(pdf_path)
            self.pdf_tree.insert("", "end", values=(filename, page_count, pdf_path))
        
        self.status_var.set(f"Found {len(self.pdf_files)} PDF files")
        self.progress.stop()
        self.combine_btn.config(state="normal")
        
        # Auto-select all files
        self.select_all_var.set(True)
        self.toggle_selection()
        
    def toggle_selection(self):
        """Toggle selection of all PDF files."""
        if self.select_all_var.get():
            for item in self.pdf_tree.get_children():
                self.pdf_tree.selection_add(item)
        else:
            self.pdf_tree.selection_remove(*self.pdf_tree.selection())
            
    def combine_pdfs(self):
        """Combine the selected PDF files."""
        selected_items = self.pdf_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one PDF file!")
            return
        
        # Get selected PDF paths
        selected_pdfs = []
        for item in selected_items:
            values = self.pdf_tree.item(item, "values")
            selected_pdfs.append(values[2])  # Full path is in column 2
        
        # Get output path
        output_filename = self.output_var.get()
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        output_path = os.path.join(self.selected_folder, output_filename)
        
        # Check if output file already exists
        if os.path.exists(output_path):
            result = messagebox.askyesno("File Exists", 
                                       f"The file {output_filename} already exists. Do you want to overwrite it?")
            if not result:
                return
        
        # Start combining in a separate thread to avoid freezing the UI
        self.status_var.set("Combining PDFs...")
        self.progress.start()
        self.combine_btn.config(state="disabled")
        
        def combine_thread():
            success = self.combiner.combine_pdfs_with_bookmarks(selected_pdfs, output_path)
            
            # Update UI in main thread
            self.root.after(0, self.combine_complete, success, output_path)
        
        thread = threading.Thread(target=combine_thread)
        thread.daemon = True
        thread.start()
        
    def combine_complete(self, success: bool, output_path: str):
        """Called when PDF combination is complete."""
        self.progress.stop()
        self.combine_btn.config(state="normal")
        
        if success:
            self.status_var.set(f"Successfully created: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", 
                              f"PDFs combined successfully!\n\nOutput file: {output_path}\n\n"
                              f"The combined PDF includes bookmarks for each individual PDF file.")
        else:
            self.status_var.set("Error combining PDFs")
            messagebox.showerror("Error", "An error occurred while combining the PDFs. Please check the console for details.")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main function to run the application."""
    try:
        # Check if PyPDF2 is available
        import PyPDF2
    except ImportError:
        print("Error: PyPDF2 is not installed.")
        print("Please install it using: pip install PyPDF2")
        sys.exit(1)
    
    # Create and run the GUI
    app = PDFCombinerGUI()
    app.run()


if __name__ == "__main__":
    main()