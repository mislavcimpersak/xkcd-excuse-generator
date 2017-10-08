"""
XKCD Excuse Generator API created using Hug Framework
"""

from io import BytesIO

import hug
from PIL import Image, ImageDraw, ImageFont


# blank image view


# api view
# GET https://function.xkcd-excuse.com/api/v1/?who=one&why=two&what=three
# >>
# {
#     "errors": {
#         "code": 1001,
#         "text": "first text two long"  // možda onda imati validaciju pokraj inputa
#     }
#     "data": {
#         "who": "one",
#         "why": "two",
#         "what": "three",
#         "image_url": "function.xkcd-excuse.com/media/<hash>.png"
#     }
# }


# media image view that displays image directly (.png extension)
# TODO - isprobati ako je minus u textu? dal se isto ok enkodira u hex?
@hug.local()
@hug.get(
    '/media/{who}-{why}-{what}',
    # versions=1,
    output=hug.output_format.png_image,
    examples='/'
)
def img(who: hug.types.text, why: hug.types.text, what: hug.types.text):
    """
    Serve image to user
    """
    # TODO better text sanitizing
    who = 'The #1  {} excuse'.format(who).upper()
    legit = 'for legitimately slacking off:'.upper()
    why = why.upper()
    what = '{}!'.format(what).upper()

    # ovo je prazna slika, ak se `blank_image` pozove ko zadnji element u skripti, pokaže sliku
    image = Image.open("blank_excuse.png", "r").convert('RGBA')

    size = width, height = image.size
    draw = ImageDraw.Draw(image, 'RGBA')

    who_font = ImageFont.truetype("xkcd-script.ttf", 24)
    legit_font = ImageFont.truetype("xkcd-script.ttf", 24)
    why_font = ImageFont.truetype("xkcd-script.ttf", 22)
    what_font = ImageFont.truetype("xkcd-script.ttf", 20)

    # Y text coordinates are constant
    WHO_TEXT_Y = 12
    LEGIT_TEXT_Y = 38
    WHY_TEXT_Y = 85
    WHAT_TEXT_Y = 220

    # X text coordinates are calculated
    who_text_x = width - (width/2 + who_font.getsize(who)[0]/2)
    legit_text_x = width - (width/2 + legit_font.getsize(legit)[0]/2)
    why_text_x = width - (width/2 + why_font.getsize(why)[0]/2)
    what_text_x = width - (width/2 + what_font.getsize(what)[0]/2) - 25

    draw.text((who_text_x, WHO_TEXT_Y), who, fill=(0, 0 ,0 ,200), font=who_font)
    draw.text((legit_text_x, LEGIT_TEXT_Y), legit, fill=(0, 0 ,0 ,200), font=legit_font)
    draw.text((why_text_x, WHY_TEXT_Y), why, fill=(0, 0 ,0 ,200), font=why_font)
    draw.text((what_text_x, WHAT_TEXT_Y), what, fill=(0, 0, 0, 200), font=what_font)

    buffer = BytesIO()
    image.save(buffer, format="png")
    return image


# _decode_hex(*texts)


# _encode_hex(*texts)
