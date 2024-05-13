import csv

TOKEN_SPACE = 0b00000000  # 0x00 =>  0
TOKEN_1 = 0b00000001  # 0x01 =>  1
TOKEN_2 = 0b00000010  # 0x02 =>  2
TOKEN_12 = 0b00000011  # 0x03 =>  3
TOKEN_3 = 0b00000100  # 0x04 =>  4
TOKEN_13 = 0b00000101  # 0x05 =>  5
TOKEN_23 = 0b00000110  # 0x06 =>  6
TOKEN_123 = 0b00000111  # 0x07 =>  7
TOKEN_4 = 0b00001000  # 0x08 =>  8
TOKEN_14 = 0b00001001  # 0x09 =>  9
TOKEN_24 = 0b00001010  # 0x0A => 10
TOKEN_124 = 0b00001011  # 0x0B => 11
TOKEN_34 = 0b00001100  # 0x0C => 12
TOKEN_134 = 0b00001101  # 0x0D => 13
TOKEN_234 = 0b00001110  # 0x0E => 14
TOKEN_1234 = 0b00001111  # 0x0F => 15
TOKEN_5 = 0b00010000  # 0x10 => 16
TOKEN_15 = 0b00010001  # 0x11 => 17
TOKEN_25 = 0b00010010  # 0x12 => 18
TOKEN_125 = 0b00010011  # 0x13 => 19
TOKEN_35 = 0b00010100  # 0x14 => 20
TOKEN_135 = 0b00010101  # 0x15 => 21
TOKEN_235 = 0b00010110  # 0x16 => 22
TOKEN_1235 = 0b00010111  # 0x17 => 23
TOKEN_45 = 0b00011000  # 0x18 => 24
TOKEN_145 = 0b00011001  # 0x19 => 25
TOKEN_245 = 0b00011010  # 0x1A => 26
TOKEN_1245 = 0b00011011  # 0x1B => 27
TOKEN_345 = 0b00011100  # 0x1C => 28
TOKEN_1345 = 0b00011101  # 0x1D => 29
TOKEN_2345 = 0b00011110  # 0x1E => 30
TOKEN_12345 = 0b00011111  # 0x1F => 31
TOKEN_6 = 0b00100000  # 0x20 => 32
TOKEN_16 = 0b00100001  # 0x21 => 33
TOKEN_26 = 0b00100010  # 0x22 => 34
TOKEN_126 = 0b00100011  # 0x23 => 35
TOKEN_36 = 0b00100100  # 0x24 => 36
TOKEN_136 = 0b00100101  # 0x25 => 37
TOKEN_236 = 0b00100110  # 0x26 => 38
TOKEN_1236 = 0b00100111  # 0x27 => 39
TOKEN_46 = 0b00101000  # 0x28 => 40
TOKEN_146 = 0b00101001  # 0x29 => 41
TOKEN_246 = 0b00101010  # 0x2A => 42
TOKEN_1246 = 0b00101011  # 0x2B => 43
TOKEN_346 = 0b00101100  # 0x2C => 44
TOKEN_1346 = 0b00101101  # 0x2D => 45
TOKEN_2346 = 0b00101110  # 0x3E => 46
TOKEN_12346 = 0b00101111  # 0x2F => 47
TOKEN_56 = 0b00110000  # 0x30 => 48
TOKEN_156 = 0b00110001  # 0x31 => 49
TOKEN_256 = 0b00110010  # 0x32 => 50
TOKEN_1256 = 0b00110011  # 0x33 => 51
TOKEN_356 = 0b00110100  # 0x34 => 52
TOKEN_1356 = 0b00110101  # 0x35 => 53
TOKEN_2356 = 0b00110110  # 0x36 => 54
TOKEN_12356 = 0b00110111  # 0x37 => 55
TOKEN_456 = 0b00111000  # 0x38 => 56
TOKEN_1456 = 0b00111001  # 0x39 => 57
TOKEN_2456 = 0b00111010  # 0x3A => 58
TOKEN_12456 = 0b00111011  # 0x3B => 59
TOKEN_3456 = 0b00111100  # 0x3C => 60
TOKEN_13456 = 0b00111101  # 0x3D => 61
TOKEN_23456 = 0b00111110  # 0x3E => 62
TOKEN_123456 = 0b00111111  # 0x3F => 63

FR_CHAR_DICT = {
    '*': TOKEN_35,
    '0': TOKEN_3456,
    # Les lettres
    'a': TOKEN_1,
    'b': TOKEN_12,
    'c': TOKEN_14,
    'd': TOKEN_145,
    'e': TOKEN_15,
    'f': TOKEN_124,
    'g': TOKEN_1245,
    'h': TOKEN_125,
    'i': TOKEN_24,
    'j': TOKEN_245,
    'k': TOKEN_13,
    'l': TOKEN_123,
    'm': TOKEN_134,
    'n': TOKEN_1345,
    'o': TOKEN_135,
    'p': TOKEN_1234,
    'q': TOKEN_12345,
    'r': TOKEN_1235,
    's': TOKEN_234,
    't': TOKEN_2345,
    'u': TOKEN_136,
    'v': TOKEN_1236,
    'w': TOKEN_2456,
    'x': TOKEN_1346,
    'y': TOKEN_13456,
    'z': TOKEN_1356,
    # Les accents
    'à': TOKEN_12356,
    'â': TOKEN_16,
    'ç': TOKEN_12346,
    'é': TOKEN_123456,
    'è': TOKEN_2346,
    'ê': TOKEN_126,
    'ë': TOKEN_1246,
    'î': TOKEN_146,
    'ï': TOKEN_12456,
    'œ': TOKEN_246,
    'ô': TOKEN_1456,
    'ù': TOKEN_23456,
    'û': TOKEN_156,
    'ü': TOKEN_1256,
    # La ponctuation
    ' ': TOKEN_SPACE,
    '-': TOKEN_36,
    ',': TOKEN_2,
    ';': TOKEN_23,
    ':': TOKEN_25,
    '.': TOKEN_256,
    '?': TOKEN_26,
    '!': TOKEN_235,
    '"': TOKEN_2356,
    '(': TOKEN_236,
    ')': TOKEN_356,
    '\'': TOKEN_3
}


def codeIntToChar(code: int) -> str:  # 21   ->   'o'
    for _char, _code in FR_CHAR_DICT.items():
        if code == _code:
            return _char


def getPhrase(code: str) -> str:
    for _str, _phrase in PHRASES.items():
        if code == _str:
            return _phrase


# Opens up and returns a CSV file
# This should be used to load a dictionary
def openLesson(name: str) -> csv.DictReader:
    with open(f'{name}.csv', newline='') as f:
        return csv.DictReader(f)


PHRASES = {
    'intro_start': "Connaissez-vous la touche Espace du clavier? Si oui, appuyez sur la touche Espace du clavier, sinon sur n'importe quelle touche.",
    'intro_jeu_1': "Apprenons la touche Espace. La touche Espace du clavier est la grande barre en bas du clavier.  Appuie sur la touche Entrée.",
    'intro_jeu_1_error': "La touche Espace du clavier est la grande barre en bas du clavier.  Appuie sur la touche Entrée.",
    'intro_jeu_2': "Vous connaissez maintenant la touche Entrée. Vous pouvez finir ce dictaticiel en appuyant sur la touche Entree.",
    'intro_jeu_2_error': "Ce n'est pas la touche Entrée. Appuyez sur la touche Entrée, la grande barre en bas du clavier.",
    'intro_jeu_3': "Fin"
}

#'intro_jeu_1': "On va vous apprendre à naviguer dans l'application. La touche Echap du clavier se situe tout en haut à gauche du clavier. Appuie sur la touche Echap.",
#'intro_jeu_1_error': "La touche Echap du clavier se situe tout en haut à gauche du clavier. Appuie sur la touche Echap.",
