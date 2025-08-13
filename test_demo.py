#!/usr/bin/env python3
"""
Demo script to create sample PDFs for testing the PDF combiner
This creates a few simple PDFs that you can use to test the utility
"""

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(filename, title, content_lines):
    """Create a simple sample PDF file."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, title)
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    for line in content_lines:
        c.drawString(100, y_position, line)
        y_position -= 20
    
    c.save()
    print(f"Created: {filename}")

def main():
    """Create sample PDFs for testing."""
    print("Creating sample PDFs for testing...")
    
    # Create a test directory
    test_dir = "test_pdfs"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Sample PDF 1
    create_sample_pdf(
        os.path.join(test_dir, "1.pdf"),
        "Chapter 1: Introduction",
        [
            "This is the first chapter of our document.",
            "It contains basic information and overview.",
            "You can use this to test the PDF combiner.",
            "",
            "Features:",
            "- Automatic bookmark generation",
            "- Smart file sorting",
            "- Easy-to-use interface"
        ]
    )
    
    # Sample PDF 2
    create_sample_pdf(
        os.path.join(test_dir, "2.pdf"),
        "Chapter 2: Getting Started",
        [
            "This chapter covers the basics of getting started.",
            "It includes installation instructions and setup.",
            "Perfect for testing the bookmark functionality.",
            "",
            "Installation steps:",
            "1. Run ./install.sh",
            "2. Launch the application",
            "3. Select your PDF folder",
            "4. Combine and enjoy!"
        ]
    )
    
    # Sample PDF 3
    create_sample_pdf(
        os.path.join(test_dir, "3.pdf"),
        "Chapter 3: Advanced Features",
        [
            "This chapter explores advanced features.",
            "Learn about command-line options and automation.",
            "Discover tips and tricks for power users.",
            "",
            "Advanced features:",
            "- Command line interface",
            "- Batch processing",
            "- Custom output naming",
            "- Progress tracking"
        ]
    )
    
    # Sample PDF 10 (to test numerical sorting)
    create_sample_pdf(
        os.path.join(test_dir, "10.pdf"),
        "Chapter 10: Conclusion",
        [
            "This is the final chapter of our document.",
            "It summarizes everything we've learned.",
            "A great way to test the numerical sorting.",
            "",
            "Summary:",
            "- PDF combining made easy",
            "- Automatic bookmark creation",
            "- Professional results every time",
            "- User-friendly interface"
        ]
    )
    
    print(f"\n✅ Created {test_dir} directory with sample PDFs!")
    print(f"📁 Test folder: {os.path.abspath(test_dir)}")
    print("\nYou can now test the PDF combiner:")
    print("1. Run: python3 pdf_combiner.py")
    print("2. Browse to the 'test_pdfs' folder")
    print("3. Scan for PDFs and combine them")
    print("4. Check the bookmarks in the combined PDF!")

if __name__ == "__main__":
    try:
        # Check if reportlab is available
        import reportlab
        main()
    except ImportError:
        print("ReportLab not found. Installing...")
        os.system("pip3 install reportlab")
        print("ReportLab installed. Running demo...")
        main()