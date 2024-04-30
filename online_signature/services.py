import os

from xhtml2pdf import pisa
from io import BytesIO
from django.core.files import File


def generate_signed_document(document):
    content = document.document_content.replace("\n\r", "<br>")
    html = """<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <style>
            @page {
                size: A4;
                margin: 1cm;
                padding: 1cm;
            }

            @font-face {
                font-family: 'Times New Roman';
                src: url("static/fonts/times_new_roman.ttf"); 
            }

            body {
                font-size: 12pt;
                font-family: 'Times New Roman';
            }
          </style>
    </head>
    <body>
    <div style="color: steelblue; border: 1px solid steelblue; padding: 10px;">
        <span style="text-decoration: underline;">Документ подписан в %s (МСК)</span><br>
        <span>Кодом из СМС: %s</span><br>
        <span>%s</span>
    </div>
    <br>
    %s
    </body>
    </html>""" % (
        document.signed_at.strftime("%d.%m.%Y %H:%M:%S"),
        document.confirmation_code,
        document.formatted_phone_number,
        content,
    )
    result = pisa.CreatePDF(html, dest=BytesIO(), encoding="utf-8")
    file_name = os.path.basename(document.document_file.name)
    document.document_file.delete()
    document.document_file = File(result.dest, name=file_name)
    document.save()
