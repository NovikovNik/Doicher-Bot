from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint


def draw_text(upper: str, bottom: str, user=None):
    i = randint(1, 3)
    img = Image.open(f"images/image{i}.jpg")
    W, H = img.size
    draw = ImageDraw.Draw(img)
    draw_upper_text(upper, draw, W, H)
    draw_bottom_text(bottom, draw, W, H)
    if user:
        img.save(f'images/pic_{user}.jpg')
        img.close
    else:
        img.save(f'images/day_word.jpg')
        img.close


def draw_upper_text(text: str, draw, W, H):
    font = ImageFont.truetype(r'fonts/poetsen.ttf', size=190)
    w, h = draw.textsize(font=font, text=text)
    draw.text(((W - w)/2, (H - h)/2 - 100),
              f"{text}", (255, 255, 255), font=font)


def draw_bottom_text(text: str, draw, W, H):
    font = ImageFont.truetype(r'fonts/poetsen.ttf', size=130)
    w, h = draw.textsize(font=font, text=f"Означает: {text}")
    draw.text(((W - w)/2, (H - h)/2 + 100),
              f"Означает: {text}", (255, 255, 255), font=font)
