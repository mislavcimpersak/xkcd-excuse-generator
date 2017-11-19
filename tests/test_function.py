from falcon import HTTP_200, HTTP_400, HTTP_404
import hug
from PIL import Image

import app
from app import (
    get_excuse_image,
    _get_text_font,
    _get_text_x_position,
    _sanitize_input,
    _decode_hex,
    _encode_hex
)


def test_excuse__success():
    OUTPUT = {
        'data': {
            'image_url': 'http://falconframework.org/media/30-30-30.png'
        }
    }
    response = hug.test.get(app, '/v1/excuse/', {'who': '0', 'why': '0', 'what': '0'})

    assert response.status == HTTP_200
    assert response.data == OUTPUT


def test_excuse__who_too_long():
    ERROR_CODE = 1011
    response = hug.test.get(app, '/v1/excuse/', {'who': 'programmerprogrammer', 'why': '0', 'what': '0'})

    assert response.status == HTTP_400
    assert response.data['errors'][0]['code'] == ERROR_CODE


def test_excuse__why_too_long():
    ERROR_CODE = 1021
    response = hug.test.get(app, '/v1/excuse/', {'who': '0', 'why': 'my code is compiling my code is compiling ', 'what': '0'})

    assert response.status == HTTP_400
    assert response.data['errors'][0]['code'] == ERROR_CODE


def test_excuse__what_too_long():
    ERROR_CODE = 1031
    response = hug.test.get(app, '/v1/excuse/', {'who': '0', 'why': '0', 'what': 'compilingcompiling'})

    assert response.status == HTTP_400
    assert response.data['errors'][0]['code'] == ERROR_CODE


def test_img__bad_hex():
    response = hug.test.get(app, '/media/30-30-3z.png')
    assert response.status == HTTP_404

    response = hug.test.get(app, '/media/aaaa-30-30.png')
    assert response.status == HTTP_404


def test_img__text_too_long():
    response = hug.test.get(app, '/media/30-30-434f4d50494c494e47434f4d50494c494e47.png')
    assert response.status == HTTP_404


def test_img__success():
    response = hug.test.get(app, '/media/30-30-30.png')
    assert response.status == HTTP_200
    assert response.content_type == 'image/png'


def test_get_excuse_image__success():
    data = get_excuse_image('programmer', 'my code is compiling', 'compiling')
    assert isinstance(data, Image.Image)
    assert data.size == (413, 360)


def test_get_excuse_image__who_too_long():
    ERROR_CODE = 1011
    data = get_excuse_image('programmerprogrammerprogrammer', 'a', 'a')
    assert data[0]['code'] == ERROR_CODE


def test_get_excuse_image__why_too_long():
    ERROR_CODE = 1021
    data = get_excuse_image('a', 'my code is compiling my code is compiling my code is compiling', 'a')
    assert data[0]['code'] == ERROR_CODE


def test_get_excuse_image__what_too_long():
    ERROR_CODE = 1031
    data = get_excuse_image('a', 'a', 'compilingcompilingcompiling')
    assert data[0]['code'] == ERROR_CODE


def test_get_text_font():
    font = _get_text_font(20)
    assert font.size == 20

    font = _get_text_font(20)
    assert font.font.family == 'xkcd Script'


def test_get_text_x_position__no_text_no_offset():
    font = _get_text_font(20)
    result = _get_text_x_position(200, '', font)

    assert result == 100


def test_get_text_x_position__with_text_no_offset():
    font = _get_text_font(20)
    result = _get_text_x_position(200, 'AAAAAA', font)

    assert result == 67


def test_get_text_x_position__no_text_with_offset():
    font = _get_text_font(20)
    result = _get_text_x_position(200, '', font, 20)

    assert result == 80


def test_get_text_x_position__with_text_with_offset():
    font = _get_text_font(20)
    result = _get_text_x_position(200, 'AAAAAA', font, 20)

    assert result == 47


def test_sanitize_input__simple():
    INPUT = 'programmer'
    OUTPUT = 'PROGRAMMER'
    assert _sanitize_input(INPUT) == OUTPUT


def test_sanitize_input__non_ascii():
    INPUT = 'čovjek'
    OUTPUT = 'COVJEK'
    assert _sanitize_input(INPUT) == OUTPUT


def test_sanitize_input__extra_spacing():
    INPUT = ' programmer  '
    OUTPUT = 'PROGRAMMER'
    assert _sanitize_input(INPUT) == OUTPUT


def test_sanitize_input__sentence():
    INPUT = 'my code is compiling'
    OUTPUT = 'MY CODE IS COMPILING'
    assert _sanitize_input(INPUT) == OUTPUT


def test_sanitize_input__sentence_extra_spacing_non_ascii():
    INPUT = '  my code is compiling čovječe'
    OUTPUT = 'MY CODE IS COMPILING COVJECE'
    assert _sanitize_input(INPUT) == OUTPUT


def test_decode_hex():
    INPUT_1 = '50524f4752414d4d4552'
    INPUT_2 = '4d5920434f444520495320434f4d50494c494e47'
    INPUT_3 = '434f4d50494c494e47'

    OUTPUT_1 = 'PROGRAMMER'
    OUTPUT_2 = 'MY CODE IS COMPILING'
    OUTPUT_3 = 'COMPILING'

    assert _decode_hex(INPUT_1, INPUT_2, INPUT_3) == [
        OUTPUT_1, OUTPUT_2, OUTPUT_3]


def test_encode_hex():
    INPUT_1 = 'PROGRAMMER'
    INPUT_2 = 'MY CODE IS COMPILING'
    INPUT_3 = 'COMPILING'

    OUTPUT_1 = '50524f4752414d4d4552'
    OUTPUT_2 = '4d5920434f444520495320434f4d50494c494e47'
    OUTPUT_3 = '434f4d50494c494e47'

    assert _encode_hex(INPUT_1, INPUT_2, INPUT_3) == [
        OUTPUT_1, OUTPUT_2, OUTPUT_3]
