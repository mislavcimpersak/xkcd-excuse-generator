"""
XKCD Excuse Generator API created using Hug Framework
"""

from binascii import hexlify, unhexlify, Error as BinAsciiError
from io import BytesIO
import os

from falcon import HTTP_404
import hug
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify


# since base excuse image is fixed, this values are also constant
IMAGE_WIDTH = 413
# Y text coordinates
WHO_TEXT_Y = 12
LEGIT_TEXT_Y = 38
WHY_TEXT_Y = 85
WHAT_TEXT_Y = 220


dir_path = os.path.dirname(os.path.realpath(__file__))


@hug.get(
    versions=1,
    examples='who=programmer&why=my%code%20is%20compiling&what=compiling'
)
def excuse(request, who: hug.types.text='', why: hug.types.text='', what: hug.types.text='') -> dict:
    """
    API view that returns url to rendered image or errors if there were any.

    GET https://function.xkcd-excuse.com/api/v1/?who=one&why=two&what=three
    >>
    {
        "errors": {
            "code": 1001,
            "text": "first text two long"  // možda onda imati validaciju pokraj inputa
        }
        "data": {
            "who": "one",
            "why": "two",
            "what": "three",
            "image_url": "function.xkcd-excuse.com/media/<hash>-<hash>-<hash>.png"
        }
    }

    :param request: request object
    :param who: who's excuse
    :param why: what is the excuse
    :param what: what are they saying

    :returns: data dict with url to image or with errors
    """
    who, why, what = _sanitize_input(who), _sanitize_input(why), _sanitize_input(what)

    image = get_excuse_image(who, why, what)

    if isinstance(image, Image.Image):
        who_hex, why_hex, what_hex = _encode_hex(who, why, what)
        image_url = '{scheme}://{domain}/media/{who}-{why}-{what}.png'.format(
            scheme=request.scheme,
            domain=request.netloc,
            who=who_hex,
            why=why_hex,
            what=what_hex
        )
        return {
            'data': {
                'image_url': image_url,
            }
        }
    else:
        return {
            'errors': image
        }


@hug.local()
@hug.get(
    '/media/{who_hex}-{why_hex}-{what_hex}.png',
    output=hug.output_format.png_image,
    examples='/'
)
def img(response, who_hex: hug.types.text, why_hex: hug.types.text, what_hex: hug.types.text):
    """
    Media image view that displays image directly from app.
    """
    try:
        who, why, what = _decode_hex(who_hex, why_hex, what_hex)
    except (BinAsciiError, UnicodeDecodeError):
        raise hug.HTTPError(HTTP_404, 'message', 'invalid image path')

    image = get_excuse_image(who, why, what)

    if isinstance(image, Image.Image):
        return image
    else:
        raise hug.HTTPError(HTTP_404, 'message', 'invalid image path')


def get_excuse_image(who: str, why: str, what: str) -> (Image, list):
    """
    Load excuse template and write on it.
    If there are errors (some text too long), return list of errors.

    :param who: who's excuse
    :param why: what is the excuse
    :param what: what are they saying

    :returns: pillow Image object with excuse written on it
    """
    errors = []

    who = 'The #1  {} excuse'.format(who).upper()
    legit = 'for legitimately slacking off:'.upper()
    why = '"{}."'.format(why)
    what = '{}!'.format(what)

    who_font = _get_text_font(24)
    legit_font = _get_text_font(24)
    why_font = _get_text_font(22)
    what_font = _get_text_font(20)

    errors = _check_user_input_size(errors, IMAGE_WIDTH, who, who_font, 1001)
    errors = _check_user_input_size(errors, IMAGE_WIDTH, why, why_font, 1002)
    errors = _check_user_input_size(errors, 100, what, what_font, 1003)

    if errors:
        return errors

    # in the beginning this is an image without an excuse
    image = Image.open(os.path.join(dir_path, 'blank_excuse.png'), 'r')\
        .convert('RGBA')
    draw = ImageDraw.Draw(image, 'RGBA')

    draw.text((_get_text_x_position(IMAGE_WIDTH, who, who_font), WHO_TEXT_Y),
        who, fill=(0, 0, 0, 200), font=who_font)
    draw.text((_get_text_x_position(IMAGE_WIDTH, legit, legit_font), LEGIT_TEXT_Y),
        legit, fill=(0, 0, 0, 200), font=legit_font)
    draw.text((_get_text_x_position(IMAGE_WIDTH, why, why_font), WHY_TEXT_Y),
        why, fill=(0, 0, 0, 200), font=why_font)
    draw.text((_get_text_x_position(IMAGE_WIDTH, what, what_font, 25), WHAT_TEXT_Y),
        what, fill=(0, 0, 0, 200), font=what_font)

    buffer = BytesIO()
    image.save(buffer, format="png")
    return image


def _get_text_font(size: int) -> ImageFont:
    """
    Loads font and sets font size for text on image

    :param size: font size

    :returns: ImageFont object with desired font size set
    """
    return ImageFont.truetype('xkcd-script.ttf', size)


def _check_user_input_size(errors: list, max_width: float, text: str,
    text_font: ImageFont, error_code: int) -> list:
    """
    Checks if user input size can actually fit in image.
    If not, add an error to existing list of errors.

    :param errors: list of errors
    :param max_width: max size of text
    :param text: user's input
    :param error_code: internal error code

    :returns: list of errors
    """
    if text_font.getsize(text)[0] > max_width:
        errors.append({
            'code': error_code,
            'message': 'Text too long.'
        })
    return errors


def _get_text_x_position(image_width: int, text: str, text_font: ImageFont, offset: int=None) -> float:
    """
    Calculate starting X coordinate for given text and text size.

    :param text: user's text
    :param text_font:
    :param offset: how much to move from center of the image to the right

    :returns: text's X coordinate
    """
    offset = 0 if offset is None else offset
    return image_width - (image_width / 2 + text_font.getsize(text)[0] / 2) - offset


def _sanitize_input(input: str) -> str:
    """
    Sanitizing input so that it can be hexlifyied.
    Removes extra spacing, slugifies all non-ascii chars, makes everything
    uppercase.

    :param input: dirty user input from get param

    :returns: cleaned user input
    """
    return slugify(input.strip(' .'), separator=' ').upper()


def _decode_hex(*texts) -> list:
    """
    Transforms all attrs to regular (human-readable) strings.

    :param texts: list of strings to be decoded

    :returns: list of hex encoded strings
    """
    return [unhexlify(text).decode() for text in texts]


def _encode_hex(*texts) -> list:
    """
    Transforms all attrs to hex encoded strings.

    :param texts: list of string to be encoded

    :returns: list of hex values
    """
    return [hexlify(bytes(text, 'utf-8')).decode() for text in texts]
