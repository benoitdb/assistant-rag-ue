import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

REGLEMENT_PDF = ROOT / "docs" / "sources" / "reglement_ue_2021_1060.pdf"
DECRET_PDF = ROOT / "docs" / "sources" / "decret_2022_608.pdf"
GUIDE_REGIONAL_PDF = ROOT / "docs" / "sources" / "guide_regional_centre_val_de_loire.pdf"
