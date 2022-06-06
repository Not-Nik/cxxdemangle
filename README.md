# cxxdemangle
Demangling C++ names from the Itanium ABI

## Example usage
```python
from cxxdemangle import demangle

mangled = input("Mangled name: ")
demangled = demangle(mangled)

print(demangled)
```

## Supported mangling parts
Currently supported:
 - Unscoped names
 - Nested names
 - Template arguments/parameters
 - Most type variations
 - Abbreviations for operator overloading

Currently unsupported:
 - Expressions
 - Abbreviations for STL classes
 - Pointer to member type
 - Special names such as virtual table's and typeinfo's

Currently untested:
 - Constructors
 - Destructors
 - Advanced templating
 - Advanced nested names
