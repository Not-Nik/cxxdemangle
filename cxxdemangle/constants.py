# cxxdemangle (c) Nikolas Wipper 2022

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

operator_names = {
    "nw": "operator new",
    "na": "operator new[]",
    "dl": "operator delete",
    "da": "operator delete[]",
    "ps": "operator +",
    "ng": "operator - (unary)",
    "ad": "operator & (unary)",
    "de": "operator * (unary)",
    "co": "operator ~",
    "pl": "operator +",
    "mi": "operator -",
    "ml": "operator *",
    "dv": "operator /",
    "rm": "operator %",
    "an": "operator &",
    "or": "operator |",
    "eo": "operator ^",
    "aS": "operator =",
    "pL": "operator +=",
    "mI": "operator -=",
    "mL": "operator *=",
    "dV": "operator /=",
    "rM": "operator %=",
    "aN": "operator &=",
    "oR": "operator |=",
    "eO": "operator ^=",
    "ls": "operator <<",
    "rs": "operator >>",
    "lS": "operator <<=",
    "rS": "operator >>=",
    "eq": "operator ==",
    "ne": "operator !=",
    "lt": "operator <",
    "gt": "operator >",
    "le": "operator <=",
    "ge": "operator >=",
    "nt": "operator !",
    "aa": "operator &&",
    "oo": "operator ||",
    "pp": "operator ++",
    "mm": "operator --",
    "cm": "operator ,",
    "pm": "operator ->*",
    "pt": "operator ->",
    "cl": "operator ()",
    "ix": "operator []",
    "qu": "operator ?",
    "st": "sizeof (a type)",
    "sz": "sizeof (an expression)", 
}

ctor_dtor_names = {
    "C1": "complete constructor",
    "C2": "base constructore",
    "C3": "allocating constructor",
    "D0": "deleting destructor",
    "D1": "complete destructor",
    "D2": "base destructor"
}

builtin_types = {
    "v": "void",
    "w": "wchar_t",
    "b": "bool",
    "c": "char",
    "a": "signed char",
    "h": "unsigned char",
    "s": "short",
    "t": "unsigned short",
    "i": "int",
    "j": "unsigned int",
    "l": "long",
    "m": "unsigned long",
    "x": "long long",
    "y": "unsigned long long",
    "n": "__int128",
    "o": "unsigned __int128",
    "f": "float",
    "d": "double",
    "e": "long double",
    "g": "__float128",
    "z": "ellipsis"
}

abbreviations = {
    "St": "::std"
}
