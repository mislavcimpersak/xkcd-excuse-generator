from app import _sanitize_input
from app import img, _get_text_font, _sanitize_input, _decode_hex, _encode_hex



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
