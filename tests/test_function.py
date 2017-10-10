from falcon import HTTP_404
import hug

import app
from app import img, _get_text_font, _sanitize_input, _decode_hex, _encode_hex


def test_img__bad_hex():
    response = hug.test.get(app, '/media/30-30-3z.png')
    assert response.status == HTTP_404

    response = hug.test.get(app, '/media/aaaa-30-30.png')
    assert response.status == HTTP_404


def test_get_text_font():
    font = _get_text_font(20)
    assert font.size == 20

    font = _get_text_font(20)
    assert font.font.family == 'xkcd Script'


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
