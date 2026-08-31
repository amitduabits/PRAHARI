from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

dest = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "plate_gj01ab1234.png"
dest.parent.mkdir(parents=True, exist_ok=True)
img = Image.new("RGB", (400, 120), "white")
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 48)
except OSError:
    font = ImageFont.load_default()
draw.text((20, 30), "GJ01AB1234", fill="black", font=font)
img.save(dest)
print(dest)
