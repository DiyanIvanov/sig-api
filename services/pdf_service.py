from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from io import BytesIO


def generate_pdf(invoice):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Heading1"],
        fontName="Helvetica",
        fontSize=24,
        spaceAfter=4
    )

    right_style = ParagraphStyle(
        "RightAligned",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
    )

    story = []
    header = Table(
        [
            [
                Paragraph("<b>SIG API</b>", styles["Heading2"]),
                Paragraph("<b>INVOICE</b>", title_style),
            ]
        ],
        colWidths=[85 * mm, 65 * mm],
    )

    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(header)
    story.append(Spacer(1, 12 * mm))

    invoice_details = Table(
        [
            ["Invoice number:", str(invoice.invoice_id)],
            ["Invoice date:", str(invoice.invoice_date)],
            ["Customer:", invoice.customer],
        ],
        colWidths=[35 * mm, 115 * mm],
    )

    invoice_details.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(invoice_details)
    story.append(Spacer(1, 12 * mm))

    product_data = [
        [
            "Product",
            "Quantity",
            "Unit price",
            "Total",
        ]
    ]

    for product in invoice.products:
        product_data.append(
            [
                product.name,
                str(product.quantity),
                f"£{product.price:,.2f}",
                f"£{product.total_price:,.2f}",
            ]
        )

    products_table = Table(
        product_data,
        colWidths=[
            75 * mm,
            25 * mm,
            30 * mm,
            30 * mm,
        ],
        repeatRows=1,
    )

    products_table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),

                # Body
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 7),

                # Alignment
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),

                # Lines
                ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
                ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.lightgrey),
            ]
        )
    )

    story.append(products_table)
    story.append(Spacer(1, 10 * mm))

    total_table = Table(
        [
            [
                "",
                Paragraph(
                    f"<b>Total: £{invoice.total_price:,.2f}</b>",
                    right_style,
                ),
            ]
        ],
        colWidths=[100 * mm, 60 * mm],
    )

    total_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LINEABOVE", (1, 0), (1, 0), 1, colors.black),
                ("TOPPADDING", (1, 0), (1, 0), 8),
            ]
        )
    )

    story.append(total_table)
    story.append(Spacer(1, 20 * mm))

    # Footer
    story.append(
        Paragraph(
            "Thank you for your business.",
            styles["Normal"],
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

