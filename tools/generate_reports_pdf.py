"""Build a styled PDF from the project's technical and test Markdown reports."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from xml.sax.saxutils import escape


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "reports" / "DjangoStart-technicke-a-testovaci-reporty.pdf"
REPORTS = (
    ("Technický stand-up report", PROJECT_ROOT / "TECHNICAL-REPORT.md"),
    ("Testovací plán dle průmyslových metodik", PROJECT_ROOT / "TEST-PLAN.md"),
    ("Testovací report dle průmyslových metodik", PROJECT_ROOT / "TEST-REPORT.md"),
)

INK = colors.HexColor("#1C2440")
VIOLET = colors.HexColor("#5C3EC7")
VIOLET_PALE = colors.HexColor("#F0EDFF")
MINT = colors.HexColor("#EAF9F2")
MUTED = colors.HexColor("#4E5872")
LINE = colors.HexColor("#DCE1ED")


def register_fonts() -> tuple[str, str]:
    windows_fonts = Path(r"C:\Windows\Fonts")
    regular = windows_fonts / "arial.ttf"
    bold = windows_fonts / "arialbd.ttf"
    if not regular.is_file() or not bold.is_file():
        raise FileNotFoundError(
            "Pro vytvoření českého PDF je vyžadován font Arial "
            f"v adresáři {windows_fonts}."
        )

    pdfmetrics.registerFont(TTFont("ReportSans", str(regular)))
    pdfmetrics.registerFont(TTFont("ReportSansBold", str(bold)))
    return "ReportSans", "ReportSansBold"


def build_styles(regular: str, bold: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName=bold,
            fontSize=31,
            leading=37,
            textColor=INK,
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["Normal"],
            fontName=regular,
            fontSize=12,
            leading=18,
            textColor=MUTED,
            spaceAfter=28,
        ),
        "h1": ParagraphStyle(
            "ReportH1",
            parent=base["Heading1"],
            fontName=bold,
            fontSize=22,
            leading=27,
            textColor=INK,
            spaceBefore=20,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "ReportH2",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=15,
            leading=20,
            textColor=VIOLET,
            spaceBefore=16,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "ReportH3",
            parent=base["Heading3"],
            fontName=bold,
            fontSize=11,
            leading=15,
            textColor=INK,
            spaceBefore=11,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "ReportBody",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.4,
            leading=14,
            textColor=INK,
            spaceAfter=7,
        ),
        "list": ParagraphStyle(
            "ReportList",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.4,
            leading=14,
            leftIndent=14,
            firstLineIndent=-11,
            textColor=INK,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "ReportCode",
            fontName=regular,
            fontSize=7.6,
            leading=10,
            leftIndent=9,
            rightIndent=9,
            textColor=INK,
            backColor=VIOLET_PALE,
            borderPadding=10,
            spaceBefore=6,
            spaceAfter=11,
        ),
        "table": ParagraphStyle(
            "ReportTable",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.3,
            leading=9.2,
            textColor=INK,
        ),
        "table_header": ParagraphStyle(
            "ReportTableHeader",
            parent=base["BodyText"],
            fontName=bold,
            fontSize=7.3,
            leading=9.2,
            textColor=VIOLET,
        ),
    }


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip()))


def table_from_lines(lines: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    rows = [table_cells(line) for line in lines if not is_table_separator(line)]
    column_count = max(len(row) for row in rows)
    normalized_rows = [row + [""] * (column_count - len(row)) for row in rows]
    data = []
    for row_index, row in enumerate(normalized_rows):
        style = styles["table_header"] if row_index == 0 else styles["table"]
        data.append([Paragraph(escape(value), style) for value in row])

    available_width = A4[0] - 3.2 * cm
    widths = [available_width / column_count] * column_count
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), VIOLET_PALE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAFE")]),
            ]
        )
    )
    return table


def inline_markdown(text: str) -> str:
    escaped = escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<font name="ReportSans">\1</font>', escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r'<b>\1</b>', escaped)
    return escaped


def markdown_story(markdown: str, styles: dict[str, ParagraphStyle]) -> list[object]:
    story: list[object] = []
    lines = markdown.splitlines()
    index = 0
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            story.append(Paragraph(inline_markdown(" ".join(paragraph_lines)), styles["body"]))
            paragraph_lines.clear()

    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            flush_paragraph()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            story.append(Preformatted("\n".join(code_lines), styles["code"]))
        elif line.startswith("|"):
            flush_paragraph()
            table_lines: list[str] = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(KeepTogether([table_from_lines(table_lines, styles), Spacer(1, 12)]))
            continue
        elif line.startswith("# "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(line[2:]), styles["h1"]))
        elif line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(line[3:]), styles["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(line[4:]), styles["h3"]))
        elif re.match(r"^\d+\. ", line):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(line), styles["list"]))
        elif line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(f"• {line[2:]}"), styles["list"]))
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph_lines.append(line.strip())
        index += 1

    flush_paragraph()
    return story


def draw_page(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(LINE)
    canvas.line(1.6 * cm, height - 1.2 * cm, width - 1.6 * cm, height - 1.2 * cm)
    canvas.setFont("ReportSansBold", 8)
    canvas.setFillColor(VIOLET)
    canvas.drawString(1.6 * cm, height - 0.95 * cm, "DJANGOSTART  /  TECHNICKÉ A TESTOVACÍ REPORTY")
    canvas.setFont("ReportSans", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 1.6 * cm, 0.85 * cm, f"Strana {document.page}")
    canvas.restoreState()


def build_pdf(output_path: Path = OUTPUT_PATH) -> Path:
    regular, bold = register_fonts()
    styles = build_styles(regular, bold)
    output_path.parent.mkdir(exist_ok=True)
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.75 * cm,
        bottomMargin=1.45 * cm,
        title="DjangoStart - Technické a testovací reporty",
        author="DjangoStart",
        subject="Technický stand-up report a testovací dokumentace dle průmyslových metodik",
    )
    story: list[object] = [
        Spacer(1, 3.1 * cm),
        Paragraph("DjangoStart", styles["title"]),
        Paragraph("Technické a testovací reporty", styles["title"]),
        Paragraph(
            "Souhrnný dokument pro stand-up, výuku a dohledatelné řízení kvality",
            styles["subtitle"],
        ),
        Table(
            [
                [Paragraph("OBSAH", styles["table_header"]), Paragraph("3 reporty", styles["table"])],
                [Paragraph("STAV TESTŮ", styles["table_header"]), Paragraph("29 / 29 PASS", styles["table"])],
                [Paragraph("VYTVOŘENO", styles["table_header"]), Paragraph(date.today().strftime("%d. %m. %Y"), styles["table"])],
            ],
            colWidths=[4.2 * cm, 9.2 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), MINT),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#BFE7D5")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BFE7D5")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 13),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                    ("TOPPADDING", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
                ]
            ),
        ),
        Spacer(1, 2 * cm),
        Paragraph(
            "Dokument kombinuje technický stand-up report, testovací plán a testovací report "
            "dle průmyslových standardů a metodik. "
            "Slouží jako podklad pro výuku, kontrolu postupu i rozhodování o dalším vydání.",
            styles["subtitle"],
        ),
    ]

    for title, path in REPORTS:
        story.append(PageBreak())
        story.append(Paragraph(title, styles["title"]))
        story.append(Spacer(1, 5))
        story.extend(markdown_story(path.read_text(encoding="utf-8"), styles))

    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vytvoří souhrnný PDF report DjangoStart.")
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Cesta k výslednému PDF souboru.",
    )
    print(build_pdf(parser.parse_args().output))
