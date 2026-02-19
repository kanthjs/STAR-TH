"""
STAR-TH Configuration Constants
"""

# App metadata
APP_VERSION = "0.1.0"
APP_TITLE = "STAR-TH: สถิติสำหรับวิจัยการเกษตรไทย"
APP_DESCRIPTION = "Modern Statistical Tool for Thai Agricultural Research"

# Claude API model
CLAUDE_MODEL = "claude-sonnet-4-6"

# Design types
DESIGN_TYPES = {
    "CRD": "Completely Randomized Design",
    "RCBD": "Randomized Complete Block Design",
    "LS": "Latin Square",
    "AL": "Alpha Lattice",
}

DESIGN_TYPES_THAI = {
    "CRD": "ออกแบบสุ่มโดยสิ้นเชิง",
    "RCBD": "ออกแบบบล็อกสุ่มสมบูรณ์",
    "LS": "ออกแบบตารางละติน",
    "AL": "ออกแบบแอลฟ่า-แลตทิซ",
}

# Crop types
CROP_TYPES = [
    "ข้าวเจ้า (Rice - Japonica)",
    "ข้าวเสบ้า (Rice - Indica)",
    "ข้าวเหนียว (Sticky Rice)",
    "ข้าวหอม (Fragrant Rice)",
    "ข้าวพื้นท้องถิ่น (Local Rice)",
    "อื่น ๆ (Other)",
]

# Thai provinces (for site/environment names)
THAI_PROVINCES = [
    "กรุงเทพ (Bangkok)",
    "ชลบุรี",
    "นครปฐม",
    "นครราชสีมา",
    "บุรีรัมย์",
    "ยโสธร",
    "ลพบุรี",
    "สกลนคร",
    "สงขลา",
    "อุบลราชธานี",
    "อื่น ๆ",
]

# CV quality thresholds
CV_THRESHOLDS = {
    "excellent": 10,      # < 10%
    "good": 15,           # 10-15%
    "acceptable": 20,     # 15-20%
    # > 20% is poor
}

CV_QUALITY_THAI = {
    "excellent": "ดีเยี่ยม",
    "good": "ดี",
    "acceptable": "ยอมรับได้",
    "poor": "ต่ำ",
}

# Statistical significance levels
ALPHA_LEVELS = [0.01, 0.05, 0.10]

# Default values for forms
DEFAULT_ALPHA = 0.05
DEFAULT_REPLICATIONS = 4
DEFAULT_TREATMENTS = 8

# Streamlit page config
PAGE_CONFIG = {
    "page_title": "STAR-TH",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
