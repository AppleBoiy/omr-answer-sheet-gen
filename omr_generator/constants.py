"""
Constants for OMR layout and styling.
"""

from reportlab.lib.units import mm


class LayoutConstants:
    """Constants for layout dimensions and styling."""
    
    # Fonts
    FONT_NORMAL = "THSarabunNew"
    FONT_BOLD = "THSarabunNew-Bold"
    
    # Colors
    COLOR_GRID = (225/255, 225/255, 225/255)
    COLOR_HIGHLIGHT = (248/255, 248/255, 248/255)
    
    # Section Heights
    ID_SECTION_HEIGHT = 28 * mm   
    ANSWER_SECTION_HEIGHT = 170 * mm 
    FOOTER_HEIGHT = 25 * mm
    
    # Markers and Bubbles
    TRIM_MARKER_SIZE = 3.5 * mm
    FIDUCIAL_SIZE = 10 * mm
    BUBBLE_DIAMETER = 7.0 * mm


class ChoicePresets:
    """Predefined choice label sets."""
    
    THAI_4 = ["ก", "ข", "ค", "ง"]
    THAI_5 = ["ก", "ข", "ค", "ง", "จ"]
    TRUE_FALSE = ["ถูก", "ผิด"]
    TRUE_FALSE_SHORT = ["ถ", "ผ"]
    ENGLISH_4 = ["A", "B", "C", "D"]
    ENGLISH_5 = ["A", "B", "C", "D", "E"]
    NUMBERS_3 = ["1", "2", "3"]
    NUMBERS_4 = ["1", "2", "3", "4"]
