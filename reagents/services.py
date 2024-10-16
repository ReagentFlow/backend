import io
import random

import barcode
from barcode.writer import ImageWriter
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from reagents.models import Container


def generate_unique_container_id() -> int:
    """Генерация уникального идентификатора контейнера"""
    while True:
        container_id = random.randint(100000000000, 999999999999)

        if not Container.objects.filter(container_id=container_id).exists():
            return container_id


def generate_barcode_image(code: str, format_barcode: str) -> io.BytesIO:
    """Генерация штрих-кода с использованием python-barcode"""
    ean = barcode.get(format_barcode, code, writer=ImageWriter())
    barcode_io = io.BytesIO()
    ean.write(barcode_io)
    barcode_io.seek(0)
    return barcode_io


def generate_pdf_with_barcode(format_barcode: str, container_id: str) -> io.BytesIO:
    """Генерация буфера"""
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    barcode_io = generate_barcode_image(container_id, format_barcode)
    barcode_img = Image.open(barcode_io)
    barcode_img_reader = ImageReader(barcode_img)
    p.drawImage(barcode_img_reader, 50, height - 100, width=35 * mm, height=20 * mm)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
