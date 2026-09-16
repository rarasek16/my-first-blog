"""Create the consultation-hours notice for Moodle courses."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "documents" / "Konzultacni-hodiny.pdf"
WINDOWS_FONTS = Path(r"C:\Windows\Fonts")
INK = colors.HexColor("#1C2440")
VIOLET = colors.HexColor("#5C3EC7")
VIOLET_PALE = colors.HexColor("#F0EDFF")
MINT = colors.HexColor("#EAF9F2")
MUTED = colors.HexColor("#4E5872")


def register_fonts() -> tuple[str, str]:
    regular = WINDOWS_FONTS / "arial.ttf"
    bold = WINDOWS_FONTS / "arialbd.ttf"
    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError(
            "Pro vytvoření českého PDF je vyžadován font Arial "
            f"v adresáři {WINDOWS_FONTS}."
        )

    pdfmetrics.registerFont(TTFont("ConsultationSans", str(regular)))
    pdfmetrics.registerFont(TTFont("ConsultationSansBold", str(bold)))
    return "ConsultationSans", "ConsultationSansBold"


def build_pdf() -> Path:
    regular, bold = register_fonts()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "ConsultationTitle",
        parent=styles["Title"],
        fontName=bold,
        fontSize=29,
        leading=35,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    subtitle = ParagraphStyle(
        "ConsultationSubtitle",
        parent=styles["Normal"],
        fontName=regular,
        fontSize=13,
        leading=19,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
    label = ParagraphStyle(
        "ConsultationLabel",
        parent=styles["Normal"],
        fontName=bold,
        fontSize=11,
        leading=15,
        textColor=VIOLET,
        alignment=TA_CENTER,
    )
    time = ParagraphStyle(
        "ConsultationTime",
        parent=styles["Normal"],
        fontName=bold,
        fontSize=25,
        leading=31,
        textColor=INK,
        alignment=TA_CENTER,
    )
    body = ParagraphStyle(
        "ConsultationBody",
        parent=styles["Normal"],
        fontName=regular,
        fontSize=12,
        leading=18,
        textColor=INK,
        alignment=TA_CENTER,
    )

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=2.2 * cm,
        leftMargin=2.2 * cm,
        topMargin=2.4 * cm,
        bottomMargin=2.4 * cm,
        title="Konzultační hodiny",
        author="Ing. Radko Kozakovič, Ph.D.",
    )
    story = [
        Spacer(1, 3.4 * cm),
        Paragraph("Konzultační hodiny", title),
        Paragraph("Ing. Radko Kozakovič, Ph.D.", subtitle),
        Spacer(1, 1.5 * cm),
        Table(
            [
                [Paragraph("PRAVIDELNÝ TERMÍN", label)],
                [Paragraph("Každé pondělí", time)],
                [Paragraph("12:35–13:20", time)],
            ],
            colWidths=[13.5 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), VIOLET_PALE),
                    ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CFC7F8")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCD7F8")),
                    ("TOPPADDING", (0, 0), (-1, -1), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ]
            ),
        ),
        Spacer(1, 1.6 * cm),
        Table(
            [[Paragraph("Po předchozí domluvě jsou možné individuální konzultace i mimo uvedený termín.", body)]],
            colWidths=[13.5 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), MINT),
                    ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#BFE7D5")),
                    ("TOPPADDING", (0, 0), (-1, -1), 18),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
                    ("LEFTPADDING", (0, 0), (-1, -1), 20),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 20),
                ]
            ),
        ),
        Spacer(1, 1.2 * cm),
        Paragraph("Určeno studentům všech mých kurzů.", subtitle),
    ]
    document.build(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build_pdf())
