"""
Font management for Thai fonts.
"""

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class FontManager:
    """Manages font registration for Thai fonts."""
    
    _fonts_registered = False
    
    @classmethod
    def get_fonts_dir(cls) -> str:
        """Get the fonts directory path."""
        # Look for fonts in parent directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        return os.path.join(parent_dir, "fonts", "THSarabunNew")
    
    @classmethod
    def register_fonts(cls) -> None:
        """Register Thai fonts for use in PDF generation."""
        if cls._fonts_registered:
            return
            
        try:
            fonts_dir = cls.get_fonts_dir()
            pdfmetrics.registerFont(
                TTFont("THSarabunNew", os.path.join(fonts_dir, "THSarabunNew.ttf"))
            )
            pdfmetrics.registerFont(
                TTFont("THSarabunNew-Bold", os.path.join(fonts_dir, "THSarabunNew Bold.ttf"))
            )
            cls._fonts_registered = True
        except Exception as e:
            print(f"Warning: Could not register fonts: {e}")
