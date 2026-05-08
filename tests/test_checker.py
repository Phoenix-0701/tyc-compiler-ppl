"""
Test cases for TyC Static Semantic Checker

This module contains test cases for the static semantic checker.
100 test cases covering all error types and comprehensive scenarios.
"""

from tests.utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)


# ============================================================================
# Valid Programs (test_001 - test_010)
# ============================================================================


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_002():
    """Test valid program with auto type inference"""
    source = """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_003():
    """Test valid program with functions"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_004():
    """Test valid program with struct"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_005():
    """Test valid program with nested blocks"""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test valid program with auto type inferred from function return"""
    source = """
    auto get_value() { return 100; }
    void main() {
        auto x = get_value();
        int y = x + 5;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_007():
    """Test valid program with nested structs"""
    source = """
    struct Engine { int hp; };
    struct Car { Engine eng; };
    void main() {
        Car myCar;
        myCar.eng.hp = 500;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_008():
    """Test valid loop control flow"""
    source = """
    void main() {
        for (int i = 0; i < 10; ++i) {
            if (i == 5) { break; }
            continue;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_009():
    """Test valid usage of built-in functions"""
    source = """
    void main() {
        int x = readInt();
        printFloat(3.14);
        printString("hello");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_010():
    """Test valid chained assignments"""
    source = """
    void main() {
        int x; int y; int z;
        x = y = z = 10;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_011():
    """Test error: Redeclared variable in same block"""
    source = """
    void main() {
        int x = 5;
        float x = 3.14;
    }
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_012():
    """Test error: Local variable shadowing parameter (Not allowed in TyC)"""
    source = """
    void foo(int x) {
        {
            int x = 5;
        }
    }
    void main() {}
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected


def test_013():
    """Test error: Redeclared function"""
    source = """
    void foo() {}
    int foo() { return 1; }
    void main() {}
    """
    expected = "Redeclared(Function, foo)"
    assert Checker(source).check_from_source() == expected


def test_014():
    """Test error: Redeclared struct"""
    source = """
    struct Point { int x; };
    struct Point { float y; };
    void main() {}
    """
    expected = "Redeclared(Struct, Point)"
    assert Checker(source).check_from_source() == expected


def test_015():
    """Test error: Redeclared member in struct"""
    source = """
    struct Point {
        int x;
        float x;
    };
    void main() {}
    """
    expected = "Redeclared(Member, x)"
    assert Checker(source).check_from_source() == expected


def test_016():
    """Test error: Redeclared parameter"""
    source = """
    void foo(int a, float a) {}
    void main() {}
    """
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected


def test_017():
    """Test error: Undeclared identifier"""
    source = """
    void main() {
        int x = y + 1;
    }
    """
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected


def test_018():
    """Test error: Undeclared function"""
    source = """
    void main() {
        bar();
    }
    """
    expected = "UndeclaredFunction(bar)"
    assert Checker(source).check_from_source() == expected


def test_019():
    """Test error: Undeclared struct"""
    source = """
    void main() {
        Car myCar;
    }
    """
    expected = "UndeclaredStruct(Car)"
    assert Checker(source).check_from_source() == expected


def test_020():
    """Test error: Out of scope access"""
    source = """
    void main() {
        {
            int a = 5;
        }
        int b = a;
    }
    """
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected


def test_021():
    """Test error: TypeCannotBeInferred on binary operation with autos"""
    source = """
    void main() {
        auto x; auto y;
        auto z = x + y;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))"
    assert Checker(source).check_from_source() == expected


def test_022():
    """Test error: TypeCannotBeInferred on assignment"""
    source = """
    void main() {
        auto a; auto b;
        a = b;
    }
    """
    expected = "TypeCannotBeInferred(AssignExpr(Identifier(a) = Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_023():
    """Test error: TypeCannotBeInferred on return"""
    source = """
    auto func() {
        auto x;
        return x;
    }
    void main() {}
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return Identifier(x)))"
    assert Checker(source).check_from_source() == expected


def test_024():
    """Test error: TypeCannotBeInferred on relational op"""
    source = """
    void main() {
        auto x; auto y;
        int z = x > y;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), >, Identifier(y)))"
    assert Checker(source).check_from_source() == expected


def test_025():
    """Test error: TypeCannotBeInferred on prefix op"""
    source = """
    void main() {
        auto a;
        int b = !a;
    }
    """
    expected = "TypeCannotBeInferred(PrefixOp(!Identifier(a)))"
    assert Checker(source).check_from_source() == expected


def test_026():
    """Test error: TypeMismatchInStatement in if condition"""
    source = """
    void main() {
        if ("hello") {}
    }
    """
    expected = "TypeMismatchInStatement(IfStmt(if StringLiteral('hello') then BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_027():
    """Test error: TypeMismatchInStatement in while condition"""
    source = """
    void main() {
        while (3.14) {}
    }
    """
    expected = "TypeMismatchInStatement(WhileStmt(while FloatLiteral(3.14) do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_028():
    """Test error: TypeMismatchInStatement in variable declaration"""
    source = """
    void main() {
        int x = 3.14;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_029():
    """Test error: TypeMismatchInStatement in void return"""
    source = """
    void main() {
        return 5;
    }
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected


def test_030():
    """Test error: TypeMismatchInStatement in for condition"""
    source = """
    void main() {
        for (int i = 0; 3.14; ++i) {}
    }
    """
    expected = "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); FloatLiteral(3.14); PrefixOp(++Identifier(i)) do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_031():
    """Test error: TypeMismatchInExpression arithmetic with string"""
    source = """
    void main() {
        int x = 5 + "str";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(5), +, StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected


def test_032():
    """Test error: TypeMismatchInExpression modulo with float"""
    source = """
    void main() {
        int x = 5 % 3.0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(5), %, FloatLiteral(3.0)))"
    assert Checker(source).check_from_source() == expected


def test_033():
    """Test error: TypeMismatchInExpression logical NOT on float"""
    source = """
    void main() {
        int x = !3.14;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(!FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_034():
    """Test error: TypeMismatchInExpression incrementing string"""
    source = """
    void main() {
        string s = "s";
        ++s;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(++Identifier(s)))"
    assert Checker(source).check_from_source() == expected


def test_035():
    """Test error: MustInLoop for break outside loop"""
    source = """
    void main() {
        break;
    }
    """
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected


# def test_036():
#     """Test error: No entry point (missing main)"""
#     source = """
#     void foo() {}
#     """
#     expected = "NoEntryPoint()"
#     assert Checker(source).check_from_source() == expected

# def test_037():
#     """Test error: Main with parameters"""
#     source = """
#     void main(int argc) {}
#     """
#     expected = "NoEntryPoint()"
#     assert Checker(source).check_from_source() == expected

def test_038():
    """Test error: Undeclared struct in variable declaration"""
    source = """
    void main() {
        Point p;
    }
    """
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected

def test_039():
    """Test error: Undeclared struct in function parameter"""
    source = """
    void move(Point p) {}
    void main() {}
    """
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected

def test_040():
    """Test error: Undeclared struct in struct member"""
    source = """
    struct Line {
        Point start;
    };
    void main() {}
    """
    expected = "UndeclaredStruct(Point)"
    assert Checker(source).check_from_source() == expected


def test_041():
    """Test error: Member access on non-struct type"""
    source = """
    void main() {
        int a = 5;
        a.x = 10;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(a).x))"
    assert Checker(source).check_from_source() == expected

def test_042():
    """Test error: Member access of non-existent field"""
    source = """
    struct A { int x; };
    void main() {
        A a;
        a.y = 10;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(a).y))"
    assert Checker(source).check_from_source() == expected

def test_043():
    """Test error: Struct literal wrong number of values"""
    source = """
    struct A { int x; int y; };
    void main() {
        A a = {1};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(1)}))"
    assert Checker(source).check_from_source() == expected

def test_044():
    """Test error: Struct literal type mismatch"""
    source = """
    struct A { int x; };
    void main() {
        A a = {3.14};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({FloatLiteral(3.14)}))"
    assert Checker(source).check_from_source() == expected

def test_045():
    """Test error: Struct literal initialization with undeclared struct"""
    source = """
    void main() {
        A a = {1};
    }
    """
    expected = "UndeclaredStruct(A)"
    assert Checker(source).check_from_source() == expected


def test_046():
    """Test error: Return float in int function"""
    source = """
    int foo() { return 3.14; }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_047():
    """Test error: Return int in void function"""
    source = """
    void foo() { return 1; }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_048():
    """Test error: Return string in auto function conflicting with int"""
    source = """
    auto foo() {
        if (1) return 1;
        return "str";
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected


def test_049():
    """Test error: Modulo with float"""
    source = """
    void main() {
        int a = 1 % 2.0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), %, FloatLiteral(2.0)))"
    assert Checker(source).check_from_source() == expected

def test_050():
    """Test error: Logical AND with float"""
    source = """
    void main() {
        int a = 1 && 2.0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), &&, FloatLiteral(2.0)))"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Test error: Logical OR with float"""
    source = """
    void main() {
        int a = 1.0 || 0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(FloatLiteral(1.0), ||, IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test_052():
    """Test error: Unary NOT on float"""
    source = """
    void main() {
        int a = !3.14;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(!FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_053():
    """Test error: Binary + on string"""
    source = """
    void main() {
        int a = 1 + "str";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), +, StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Test error: Relational < on string"""
    source = """
    void main() {
        int a = 1 < "str";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), <, StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Test error: Assign float to int"""
    source = """
    void main() {
        int a;
        a = 1.0;
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(a) = FloatLiteral(1.0)))"
    assert Checker(source).check_from_source() == expected

def test_056():
    """Test error: Function call too few arguments"""
    source = """
    void f(int a) {}
    void main() { f(); }
    """
    expected = "TypeMismatchInExpression(FuncCall(f, []))"
    assert Checker(source).check_from_source() == expected

def test_057():
    """Test error: Function call too many arguments"""
    source = """
    void f(int a) {}
    void main() { f(1, 2); }
    """
    expected = "TypeMismatchInExpression(FuncCall(f, [IntLiteral(1), IntLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_058():
    """Test error: Function call argument type mismatch"""
    source = """
    void f(int a) {}
    void main() { f(3.14); }
    """
    expected = "TypeMismatchInExpression(FuncCall(f, [FloatLiteral(3.14)]))"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Test error: Call undefined function"""
    source = """
    void main() {
        undefined_func();
    }
    """
    expected = "UndeclaredFunction(undefined_func)"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Test error: Array access unsupported"""
    source = """
    void main() {
        int a;
        int b = a[1];
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(a), [], IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected


def test_061():
    """Test error: Break outside loop or switch"""
    source = """
    void main() {
        if (1) { break; }
    }
    """
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Test error: Continue outside loop"""
    source = """
    void main() {
        if (1) { continue; }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Test error: Continue inside switch but outside loop"""
    source = """
    void main() {
        switch(1) {
            case 1: continue;
        }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Test error: Shadowing parameter inside nested block"""
    source = """
    void foo(int a) {
        if (1) {
            int a = 5;
        }
    }
    void main() {}
    """
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Test valid: Shadowing in local scopes"""
    source = """
    void main() {
        int x = 1;
        {
            float x = 3.14;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_066():
    """Test error: Assign to literal"""
    source = """
    void main() {
        1 = 2;
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(IntLiteral(1) = IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Test error: Prefix operation on literal value (L-value constraint)"""
    source = """
    void main() {
        ++5;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(++IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_068():
    """Test error: Postfix decrement on literal"""
    source = """
    void main() {
        1--;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(IntLiteral(1)--))"
    assert Checker(source).check_from_source() == expected

def test_069():
    """Test error: Unresolved auto in binary operation"""
    source = """
    void main() {
        auto a;
        auto b;
        int c = a * b;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(a), *, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Test error: Unresolved auto in return"""
    source = """
    auto foo() {
        auto x;
        return x;
    }
    void main() {}
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Test error: Unresolved auto in if condition"""
    source = """
    void main() {
        auto x;
        if (x) {}
    }
    """
    expected = "TypeCannotBeInferred(IfStmt(if Identifier(x) then BlockStmt([])))"
    assert Checker(source).check_from_source() == expected

def test_072():
    """Test valid: Auto type inferred across assignments"""
    source = """
    void main() {
        auto a;
        auto b;
        b = 10;
        a = b;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_073():
    """Test error: Void function used in expression"""
    source = """
    void foo() {}
    void main() {
        int a = foo() + 1;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(FuncCall(foo, []), +, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_074():
    """Test valid: Function return type inferred from another function"""
    source = """
    int foo() { return 10; }
    auto bar() { return foo(); }
    void main() {
        int x = bar();
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_075():
    """Test valid: Multi-level break and continue in loops"""
    source = """
    void main() {
        while(1) {
            for(int i=0; i<10; ++i) {
                switch(i) {
                    case 5: break;
                    default: continue;
                }
            }
            break;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_076():
    """Test valid: Auto inference resolved via function parameter context"""
    source = """
    void foo(int a) {}
    void main() { 
        auto x; 
        foo(x); 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_077():
    """Test valid: Valid empty return in void function"""
    source = """
    void main() { 
        return; 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_078():
    """Test error: Return a value inside a void function"""
    source = """
    void main() { 
        return 1; 
    }
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected


def test_079():
    """Test error: Empty return inside a typed function"""
    source = """
    int foo() { 
        return; 
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return))"
    assert Checker(source).check_from_source() == expected


def test_080():
    """Test error: Return float inside int function"""
    source = """
    int foo() { 
        return 3.14; 
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected



def test_081():
    """Test valid: Nested struct initialization"""
    source = """
    struct Engine { int hp; }; 
    struct Car { Engine eng; }; 
    void main() { 
        Car myCar = {{500}}; 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_082():
    """Test valid: Chained assignment with auto resolution"""
    source = """
    void main() {
        auto a; auto b; int c = 5;
        a = b = c;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_083():
    """Test valid: Struct member as function argument"""
    source = """
    struct S { int x; }; 
    void f(int val) {} 
    void main() { 
        S s; 
        f(s.x); 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_084():
    """Test error: Assigning struct to incompatible struct type"""
    source = """
    struct S1 { int x; }; 
    struct S2 { int x; }; 
    void main() { 
        S1 a; S2 b; 
        a = b; 
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(a) = Identifier(b)))"
    assert Checker(source).check_from_source() == expected


def test_085():
    """Test valid: Function returning a struct"""
    source = """
    struct Point { int x; }; 
    Point getPoint() { 
        Point p; 
        return p; 
    } 
    void main() { 
        Point a = getPoint(); 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_086():
    """Test valid: Auto variable inferred as struct via function return"""
    source = """
    struct Point { int x; }; 
    Point getPoint() { 
        Point p; return p; 
    } 
    void main() { 
        auto a = getPoint(); 
        a.x = 10;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_087():
    """Test valid: Struct member access directly on function call"""
    source = """
    struct Point { int x; }; 
    Point getPoint() { 
        Point p; return p; 
    } 
    void main() { 
        int val = getPoint().x; 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_088():
    """Test valid: For loop with minimal valid components"""
    source = """
    void main() {
        for(int i = 0;;) { break; }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_089():
    """Test error: Self-initialization evaluates RHS before declaration"""
    source = """
    void main() { 
        int x = x; 
    }
    """
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected


def test_090():
    """Test valid: Parameter shadowing across separate scopes"""
    source = """
    void f(int g) { g = 5; }
    void main() {
        int g = 10;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_091():
    """Test error: Strict TyC Rule - Local variable shadowing parameter in nested block"""
    source = """
    void foo(int a) { 
        { 
            int a = 5; 
        } 
    } 
    void main() {}
    """
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected


def test_092():
    """Test valid: Switch statement without default case"""
    source = """
    void main() { 
        switch(1) { 
            case 1: break; 
        } 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_093():
    """Test error: Float type in switch case condition"""
    source = """
    void main() {
        switch(1) {
            case 1.0: break;
        }
    }
    """
    expected = "TypeMismatchInStatement(CaseStmt(case FloatLiteral(1.0): [BreakStmt()]))"
    assert Checker(source).check_from_source() == expected


def test_094():
    """Test error: Modulo operator on float type"""
    source = """
    void main() { 
        int a = 5 % 2.0; 
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(5), %, FloatLiteral(2.0)))"
    assert Checker(source).check_from_source() == expected



def test_095():
    """Test error: Logical AND on float type"""
    source = """
    void main() { 
        int a = 1 && 2.0; 
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), &&, FloatLiteral(2.0)))"
    assert Checker(source).check_from_source() == expected


def test_096():
    """Test error: Prefix operation on literal value"""
    source = """
    void main() {
        ++5;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(++IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_097():
    """Test error: Postfix operation on binary expression"""
    source = """
    void main() {
        (1 + 2)++;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(BinaryOp(IntLiteral(1), +, IntLiteral(2))++))"
    assert Checker(source).check_from_source() == expected

def test_098():
    """Test error: Assignment to binary expression (L-value constraint)"""
    source = """
    void main() { 
        1 + 2 = 5; 
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(BinaryOp(IntLiteral(1), +, IntLiteral(2)) = IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected


def test_099():
    """Test error: Unresolved auto used in function call arguments"""
    source = """
    void f(int a) {} 
    void main() { 
        auto x; auto y; 
        f(x + y); 
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))"
    assert Checker(source).check_from_source() == expected


def test_100():
    """Test valid: Local variable initialization"""
    source = """
    void main() {
        int a = 10;
        int b = a;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_101():
    """Test error: Function overloading is strictly prohibited"""
    source = """
    void compute() {} 
    void compute(int x) {} 
    void main() {}
    """
    expected = "Redeclared(Function, compute)"
    assert Checker(source).check_from_source() == expected


def test_102():
    """Test valid: Struct and Function sharing the same name (Independent Namespaces)"""
    source = """
    struct Manager { int x; }; 
    void Manager() {} 
    void main() { 
        Manager m; 
        m.x = 1; 
        Manager(); 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_103():
    """Test valid: Inline struct literal as function argument"""
    source = """
    struct Point { int x; int y; }; 
    void draw(Point p) {} 
    void main() { 
        draw({10, 20}); 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_104():
    """Test valid: Multiple variable declaration in one line"""
    source = """
    void main() { 
        int a = 1, b = 2; 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_105():
    """Test error: Multiple variable declaration with one type mismatch"""
    source = """
    void main() { 
        int a = 1, b = 3.14; 
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), b = FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_106():
    """Test valid: Deeply nested struct member access and initialization"""
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() {
        B b = {{10}};
        int y = b.a.x + 5;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_107():
    """Test error: String literal in for loop condition"""
    source = """
    void main() {
        for (int i = 0; "hello"; ++i) {}
    }
    """
    expected = "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); StringLiteral('hello'); PrefixOp(++Identifier(i)) do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected


def test_108():
    """Test error: Array access is not supported in TyC"""
    source = """
    void main() {
        int x = 5;
        int y = x[0];
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), [], IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected


def test_109():
    """Test error: Unary minus on string literal"""
    source = """
    void main() {
        string s = -"hello";
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(-StringLiteral('hello')))"
    assert Checker(source).check_from_source() == expected


def test_110():
    """Test error: Assigning void function call to typed variable"""
    source = """
    void foo() {}
    void main() {
        int x = foo();
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = FuncCall(foo, [])))"
    assert Checker(source).check_from_source() == expected


# def test_111():
#     """Test error: Redeclared parameter in deeply nested block (Strict rule)"""
#     source = """
#     void test(int p) {
#         for(;;) {
#             if (1) {
#                 int p = 5;
#             }
#         }
#     }
#     void main() {}
#     """
#     expected = "Redeclared(Variable, p)"
#     assert Checker(source).check_from_source() == expected


def test_112():
    """Test valid: auto tie-break resolution with integer literal (Rule 2.2.1)"""
    source = """
    void main() {
        auto x;
        auto y = x + 5; 
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_113():
    """Test error: auto tie-break does NOT apply for float literals (Rule 2.2.1 applies to int only)"""
    source = """
    void main() {
        auto x;
        auto y = x + 5.0;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, FloatLiteral(5.0)))"
    assert Checker(source).check_from_source() == expected


def test_114():
    """Test error: Modulo with un-inferred auto operands"""
    source = """
    void main() {
        auto x; auto y;
        int z = x % y;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), %, Identifier(y)))"
    assert Checker(source).check_from_source() == expected


def test_115():
    """Test valid: Continue inside switch that is nested in a while loop"""
    source = """
    void main() {
        while(1) {
            switch(1) {
                case 1: continue;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected