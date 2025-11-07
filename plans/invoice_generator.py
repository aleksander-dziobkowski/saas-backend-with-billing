from django.http import HttpResponse
from django.core.mail import EmailMessage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import date
from billing_saas.settings import EMAIL_HOST_USER
from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_invoice_email(to_email, subject, body, pdf_bytes):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=[to_email],
    )
    email.attach("faktura.pdf", pdf_bytes, "application/pdf")
    email.send()
    return f"Email sent to {to_email}"

def generate_invoice_pdf(user, plan):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    amount = plan.price

    elements.append(Paragraph("<b>Faktura VAT</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Data wystawienia: {date.today().strftime('%d-%m-%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    sprzedawca = "<b>Sprzedawca: Dane twojej firmy</b>"
    nabywca = f"<b>Nabywca: {user.email}</b>"

    tabela_dane = Table([[Paragraph(sprzedawca, styles['Normal']),
                         Paragraph(nabywca, styles['Normal'])]], colWidths=[250, 250])
    elements.append(tabela_dane)
    elements.append(Spacer(1, 20))

    pozycje = [
        ["Lp.", "Nazwa towaru/uslugi", "Ilosc", "Cena jedn. (PLN)", "Wartosc (PLN)"],
        ["1", plan.name, "1", amount, amount],
    ]
    tabela_pozycji = Table(pozycje, colWidths=[30, 200, 60, 100, 100])
    tabela_pozycji.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(tabela_pozycji)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Razem brutto: {amount}</b>", styles['Heading3']))

    doc.build(elements)
    buffer.seek(0)
    
    print("wywoluje send_invoice_email")
    send_invoice_email.delay(
        user.email,
        "Twoja faktura VAT",
        "Dzień dobry,\n\nw załączniku znajduje się Twoja faktura PDF.\n\nPozdrawiamy!",
        buffer.read()
    )

    return HttpResponse("Invoice sent")
