from app import _sanitize_input


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
