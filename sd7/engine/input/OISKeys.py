#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project Engine
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#
# NOTICE THIS FILE HAS BEEN AUTOMATICALLY GENERATED FROM OISKeys.h
#  BY USING scripts/keygen.py
#
# ALL CHANGES WILL BE LOST!

__version__ = "$Revision$"

__all__ = ["Key"]


    
class Key(object):

    UNASSIGNED = 0
    ESC = 1
    N1 = 2
    N2 = 3
    N3 = 4
    N4 = 5
    N5 = 6
    N6 = 7
    N7 = 8
    N8 = 9
    N9 = 10
    N0 = 11
    MINUS = 12
    EQUALS = 13
    BACK = 14
    TAB = 15
    Q = 16
    W = 17
    E = 18
    R = 19
    T = 20
    Y = 21
    U = 22
    I = 23
    O = 24
    P = 25
    LBRACKET = 26
    RBRACKET = 27
    RETURN = 28
    LCTRL = 29
    A = 30
    S = 31
    D = 32
    F = 33
    G = 34
    H = 35
    J = 36
    K = 37
    L = 38
    SEMICOLON = 39
    APOSTROPHE = 40
    GRAVE = 41
    LSHIFT = 42
    BACKSLASH = 43
    Z = 44
    X = 45
    C = 46
    V = 47
    B = 48
    N = 49
    M = 50
    COMMA = 51
    PERIOD = 52
    SLASH = 53
    RSHIFT = 54
    MULTIPLY = 55
    LALT = 56
    SPACE = 57
    CAPITAL = 58
    F1 = 59
    F2 = 60
    F3 = 61
    F4 = 62
    F5 = 63
    F6 = 64
    F7 = 65
    F8 = 66
    F9 = 67
    F10 = 68
    NUMLOCK = 69
    SCROLL = 70
    NUMPAD7 = 71
    NUMPAD8 = 72
    NUMPAD9 = 73
    SUBTRACT = 74
    NUMPAD4 = 75
    NUMPAD5 = 76
    NUMPAD6 = 77
    ADD = 78
    NUMPAD1 = 79
    NUMPAD2 = 80
    NUMPAD3 = 81
    NUMPAD0 = 82
    DECIMAL = 83
    OEM_102 = 86
    F11 = 87
    F12 = 88
    F13 = 100
    F14 = 101
    F15 = 102
    KANA = 112
    ABNT_C1 = 115
    CONVERT = 121
    NOCONVERT = 123
    YEN = 125
    ABNT_C2 = 126
    NUMPADEQUALS = 141
    PREVTRACK = 144
    AT = 145
    COLON = 146
    UNDERLINE = 147
    KANJI = 148
    STOP = 149
    AX = 150
    UNLABELED = 151
    NEXTTRACK = 153
    NUMPADENTER = 156
    RCTRL = 157
    MUTE = 160
    CALCULATOR = 161
    PLAYPAUSE = 162
    MEDIASTOP = 164
    VOLUMEDOWN = 174
    VOLUMEUP = 176
    WEBHOME = 178
    NUMPADCOMMA = 179
    DIVIDE = 181
    SYSRQ = 183
    RALT = 184
    PAUSE = 197
    HOME = 199
    UP = 200
    PGUP = 201
    LEFT = 203
    RIGHT = 205
    END = 207
    DOWN = 208
    PGDOWN = 209
    INSERT = 210
    DELETE = 211
    LWIN = 219
    RWIN = 220
    APPS = 221
    POWER = 222
    SLEEP = 223
    WAKE = 227
    WEBSEARCH = 229
    WEBFAVORITES = 230
    WEBREFRESH = 231
    WEBSTOP = 232
    WEBFORWARD = 233
    WEBBACK = 234
    MYCOMPUTER = 235
    MAIL = 236
    MEDIASELECT = 237

    name2keyid = {
        'UNASSIGNED' : 0,
        'ESC' : 1,
        '1' : 2,
        'N1' : 2,
        '2' : 3,
        'N2' : 3,
        '3' : 4,
        'N3' : 4,
        '4' : 5,
        'N4' : 5,
        '5' : 6,
        'N5' : 6,
        '6' : 7,
        'N6' : 7,
        '7' : 8,
        'N7' : 8,
        '8' : 9,
        'N8' : 9,
        '9' : 10,
        'N9' : 10,
        '0' : 11,
        'N0' : 11,
        'MINUS' : 12,
        'EQUALS' : 13,
        'BACK' : 14,
        'TAB' : 15,
        'Q' : 16,
        'W' : 17,
        'E' : 18,
        'R' : 19,
        'T' : 20,
        'Y' : 21,
        'U' : 22,
        'I' : 23,
        'O' : 24,
        'P' : 25,
        'LBRACKET' : 26,
        'RBRACKET' : 27,
        'RETURN' : 28,
        'LCTRL' : 29,
        'A' : 30,
        'S' : 31,
        'D' : 32,
        'F' : 33,
        'G' : 34,
        'H' : 35,
        'J' : 36,
        'K' : 37,
        'L' : 38,
        'SEMICOLON' : 39,
        'APOSTROPHE' : 40,
        'GRAVE' : 41,
        'LSHIFT' : 42,
        'BACKSLASH' : 43,
        'Z' : 44,
        'X' : 45,
        'C' : 46,
        'V' : 47,
        'B' : 48,
        'N' : 49,
        'M' : 50,
        'COMMA' : 51,
        'PERIOD' : 52,
        'SLASH' : 53,
        'RSHIFT' : 54,
        'MULTIPLY' : 55,
        'LALT' : 56,
        'SPACE' : 57,
        'CAPITAL' : 58,
        'F1' : 59,
        'F2' : 60,
        'F3' : 61,
        'F4' : 62,
        'F5' : 63,
        'F6' : 64,
        'F7' : 65,
        'F8' : 66,
        'F9' : 67,
        'F10' : 68,
        'NUMLOCK' : 69,
        'SCROLL' : 70,
        'NUMPAD7' : 71,
        'NUMPAD8' : 72,
        'NUMPAD9' : 73,
        'SUBTRACT' : 74,
        'NUMPAD4' : 75,
        'NUMPAD5' : 76,
        'NUMPAD6' : 77,
        'ADD' : 78,
        'NUMPAD1' : 79,
        'NUMPAD2' : 80,
        'NUMPAD3' : 81,
        'NUMPAD0' : 82,
        'DECIMAL' : 83,
        'OEM_102' : 86,
        'F11' : 87,
        'F12' : 88,
        'F13' : 100,
        'F14' : 101,
        'F15' : 102,
        'KANA' : 112,
        'ABNT_C1' : 115,
        'CONVERT' : 121,
        'NOCONVERT' : 123,
        'YEN' : 125,
        'ABNT_C2' : 126,
        'NUMPADEQUALS' : 141,
        'PREVTRACK' : 144,
        'AT' : 145,
        'COLON' : 146,
        'UNDERLINE' : 147,
        'KANJI' : 148,
        'STOP' : 149,
        'AX' : 150,
        'UNLABELED' : 151,
        'NEXTTRACK' : 153,
        'NUMPADENTER' : 156,
        'RCTRL' : 157,
        'MUTE' : 160,
        'CALCULATOR' : 161,
        'PLAYPAUSE' : 162,
        'MEDIASTOP' : 164,
        'VOLUMEDOWN' : 174,
        'VOLUMEUP' : 176,
        'WEBHOME' : 178,
        'NUMPADCOMMA' : 179,
        'DIVIDE' : 181,
        'SYSRQ' : 183,
        'RALT' : 184,
        'PAUSE' : 197,
        'HOME' : 199,
        'UP' : 200,
        'PGUP' : 201,
        'LEFT' : 203,
        'RIGHT' : 205,
        'END' : 207,
        'DOWN' : 208,
        'PGDOWN' : 209,
        'INSERT' : 210,
        'DELETE' : 211,
        'LWIN' : 219,
        'RWIN' : 220,
        'APPS' : 221,
        'POWER' : 222,
        'SLEEP' : 223,
        'WAKE' : 227,
        'WEBSEARCH' : 229,
        'WEBFAVORITES' : 230,
        'WEBREFRESH' : 231,
        'WEBSTOP' : 232,
        'WEBFORWARD' : 233,
        'WEBBACK' : 234,
        'MYCOMPUTER' : 235,
        'MAIL' : 236,
        'MEDIASELECT' : 237,
    }

    keyid2name = {
        0 : 'UNASSIGNED',
        1 : 'ESC',
        2 : 'N1',
        3 : 'N2',
        4 : 'N3',
        5 : 'N4',
        6 : 'N5',
        7 : 'N6',
        8 : 'N7',
        9 : 'N8',
        10 : 'N9',
        11 : 'N0',
        12 : 'MINUS',
        13 : 'EQUALS',
        14 : 'BACK',
        15 : 'TAB',
        16 : 'Q',
        17 : 'W',
        18 : 'E',
        19 : 'R',
        20 : 'T',
        21 : 'Y',
        22 : 'U',
        23 : 'I',
        24 : 'O',
        25 : 'P',
        26 : 'LBRACKET',
        27 : 'RBRACKET',
        28 : 'RETURN',
        29 : 'LCTRL',
        30 : 'A',
        31 : 'S',
        32 : 'D',
        33 : 'F',
        34 : 'G',
        35 : 'H',
        36 : 'J',
        37 : 'K',
        38 : 'L',
        39 : 'SEMICOLON',
        40 : 'APOSTROPHE',
        41 : 'GRAVE',
        42 : 'LSHIFT',
        43 : 'BACKSLASH',
        44 : 'Z',
        45 : 'X',
        46 : 'C',
        47 : 'V',
        48 : 'B',
        49 : 'N',
        50 : 'M',
        51 : 'COMMA',
        52 : 'PERIOD',
        53 : 'SLASH',
        54 : 'RSHIFT',
        55 : 'MULTIPLY',
        56 : 'LALT',
        57 : 'SPACE',
        58 : 'CAPITAL',
        59 : 'F1',
        60 : 'F2',
        61 : 'F3',
        62 : 'F4',
        63 : 'F5',
        64 : 'F6',
        65 : 'F7',
        66 : 'F8',
        67 : 'F9',
        68 : 'F10',
        69 : 'NUMLOCK',
        70 : 'SCROLL',
        71 : 'NUMPAD7',
        72 : 'NUMPAD8',
        73 : 'NUMPAD9',
        74 : 'SUBTRACT',
        75 : 'NUMPAD4',
        76 : 'NUMPAD5',
        77 : 'NUMPAD6',
        78 : 'ADD',
        79 : 'NUMPAD1',
        80 : 'NUMPAD2',
        81 : 'NUMPAD3',
        82 : 'NUMPAD0',
        83 : 'DECIMAL',
        86 : 'OEM_102',
        87 : 'F11',
        88 : 'F12',
        100 : 'F13',
        101 : 'F14',
        102 : 'F15',
        112 : 'KANA',
        115 : 'ABNT_C1',
        121 : 'CONVERT',
        123 : 'NOCONVERT',
        125 : 'YEN',
        126 : 'ABNT_C2',
        141 : 'NUMPADEQUALS',
        144 : 'PREVTRACK',
        145 : 'AT',
        146 : 'COLON',
        147 : 'UNDERLINE',
        148 : 'KANJI',
        149 : 'STOP',
        150 : 'AX',
        151 : 'UNLABELED',
        153 : 'NEXTTRACK',
        156 : 'NUMPADENTER',
        157 : 'RCTRL',
        160 : 'MUTE',
        161 : 'CALCULATOR',
        162 : 'PLAYPAUSE',
        164 : 'MEDIASTOP',
        174 : 'VOLUMEDOWN',
        176 : 'VOLUMEUP',
        178 : 'WEBHOME',
        179 : 'NUMPADCOMMA',
        181 : 'DIVIDE',
        183 : 'SYSRQ',
        184 : 'RALT',
        197 : 'PAUSE',
        199 : 'HOME',
        200 : 'UP',
        201 : 'PGUP',
        203 : 'LEFT',
        205 : 'RIGHT',
        207 : 'END',
        208 : 'DOWN',
        209 : 'PGDOWN',
        210 : 'INSERT',
        211 : 'DELETE',
        219 : 'LWIN',
        220 : 'RWIN',
        221 : 'APPS',
        222 : 'POWER',
        223 : 'SLEEP',
        227 : 'WAKE',
        229 : 'WEBSEARCH',
        230 : 'WEBFAVORITES',
        231 : 'WEBREFRESH',
        232 : 'WEBSTOP',
        233 : 'WEBFORWARD',
        234 : 'WEBBACK',
        235 : 'MYCOMPUTER',
        236 : 'MAIL',
        237 : 'MEDIASELECT',
    }

    @staticmethod
    def toString(id):
        return Key.keyid2name[id]

    @staticmethod
    def toKeyId(name):
        return Key.name2keyid[name]
    
    