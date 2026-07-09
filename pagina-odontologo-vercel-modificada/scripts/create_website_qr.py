from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "marketing"
RAW_QR = OUT_DIR / "armendariz-website-qr-code.png"
OUT_CARD = OUT_DIR / "armendariz-website-qr.png"

WEBSITE_URL = "https://armendarizodontologia.com"

INK = "#17324d"
MUTED = "#5b7083"
TEAL = "#0f766e"
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


def draw_wrapped(draw, xy, text, font_obj, fill, max_width, gap=8):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
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
        y += bbox[3] - bbox[1] + gap

    return y


def download_qr():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    qr_api = (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size=900x900&margin=24&format=png&data={quote(WEBSITE_URL, safe='')}"
    )
    with urlopen(qr_api, timeout=30) as response:
        RAW_QR.write_bytes(response.read())


def create_card():
    canvas = Image.new("RGBA", (1080, 1350), "#f7fbfb")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((-120, -120, 650, 300), radius=140, fill=SKY)
    draw.rounded_rectangle((590, 930, 1240, 1480), radius=150, fill=MINT)

    logo = Image.open(ROOT / "assets" / "img" / "logo-armendariz.png").convert("RGBA")
    logo.thumbnail((200, 200), Image.LANCZOS)
    draw.rounded_rectangle((80, 60, 330, 260), radius=28, fill=WHITE, outline=LINE, width=2)
    canvas.alpha_composite(logo, (80 + (250 - logo.width) // 2, 60 + (200 - logo.height) // 2))

    draw.text((365, 88), "Armendáriz", font=font(FONT_BLACK, 54), fill=INK)
    draw.text((368, 154), "Salud Odontológica", font=font(FONT_REGULAR, 34), fill=TEAL)
    draw.text((368, 204), "Paraná 460 · Bahía Blanca", font=font(FONT_REGULAR, 28), fill=MUTED)

    draw_wrapped(
        draw,
        (92, 336),
        "Escaneá y visitá nuestra página web",
        font(FONT_BLACK, 64),
        INK,
        900,
        gap=12,
    )

    draw_wrapped(
        draw,
        (96, 520),
        "Conocé servicios, horarios, dirección y pedí tu turno por WhatsApp.",
        font(FONT_REGULAR, 38),
        MUTED,
        850,
        gap=10,
    )

    qr = Image.open(RAW_QR).convert("RGBA").resize((560, 560), Image.LANCZOS)
    draw.rounded_rectangle((260, 680, 820, 1240), radius=34, fill=WHITE)
    canvas.alpha_composite(qr, (260, 680))

    draw.rounded_rectangle((208, 1254, 872, 1316), radius=20, fill=TEAL)
    draw.text((268, 1270), "armendarizodontologia.com", font=font(FONT_BOLD, 31), fill=WHITE)

    canvas.convert("RGB").save(OUT_CARD, quality=96, optimize=True)


if __name__ == "__main__":
    download_qr()
    create_card()
    print(OUT_CARD)
