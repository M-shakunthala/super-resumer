from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib import styles
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from pathlib import Path
from core.config import Config


class PDFBuilder:

    def __init__(self):
        """Initialize PDF builder with configuration"""
        self.config = Config.load()
        pdf_config = self.config.get('pdf', {})
        
        # Output directory for PDFs
        self.output_dir = pdf_config.get('output_dir', 'resumes/pdfs')
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # PDF settings
        self.page_size = pdf_config.get('page_size', 'letter')
        self.margins = pdf_config.get('margins', {
            'top': 0.75 * inch,
            'bottom': 0.75 * inch,
            'left': 0.75 * inch,
            'right': 0.75 * inch
        })
        
        # Try to register custom fonts if available
        self._register_fonts()

    def _register_fonts(self):
        """Register custom fonts if available"""
        fonts_dir = Path("resumes/fonts")
        if fonts_dir.exists():
            try:
                # Register custom fonts if they exist
                for font_file in fonts_dir.glob("*.ttf"):
                    try:
                        font_name = font_file.stem
                        pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
                        print(f"Registered font: {font_name}")
                    except:
                        pass
            except Exception as e:
                print(f"Font registration error: {e}")

    def build(
        self,
        resume_text,
        filename,
        company_name=None
    ):
        """
        Build PDF from resume text
        
        Args:
            resume_text: Resume text content
            filename: Output PDF filename
            company_name: Optional company name for filename
        """
        # Sanitize filename
        if company_name:
            safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"resume_{safe_name.replace(' ', '_').lower()}.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self._get_pagesize(),
            rightMargin=self.margins['right'],
            leftMargin=self.margins['left'],
            topMargin=self.margins['top'],
            bottomMargin=self.margins['bottom']
        )

        # Get styles
        style = styles.getSampleStyleSheet()
        
        # Customize styles for professional look
        self._customize_styles(style)
        
        # Build content
        content = self._parse_resume_content(resume_text, style)
        
        # Build PDF
        doc.build(content)
        
        return output_path
    
    def _get_pagesize(self):
        """Get page size from config"""
        if self.page_size == 'letter':
            return letter
        elif self.page_size == 'a4':
            from reportlab.lib.pagesizes import A4
            return A4
        else:
            return letter
    
    def _customize_styles(self, style):
        """Customize styles for professional resume look"""
        # Title style
        if 'Title' in style:
            style['Title'].fontSize = 18
            style['Title'].fontName = 'Helvetica-Bold'
            style['Title'].spaceAfter = 12
        
        # Heading style
        if 'Heading1' in style:
            style['Heading1'].fontSize = 14
            style['Heading1'].fontName = 'Helvetica-Bold'
            style['Heading1'].spaceAfter = 6
            style['Heading1'].spaceBefore = 12
        
        # Body text style
        if 'BodyText' in style:
            style['BodyText'].fontSize = 10
            style['BodyText'].fontName = 'Helvetica'
            style['BodyText'].spaceAfter = 3
            style['BodyText'].leading = 14
    
    def _parse_resume_content(self, resume_text, style):
        """Parse resume text into PDF content"""
        content = []
        lines = resume_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                content.append(Spacer(1, 0.1 * inch))
                continue
            
            # Detect headers (lines ending with colon or all caps)
            if line.endswith(':') or line.isupper() or self._is_header(line):
                content.append(Paragraph(line, style['Heading1']))
            else:
                content.append(Paragraph(line, style['BodyText']))
        
        return content
    
    def _is_header(self, line):
        """Check if line is likely a header"""
        # Common resume section headers
        headers = ['skills', 'experience', 'education', 'projects', 'certifications', 
                  'languages', 'interests', 'summary', 'objective', 'contact']
        line_lower = line.lower().rstrip(':')
        return line_lower in headers
    
    def build_from_sections(self, resume_sections, filename, company_name=None):
        """
        Build PDF from structured resume sections
        
        Args:
            resume_sections: Dictionary with resume sections
            filename: Output PDF filename
            company_name: Optional company name for filename
        """
        # Convert sections to text
        resume_text = self._sections_to_text(resume_sections)
        return self.build(resume_text, filename, company_name)
    
    def _sections_to_text(self, sections):
        """Convert resume sections dictionary to text"""
        lines = []
        for section_name, section_content in sections.items():
            if section_content:
                lines.append(section_name.upper() + ':')
                lines.append(section_content)
                lines.append('')  # Empty line between sections
        
        return '\n'.join(lines)
    
    def build_multiple(self, resume_variants, base_name="resume"):
        """
        Build multiple PDFs from resume variants
        
        Args:
            resume_variants: Dictionary of {company_name: resume_text}
            base_name: Base name for PDF files
            
        Returns:
            List of generated PDF paths
        """
        generated_files = []
        
        for company_name, resume_text in resume_variants.items():
            filename = f"{base_name}_{company_name.lower().replace(' ', '_')}.pdf"
            output_path = self.build(resume_text, filename, company_name)
            generated_files.append(output_path)
        
        return generated_files
    
    def get_pdf_path(self, company_name):
        """Get expected PDF path for a company"""
        safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"resume_{safe_name.replace(' ', '_').lower()}.pdf"
        return os.path.join(self.output_dir, filename)
    
    def pdf_exists(self, company_name):
        """Check if PDF already exists for company"""
        pdf_path = self.get_pdf_path(company_name)
        return os.path.exists(pdf_path)
    
    def cleanup_old_pdfs(self, days=7):
        """Remove PDFs older than specified days"""
        import time
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        removed_count = 0
        for pdf_file in Path(self.output_dir).glob("*.pdf"):
            if pdf_file.stat().st_mtime < cutoff_time:
                pdf_file.unlink()
                removed_count += 1
        
        return removed_count
