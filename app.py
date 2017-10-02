from io import BytesIO
import os

from PIL import Image, ImageDraw, ImageFont
from flask import Flask, send_file
from flask import request

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route('/blank', methods=['GET'])
def blank():
    """
    Serves blank image.
    """
    with open(os.path.join(dir_path, 'blank_excuse.png'), 'rb') as buffer:
        return send_file(BytesIO(buffer.read()), mimetype='image/png')


@app.route('/', methods=['GET'])
def root():
    """
    If `first_text` and `second_text` are sent as GET parameters those text
    will be written on a blank XKCD excuse image.

    This needs a LOT of work. Created in a rush without any proper thought
    given about code quality :'(
    """
    first_text = request.args.get('first_text')
    second_text = request.args.get('second_text')

    if not first_text or not second_text:
        # TODO
        example_url = '{}?first_text=my%20function%20is%20uploading%20to%20aws&second_text=uploading'.format(request.url)
        return (
            'Usage: just add GET parameters `first_text` & `second_text` with desired text to the current URL ;)'
            '<br/><br/><br/> ie. &nbsp;'
            '<a href="{0}">{0}</a>'.format(example_url)
        )

    first_text = '"{}"'.format(first_text.upper())
    second_text = '{}!'.format(second_text.strip('!').upper())

    # in the beginning this is an empty image
    image = Image.open(os.path.join(dir_path, 'blank_excuse.png'), 'r')\
        .convert('RGBA')

    size = width, height = image.size
    draw = ImageDraw.Draw(image, 'RGBA')
    first_font = ImageFont.truetype(os.path.join(dir_path, 'xkcd-script.ttf'), 22)
    second_font = ImageFont.truetype(os.path.join(dir_path, 'xkcd-script.ttf'), 20)

    if first_font.getsize(first_text)[0] > width:
        return 'First text too long'

    if second_font.getsize(second_text)[0] > 100:
        return 'Second text too long'

    # Y coordinates are constant
    FIRST_TEXT_Y = 85
    SECOND_TEXT_Y = 220

    first_text_x = width - (width / 2 + first_font.getsize(first_text)[0] / 2)
    second_text_x = width - (width / 2 + second_font.getsize(second_text)[0] / 2) - 25

    draw.text((first_text_x, FIRST_TEXT_Y), first_text, fill=(0, 0 ,0 ,200), font=first_font)
    draw.text((second_text_x, SECOND_TEXT_Y), second_text, fill=(0, 0, 0, 200), font=second_font)

    buffer = BytesIO()
    image.save(buffer, format="PNG", quality=85, optimize=True)
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
