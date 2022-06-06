from cxxdemangle import demangle


def test(mangled, expected):
    result = demangle(mangled)
    if result != expected:
        print("Failed to demangle " + mangled + ". Expected " + expected + ", but got " + result)
    else:
        print("Successfully demangled " + mangled + " into " + result)


if __name__ == "__main__":
    test("f", "f")
    test("_Z1fv", "f(void)")
    test("_Z1fi", "f(int)")
    test("_Z3foo3bar", "foo(bar)")
    test("_Zrm1XS_", "operator %(X, X)")
    test("_ZplR1XS0_", "operator +(X &, X &)")
    test("_ZlsRK1XS1_", "operator <<(const X &, const X &)")
    test("_ZN3FooIA4_iE3barE", "Foo<int[4]>::bar()")
    test("_Z1fIiEvi", "void f<int>(int)")
    test("_Z5firstI3DuoEvS0_", "void first<Duo>(Duo)")
    test("_Z5firstI3DuoEvT_", "void first<Duo>(Duo)")
    test("_Z3fooIiPFidEiEvv", "void foo<int, int(*)(double), int>(void)")
    test("_ZN1N1fE", "N::f()")
    test("_ZN6System5Sound4beepEv", "System::Sound::beep()")
    test("_ZN5Arena5levelE", "Arena::level()")
    test("_ZN5StackIiiE5levelE", "Stack<int, int>::level()")
    test("_Z1fI1XEvPVN1AIT_E1TE", "void f<X>(volatile A<X>::T *)")
    # Doesn't work because expressions are not supported yet
    # test("_ZngILi42EEvN1AIXplT_Li2EEE1TE", "void operator-<42>(A<(42)+(2)>::T)")
    test("_Z4makeI7FactoryiET_IT0_Ev", "Factory<int> make<Factory, int>(void)")
    test("_Z3foo5Hello5WorldS0_S_", "foo(Hello, World, World, Hello)")
