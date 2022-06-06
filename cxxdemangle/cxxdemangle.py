# cxxdemangle (c) Nikolas Wipper 2022

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .constants import builtin_types, abbreviations
from .primitives import demangle_unsigned, does_source_name_come_next, demangle_source_name, does_unqualified_name_come_next, demangle_unqualified_name

# This is filled on runtime
# Fuck thread safety
subs = []
# Same here, just that these are only types
temp_subs = []
# Set to tell whether a return type is encoded
has_return = False


def does_sequence_id_come_next(mangled):
    return mangled.startswith("S")


def demangle_sequence_id(mangled):
    if does_sequence_id_come_next(mangled):
        mangled = mangled[1:]
        num, mangled = demangle_unsigned(mangled)
        if num == '':
            num = "-1"
        num = int(num, 36) + 1
        if mangled.startswith("_"):
            return subs[num], mangled[1:]
    return "", mangled


def does_template_param_come_next(mangled):
    return mangled.startswith("T")


def demangle_template_param(mangled):
    mangled = mangled[1:]
    num, mangled = demangle_unsigned(mangled)
    if num == '':
        num = "-1"
    num = int(num, 36) + 1
    if mangled.startswith("_"):
        return temp_subs[num], mangled[1:]
    return "", mangled


def does_template_arg_come_next(mangled):
    return does_type_come_next(mangled) or mangled.startswith("X")


def demangle_template_arg(mangled):
    if does_type_come_next(mangled):
        return demangle_type(mangled)
    return "", mangled


def do_template_args_come_next(mangled):
    return mangled != '' and mangled[0] == "I"


def demangle_template_args(mangled):
    global has_return, temp_subs
    old_return = has_return
    mangled = mangled[1:]
    temp_args = []

    while does_template_arg_come_next(mangled):
        has_return = True
        temp_arg, mangled = demangle_template_arg(mangled)
        if temp_arg == '':
            break
        temp_args.append(temp_arg)

    if not temp_args:
        has_return = old_return
        temp_args, mangled = demangle_template_param(mangled)
        if mangled[0] != 'E' and does_template_param_come_next(mangled):
            return "", mangled
        mangled = mangled[1:]
        temp_args = "<" + temp_args + ">"
        return temp_args, mangled

    if mangled[0] != "E":
        return "", mangled
    mangled = mangled[1:]

    temp_subs = temp_args
    subs.extend(temp_args)

    return "<" + ", ".join(temp_args) + ">", mangled


def demangle_prefix_part(mangled):
    if mangled[:2] in abbreviations:
        return abbreviations[mangled[:2]], mangled[2:]
    if does_sequence_id_come_next(mangled):
        return demangle_sequence_id(mangled)
    if does_unqualified_name_come_next(mangled):
        return demangle_unqualified_name(mangled)
    if does_template_param_come_next(mangled):
        return demangle_template_param(mangled)
    return "", mangled


def does_prefix_come_next(mangled):
    return does_sequence_id_come_next(mangled) or does_unqualified_name_come_next(mangled) or mangled[:2] in abbreviations


def demangle_prefix(mangled):
    names = []

    while does_prefix_come_next(mangled):
        name, mangled = demangle_prefix_part(mangled)
        if name == '':
            break
        if do_template_args_come_next(mangled):
            temp_args, mangled = demangle_template_args(mangled)
            name += temp_args
        names.append(name)

    return "::".join(names), mangled


def demangle_cv_qualifiers(mangled):
    qualifiers = []
    char = mangled[0]
    while char in ["r", "V", "K"]:
        if char == "r" and "restrict" not in qualifiers:
            qualifiers.append("restrict")
        elif char == "V" and "volatile" not in qualifiers:
            qualifiers.append("volatile")
        elif char == "K" and "const" not in qualifiers:
            qualifiers.append("const")
        mangled = mangled[1:]
        char = mangled[0]
    return " ".join(qualifiers), mangled


def demangle_nested_name(mangled):
    name, mangled = demangle_cv_qualifiers(mangled)
    if name != '':
        name += " "

    path, mangled = demangle_prefix(mangled)
    name += path

    return name, mangled


def demangle_unscoped_name(mangled):
    name = ""
    if mangled.startswith("St"):
        name = "::std::"
        mangled = mangled[2:]
    unq_name, mangled = demangle_unqualified_name(mangled)
    name += unq_name

    if do_template_args_come_next(mangled):
        temp_args, mangled = demangle_template_args(mangled)
        name += temp_args

    return name, mangled


def demangle_name(mangled):
    if mangled.startswith("N"):
        name, mangled = demangle_nested_name(mangled[1:])
    else:
        name, mangled = demangle_unscoped_name(mangled)

    return name, mangled


def does_builtin_type_come_next(mangled):
    return mangled[0] in builtin_types or (mangled[0] == "u" and does_source_name_come_next(mangled))


def demangle_builtin_type(mangled):
    if mangled[0] in builtin_types:
        return builtin_types[mangled[0]], mangled[1:]
    if mangled[0] == "u":
        return demangle_source_name(mangled[1:])
    return "", mangled


def demangle_type_qualifiers(mangled):
    qualifiers = []
    char = mangled[0]
    while char in ["P", "R", "C", "G", "U"]:
        if char == "P":
            qualifiers.append("*")
        elif char == "R":
            qualifiers.append("&")
        elif char == "C":
            qualifiers.append("_Complex")
        elif char == "G":
            qualifiers.append("imaginary")
        elif char == "U":
            source_name, mangled = demangle_source_name(mangled)
            qualifiers.append(source_name)
        mangled = mangled[1:]
        char = mangled[0]
    return " ".join(qualifiers), mangled


def demangle_type_name(mangled):
    name, mangled = demangle_builtin_type(mangled)
    if name == '':
        name, mangled = demangle_name(mangled)
    if name == '':
        name, mangled = demangle_sequence_id(mangled)
    return name, mangled


def does_array_type_come_next(mangled):
    return mangled[0] == "A"


def demangle_array_type(mangled):
    mangled = mangled[1:]
    num, mangled = demangle_unsigned(mangled)
    if mangled[0] != "_":
        return "", mangled
    mangled = mangled[1:]
    element, mangled = demangle_type(mangled)
    return element + "[" + num + "]", mangled


def does_function_type_come_next(mangled):
    return mangled.startswith("PF")


def demangle_function_type(mangled):
    global has_return

    mangled = mangled[2:]
    func_type = ""
    if mangled[0] == "Y":
        func_type = "extern \"C\" "
        mangled = mangled[1:]

    old_return = has_return
    has_return = True

    sign, mangled, ret_type = demangle_bare_function_type(mangled)
    func_type += ret_type + "(*)(" + sign + ")"

    has_return = old_return

    if mangled[0] != "E":
        return "", mangled

    mangled = mangled[1:]

    return func_type, mangled


def does_type_come_next(mangled):
    return mangled[0] in ["P", "R", "C", "G", "U", "r", "V", "K", "A"] or does_builtin_type_come_next(mangled) or \
           does_sequence_id_come_next(mangled) or does_source_name_come_next(mangled) or does_function_type_come_next(mangled)


def demangle_type(mangled):
    save_sub = False

    if does_function_type_come_next(mangled):
        name, mangled = demangle_function_type(mangled)
    else:
        qualifiers, mangled = demangle_type_qualifiers(mangled)

        name, mangled = demangle_cv_qualifiers(mangled)
        if name != '':
            name += " "
            save_sub = True

        if does_array_type_come_next(mangled):
            type_name, mangled = demangle_array_type(mangled)
        elif does_template_param_come_next(mangled):
            type_name, mangled = demangle_template_param(mangled)
        else:
            type_name, mangled = demangle_type_name(mangled)

        subs.append(type_name)
        name += type_name

        if do_template_args_come_next(mangled):
            temp_args, mangled = demangle_template_args(mangled)
            name += temp_args

        if save_sub:
            subs.append(name)

        if qualifiers != '':
            name += " " + qualifiers
            subs.append(name)

    return name, mangled


def demangle_bare_function_type(mangled):
    arguments = []

    if has_return:
        ret_type, mangled = demangle_type(mangled)
    else:
        ret_type = ""

    while mangled != '':
        loc_type, mangled = demangle_type(mangled)
        if loc_type == '':
            break
        arguments.append(loc_type)
    return ", ".join(arguments), mangled, ret_type


def demangle(mangled):
    global subs, temp_subs, has_return
    subs = []
    temp_subs = []
    has_return = False
    if not mangled.startswith("_Z"):
        return mangled
    mangled = mangled[2:]  # Remove first two chars i.e. "_Z"
    name, mangled = demangle_name(mangled)
    function_type, mangled, ret_type = demangle_bare_function_type(mangled)
    if ret_type != '':
        ret_type += " "

    return ret_type + name + "(" + function_type + ")"
