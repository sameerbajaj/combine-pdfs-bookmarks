#!/usr/bin/env python3
"""
PDF Combiner with Automatic Bookmark Generation - Command Line Interface
A utility to combine multiple PDFs into a single file with automatic bookmark creation.
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from typing import List, Tuple
import re


def natural_sort_key(path: str, root_folder: str = None):
    """Return a key that naturally sorts by folder path components then filename (ascending)."""
    def split_parts(s: str):
        tokens = re.split(r"(\d+)", s.lower())
        return tuple((0, int(p)) if p.isdigit() else (1, p) for p in tokens)
    # Use relative path to the root folder when provided so top-level dir order comes first
    rel_path = os.path.relpath(path, root_folder) if root_folder else os.path.normpath(path)
    components = rel_path.split(os.sep)
    # Sort by each component using natural ordering (numbers before letters within each token)
    return tuple(split_parts(component) for component in components)


class PDFCombinerCLI:
    def __init__(self):
        self.combined_pdf = None
        self.output_path = None
        
    def find_pdf_files(self, folder_path: str, recursive: bool = False) -> List[str]:
        """Find all PDF files in the specified folder. If recursive, include subfolders."""
        folder = Path(folder_path)
        candidates: List[str] = []
        if recursive:
            candidates.extend([str(p) for p in folder.rglob("*.pdf")])
            candidates.extend([str(p) for p in folder.rglob("*.PDF")])
        else:
            candidates.extend([str(p) for p in folder.glob("*.pdf")])
            candidates.extend([str(p) for p in folder.glob("*.PDF")])
        # Sort files naturally (1.pdf, 2.pdf, 10.pdf instead of 1.pdf, 10.pdf, 2.pdf)
        candidates.sort(key=lambda p: natural_sort_key(p, folder_path))
        return candidates
    
    def get_pdf_info(self, pdf_path: str) -> Tuple[str, int]:
        """Get PDF filename and page count."""
        try:
            from PyPDF2 import PdfReader  # Lazy import
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                page_count = len(reader.pages)
                filename = os.path.basename(pdf_path)
                return filename, page_count
        except ImportError:
            print("Error: PyPDF2 is not installed. Please install it using: pip install PyPDF2")
            return os.path.basename(pdf_path), 0
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return os.path.basename(pdf_path), 0
    
    def combine_pdfs_with_bookmarks(self, pdf_files: List[str], output_path: str) -> bool:
        """Combine PDFs and create bookmarks for each file."""
        try:
            from PyPDF2 import PdfReader, PdfWriter  # Lazy import
        except ImportError:
            print("Error: PyPDF2 is not installed. Please install it using: pip install PyPDF2")
            return False
        
        try:
            writer = PdfWriter()
            current_page = 0
            
            print(f"Starting to combine {len(pdf_files)} PDF files...")
            
            # Ensure deterministic, hierarchical natural ordering
            try:
                root = os.path.commonpath(pdf_files) if pdf_files else None
            except Exception:
                root = None
            pdf_files = sorted(pdf_files, key=lambda p: natural_sort_key(p, root))
            
            # Process each PDF file
            for i, pdf_path in enumerate(pdf_files, 1):
                if not os.path.exists(pdf_path):
                    print(f"Warning: {pdf_path} not found, skipping...")
                    continue
                
                try:
                    filename = os.path.basename(pdf_path)
                    print(f"Processing {i}/{len(pdf_files)}: {filename}")
                    
                    with open(pdf_path, 'rb') as file:
                        reader = PdfReader(file)
                        
                        # Add all pages from this PDF
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        # Create bookmark for this PDF
                        # Remove .pdf extension for cleaner bookmark names
                        bookmark_name = filename.replace('.pdf', '').replace('.PDF', '')
                        
                        # Add bookmark pointing to the first page of this PDF
                        writer.add_outline_item(
                            title=bookmark_name,
                            page_number=current_page
                        )
                        
                        current_page += len(reader.pages)
                        print(f"  Added {len(reader.pages)} pages, bookmark '{bookmark_name}' at page {current_page - len(reader.pages) + 1}")
                        
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
                    return False
            
            # Write the combined PDF
            print(f"Writing combined PDF to: {output_path}")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            self.combined_pdf = output_path
            print(f"Successfully created combined PDF with {current_page} total pages")
            return True
            
        except Exception as e:
            print(f"Error combining PDFs: {e}")
            return False
    
    def interactive_mode(self, folder_path: str = None):
        """Run in interactive mode, asking user for input."""
        print("=== PDF Combiner with Automatic Bookmarks ===\n")
        
        # Get folder path
        if not folder_path:
            folder_path = input("Enter the path to the folder containing PDFs: ").strip()
            if not folder_path:
                print("No folder path provided. Exiting.")
                return False
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist.")
            return False
        
        if not os.path.isdir(folder_path):
            print(f"Error: '{folder_path}' is not a directory.")
            return False
        
        # Ask about including subfolders
        include_subfolders_resp = input("Include PDFs from subfolders as well? (y/n) [y]: ").strip().lower()
        include_subfolders = include_subfolders_resp in ["", "y", "yes"]
        
        # Find PDF files
        print(f"\nScanning folder: {folder_path} {'(including subfolders)' if include_subfolders else ''}")
        pdf_files = self.find_pdf_files(folder_path, recursive=include_subfolders)
        
        if not pdf_files:
            print("No PDF files found in the specified location.")
            return False
        
        # Display found PDFs
        print(f"\nFound {len(pdf_files)} PDF files:")
        total_pages = 0
        for i, pdf_path in enumerate(pdf_files, 1):
            filename, page_count = self.get_pdf_info(pdf_path)
            total_pages += page_count
            print(f"  {i:2d}. {filename:<30} ({page_count:3d} pages)  -> {pdf_path}")
        
        print(f"\nTotal pages: {total_pages}")
        
        # Ask user to confirm
        response = input(f"\nDo you want to combine all {len(pdf_files)} PDFs? (y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Operation cancelled.")
            return False
        
        # Get output filename
        default_output = "combined_pdfs.pdf"
        output_filename = input(f"Enter output filename (default: {default_output}): ").strip()
        if not output_filename:
            output_filename = default_output
        
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        output_path = os.path.join(folder_path, output_filename)
        
        # Check if output file already exists
        if os.path.exists(output_path):
            response = input(f"File '{output_filename}' already exists. Overwrite? (y/n): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return False
        
        # Combine PDFs
        print(f"\nStarting combination process...")
        success = self.combine_pdfs_with_bookmarks(pdf_files, output_path)
        
        if success:
            print(f"\n✅ Success! Combined PDF saved as: {output_path}")
            print("Open the file in any PDF viewer to see the bookmarks in the left sidebar.")
        else:
            print("\n❌ Error occurred during combination. Please check the error messages above.")
        
        return success


def main():
    """Main function to handle command line arguments and run the application."""
    parser = argparse.ArgumentParser(
        description="Combine multiple PDFs into a single file with automatic bookmark generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/pdfs                       # Simplest usage (interactive prompts)
  %(prog)s /path/to/pdfs -o combined.pdf -r    # Non-interactive recursive
  %(prog)s /path/to/pdfs -y                    # Non-interactive defaults (use combined_pdfs.pdf)
  %(prog)s -f /path/to/pdfs                    # Backward-compatible flag usage
  %(prog)s                                     # Interactive mode, prompt for folder
        """
    )
    
    # Positional folder argument (simplest usage)
    parser.add_argument(
        'folder', nargs='?', help='Path to folder containing PDF files'
    )
    
    # Backward-compatible optional flag
    parser.add_argument(
        '-f', '--folder', dest='folder_opt', help='Path to folder containing PDF files'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename for combined PDF (non-interactive when provided)'
    )
    
    parser.add_argument(
        '-r', '--recursive', action='store_true',
        help='Scan subfolders recursively (non-interactive mode). In interactive mode you will be prompted.'
    )
    
    parser.add_argument(
        '-y', '--yes', action='store_true',
        help='Assume yes to prompts and use defaults (non-interactive).'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='PDF Combiner v1.1'
    )
    
    args = parser.parse_args()
    
    # Determine folder (positional takes precedence)
    folder = args.folder if args.folder else args.folder_opt
    
    # Create combiner instance
    combiner = PDFCombinerCLI()
    
    # If output or -y is provided, run in non-interactive mode
    if folder and (args.output or args.yes):
        if not os.path.exists(folder):
            print(f"Error: Folder '{folder}' does not exist.")
            sys.exit(1)
        if not os.path.isdir(folder):
            print(f"Error: '{folder}' is not a directory.")
            sys.exit(1)
        
        pdf_files = combiner.find_pdf_files(folder, recursive=args.recursive)
        if not pdf_files:
            print("No PDF files found in the specified folder.")
            sys.exit(1)
        
        output_filename = args.output if args.output else "combined_pdfs.pdf"
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        output_path = os.path.join(folder, output_filename)
        
        print(f"Combining {len(pdf_files)} PDFs from '{folder}' into '{output_path}'")
        success = combiner.combine_pdfs_with_bookmarks(pdf_files, output_path)
        
        if success:
            print(f"\n✅ Success! Combined PDF saved as: {output_path}")
        else:
            print("\n❌ Error occurred during combination.")
            sys.exit(1)
        return
    
    # Otherwise, run interactive mode (optionally with a folder provided)
    success = combiner.interactive_mode(folder)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()