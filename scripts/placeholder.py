"""
Screenshot Placeholder Generator
Creates simple placeholder images until real screenshots are taken
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_placeholder(filename, text, width=1920, height=1080):
    """Create a placeholder image with text."""
    
    # Create image with professional blue background
    img = Image.new('RGB', (width, height), color='#1E3A8A')
    draw = ImageDraw.Draw(img)
    
    # Add subtle gradient effect
    for y in range(height):
        color = (
            int(30 + (y / height) * 20),
            int(58 + (y / height) * 30),
            int(138 + (y / height) * 50)
        )
        draw.line([(0, y), (width, y)], fill=color)
    
    # Add border
    draw.rectangle([(10, 10), (width-10, height-10)], outline='#3B82F6', width=4)
    
    # Add main text
    try:
        # Try to use a nice font
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except:
        # Fall back to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw title
    title = "AI Job Agent"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, height//4), title, fill='white', font=font_large)
    
    # Draw subtitle
    subtitle = text
    bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, height//2), subtitle, fill='#93C5FD', font=font_small)
    
    # Add note at bottom
    note = "Screenshot placeholder - Replace with actual screenshot"
    bbox = draw.textbbox((0, 0), note, font=font_small)
    note_width = bbox[2] - bbox[0]
    note_x = (width - note_width) // 2
    draw.text((note_x, height - 100), note, fill='#60A5FA', font=font_small)
    
    # Save image
    img.save(filename)
    print("Created placeholder: {}".format(filename))


def create_all_placeholders():
    """Create all required placeholder screenshots."""
    
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    placeholders = [
        ("dashboard_overview.png", "Dashboard Overview - Streamlit Interface"),
        ("job_tracking_table.png", "Job Tracking Table - Application Status"),
        ("resume_tailoring_example.png", "Resume Tailoring - AI Optimization"),
        ("successful_apply_log.png", "Application Log - Success Messages"),
        ("architecture_diagram.png", "System Architecture Diagram")
    ]
    
    print("Creating screenshot placeholders...")
    print("=" * 50)
    
    for filename, text in placeholders:
        filepath = os.path.join(screenshots_dir, filename)
        create_placeholder(filepath, text)
    
    print("\nAll placeholders created!")
    print("Location: screenshots/")
    print("Next: Replace with real screenshots using:")
    print("   python screenshots/take_screenshots.py")
    print("   OR")
    print("   streamlit run ui/dashboard.py")
    print("   Then manually capture screenshots")


if __name__ == "__main__":
    try:
        create_all_placeholders()
    except ImportError:
        print("PIL/Pillow not installed")
        print("Install with: pip install Pillow")
        print("\nOr simply take real screenshots instead of placeholders")