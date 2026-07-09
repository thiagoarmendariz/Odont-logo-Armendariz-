from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "marketing" / "armendariz-promo-instagram.png"
OUT_STORY = ROOT / "assets" / "marketing" / "armendariz-promo-historia.png"
OUT_SERVICES = ROOT / "assets" / "marketing" / "armendariz-promo-servicios.png"

W = H = 1080
INK = "#17324d"
MUTED = "#5b7083"
TEAL = "#0f766e"
TEAL_DARK = "#0b5f59"
MINT = "#d9f6ec"
SKY = "#dff5ff"
WHITE = "#ffffff"
LINE = "#dbe8ee"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
FONT_REGULAR = FONT_DIR / "Arial.ttf"
FONT_BOLD = FONT_DIR / "Arial Bold.ttf"
FONT_BLACK = FONT_DIR / "Arial Black.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def rounded_image(path, size, radius=32):
    img = Image.open(path).convert("RGB")
    img_ratio = img.width / img.height
    target_ratio = size[0] / size[1]

    if img_ratio > target_ratio:
      new_height = size[1]
      new_width = int(new_height * img_ratio)
    else:
      new_width = size[0]
      new_height = int(new_width / img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)
    left = (new_width - size[0]) // 2
    top = (new_height - size[1]) // 2
    img = img.crop((left, top, left + size[0], top + size[1]))

    mask = Image.new("L", size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)

    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def draw_text(draw, xy, text, font_obj, fill, max_width, line_gap=8):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font_obj)
        y += (bbox[3] - bbox[1]) + line_gap

    return y


def paste_shadowed(base, image, xy, radius=32):
    x, y = xy
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (x + 10, y + 14, x + image.width + 10, y + image.height + 14),
        radius=radius,
        fill=(23, 50, 77, 32),
    )
    base.alpha_composite(shadow)
    base.alpha_composite(image, xy)


def draw_logo_header(canvas, draw, logo_size=(180, 180), box=(70, 54, 288, 230), text_x=324):
    logo = Image.open(ROOT / "assets" / "img" / "logo-armendariz.png").convert("RGBA")
    logo.thumbnail(logo_size, Image.LANCZOS)
    draw.rounded_rectangle(box, radius=28, fill=WHITE, outline=LINE, width=2)
    canvas.alpha_composite(
        logo,
        (
            box[0] + ((box[2] - box[0]) - logo.width) // 2,
            box[1] + ((box[3] - box[1]) - logo.height) // 2,
        ),
    )
    draw.text((text_x, box[1] + 20), "Dr. Andres Armendariz", font=font(FONT_BOLD, 39), fill=INK)
    draw.text((text_x, box[1] + 70), "Odontologia general", font=font(FONT_REGULAR, 28), fill=TEAL)
    draw.text((text_x, box[1] + 112), "Parana 460 · Bahia Blanca", font=font(FONT_REGULAR, 26), fill=MUTED)


def create_square_general():
    canvas = Image.new("RGBA", (W, H), "#f7fbfb")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((-80, -90, 560, 260), radius=90, fill=SKY)
    draw.rounded_rectangle((670, 760, 1180, 1160), radius=120, fill=MINT)

    draw_logo_header(canvas, draw)

    y = draw_text(
        draw,
        (70, 330),
        "Atencion odontologica profesional y personalizada",
        font(FONT_BLACK, 66),
        INK,
        520,
        line_gap=10,
    )

    y += 22
    draw_text(
        draw,
        (72, y),
        "Turnos simples por WhatsApp y atencion cercana para cuidar tu salud bucal.",
        font(FONT_REGULAR, 30),
        MUTED,
        510,
        line_gap=8,
    )

    draw.rounded_rectangle((70, 765, 505, 845), radius=22, fill=TEAL)
    draw.text((105, 785), "Pedir turno", font=font(FONT_BOLD, 31), fill=WHITE)
    draw.text((305, 785), "291 423-8463", font=font(FONT_BOLD, 31), fill=WHITE)

    draw.rounded_rectangle((70, 874, 505, 936), radius=18, fill=WHITE, outline=LINE, width=2)
    draw.text((98, 891), "@andres.armendariz.180", font=font(FONT_BOLD, 26), fill=TEAL_DARK)

    main_photo = rounded_image(ROOT / "assets" / "img" / "consultorio-espera.jpg", (418, 428), 34)
    secondary_photo = rounded_image(ROOT / "assets" / "img" / "consultorio-sillon.jpg", (360, 278), 30)
    third_photo = rounded_image(ROOT / "assets" / "img" / "consultorio-pasillo.jpg", (300, 220), 28)

    paste_shadowed(canvas, main_photo, (600, 246), 34)
    paste_shadowed(canvas, secondary_photo, (548, 700), 30)
    paste_shadowed(canvas, third_photo, (728, 802), 28)

    label_box = (620, 610, 968, 660)
    draw.rounded_rectangle(label_box, radius=16, fill=(255, 255, 255, 232))
    draw.text((642, 623), "Consultorio moderno", font=font(FONT_BOLD, 23), fill=TEAL_DARK)

    canvas = canvas.convert("RGB")
    canvas.save(OUT, quality=96, optimize=True)
    print(OUT)


def create_story():
    canvas = Image.new("RGBA", (1080, 1920), "#f7fbfb")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((-140, -120, 1220, 360), radius=140, fill=SKY)
    draw.rounded_rectangle((640, 1220, 1260, 2030), radius=150, fill=MINT)

    draw_logo_header(canvas, draw, logo_size=(190, 190), box=(78, 76, 318, 270), text_x=350)

    hero = rounded_image(ROOT / "assets" / "img" / "consultorio-espera.jpg", (920, 620), 42)
    paste_shadowed(canvas, hero, (80, 330), 42)

    draw.rounded_rectangle((118, 895, 960, 970), radius=22, fill=(255, 255, 255, 236))
    draw.text((155, 914), "Consultorio en Bahia Blanca", font=font(FONT_BOLD, 34), fill=TEAL_DARK)

    y = draw_text(
        draw,
        (82, 1058),
        "Cuida tu salud bucal con atencion cercana",
        font(FONT_BLACK, 72),
        INK,
        900,
        line_gap=12,
    )

    y += 34
    draw_text(
        draw,
        (86, y),
        "Turnos por WhatsApp para consultas generales, limpiezas, arreglos, ortopedia y urgencias odontologicas.",
        font(FONT_REGULAR, 38),
        MUTED,
        850,
        line_gap=12,
    )

    draw.rounded_rectangle((84, 1570, 996, 1672), radius=30, fill=TEAL)
    draw.text((126, 1598), "Pedir turno", font=font(FONT_BOLD, 42), fill=WHITE)
    draw.text((592, 1598), "291 423-8463", font=font(FONT_BOLD, 42), fill=WHITE)

    draw.rounded_rectangle((84, 1710, 996, 1795), radius=25, fill=WHITE, outline=LINE, width=2)
    draw.text((126, 1734), "@andres.armendariz.180", font=font(FONT_BOLD, 34), fill=TEAL_DARK)

    canvas.convert("RGB").save(OUT_STORY, quality=96, optimize=True)
    print(OUT_STORY)


def create_services_square():
    canvas = Image.new("RGBA", (W, H), "#f7fbfb")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((-100, -70, 1180, 250), radius=110, fill=SKY)
    draw.rounded_rectangle((760, 540, 1240, 1160), radius=120, fill=MINT)

    logo = Image.open(ROOT / "assets" / "img" / "logo-armendariz.png").convert("RGBA")
    logo.thumbnail((170, 170), Image.LANCZOS)
    draw.rounded_rectangle((70, 56, 280, 220), radius=26, fill=WHITE, outline=LINE, width=2)
    canvas.alpha_composite(logo, (70 + (210 - logo.width) // 2, 56 + (164 - logo.height) // 2))

    draw.text((318, 78), "Servicios odontologicos", font=font(FONT_BLACK, 52), fill=INK)
    draw.text((320, 144), "Dr. Andres Armendariz · Bahia Blanca", font=font(FONT_REGULAR, 29), fill=TEAL)

    photo = rounded_image(ROOT / "assets" / "img" / "consultorio-sillon.jpg", (402, 510), 38)
    paste_shadowed(canvas, photo, (606, 270), 38)

    services = [
        "Limpieza dental",
        "Consultas generales",
        "Arreglos",
        "Blanqueamiento dental",
        "Ortopedia",
        "Extracciones",
        "Urgencias odontologicas",
    ]

    y = 300
    for index, service in enumerate(services, start=1):
        draw.rounded_rectangle((76, y, 548, y + 64), radius=18, fill=WHITE, outline=LINE, width=2)
        draw.rounded_rectangle((94, y + 13, 134, y + 53), radius=12, fill=MINT)
        draw.text((105, y + 20), str(index), font=font(FONT_BOLD, 20), fill=TEAL_DARK)
        draw.text((154, y + 17), service, font=font(FONT_BOLD, 28), fill=INK)
        y += 78

    draw.rounded_rectangle((76, 878, 1008, 962), radius=24, fill=TEAL)
    draw.text((112, 902), "Turnos por WhatsApp", font=font(FONT_BOLD, 34), fill=WHITE)
    draw.text((664, 902), "291 423-8463", font=font(FONT_BOLD, 34), fill=WHITE)

    draw.text((80, 1000), "Parana 460 · Bahia Blanca", font=font(FONT_REGULAR, 27), fill=MUTED)

    canvas.convert("RGB").save(OUT_SERVICES, quality=96, optimize=True)
    print(OUT_SERVICES)


def main():
    create_square_general()
    create_story()
    create_services_square()


if __name__ == "__main__":
    main()
