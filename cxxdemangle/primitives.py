# cxxdemangle (c) Nikolas Wipper 2022

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .constants import operator_names, ctor_dtor_names

def demangle_number(mangled):
    num = ""
    if mangled[0] == "n":
        num = "-"
        mangled = mangled[1:]
    while mangled[0].isnumeric():
        num += mangled[0]
        mangled = mangled[1:]
    return num, mangled


def demangle_unsigned(mangled):
    num = ""
    while mangled[0].isnumeric():
        num += mangled[0]
        mangled = mangled[1:]
    return num, mangled


def does_source_name_come_next(mangled):
    if not mangled:
        return False
    if mangled[0] == "n":
        mangled = mangled[1:]
    return mangled[0].isnumeric()


def demangle_source_name(mangled):
    length, mangled = demangle_number(mangled)
    length = int(length)
    return mangled[:length], mangled[length:]


def does_unqualified_name_come_next(mangled):
    if mangled[:2] in operator_names:
        return True
    if mangled[:2] in ctor_dtor_names:
        return True
    return does_source_name_come_next(mangled)


def demangle_unqualified_name(mangled):
    if mangled[:2] in operator_names:
        return operator_names[mangled[:2]], mangled[2:]
    if mangled[:2] in ctor_dtor_names:
        return ctor_dtor_names[mangled[:2]], mangled[2:]
    if does_source_name_come_next(mangled):
        return demangle_source_name(mangled)
    return "", mangled