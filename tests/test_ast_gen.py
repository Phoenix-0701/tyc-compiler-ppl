"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator


import pytest
from tests.utils import ASTGenerator

def test_ast_arithmetic_chain():
    source = "void main() { x = a + b + c + d; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), +, Identifier(c)), +, Identifier(d))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_array_assign_func_call():
    source = "void main() { arr[f()] = g(); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(BinaryOp(Identifier(arr), [], FuncCall(f, [])) = FuncCall(g, [])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_prefix_member_access():
    source = "void main() { ++p.x; --p.y; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(PrefixOp(++MemberAccess(Identifier(p).x))), ExprStmt(PrefixOp(--MemberAccess(Identifier(p).y)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_float_var_decl_arithmetic():
    source = "void main() { float x = 1.0 + 2.5 * 3.0; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(FloatType(), x = BinaryOp(FloatLiteral(1.0), +, BinaryOp(FloatLiteral(2.5), *, FloatLiteral(3.0))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_auto_struct_literal_nested():
    source = "void main() { auto s = { {1}, {2, 3} }; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, s = StructLiteral({StructLiteral({IntLiteral(1)}), StructLiteral({IntLiteral(2), IntLiteral(3)})}))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_nested_else():
    source = "void main() { if (a) if (b) c = 1; else c = 2; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then IfStmt(if Identifier(b) then ExprStmt(AssignExpr(Identifier(c) = IntLiteral(1))), else ExprStmt(AssignExpr(Identifier(c) = IntLiteral(2)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_break_nested():
    source = "void main() { while (i < 10) { i++; if (i == 5) break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while BinaryOp(Identifier(i), <, IntLiteral(10)) do BlockStmt([ExprStmt(PostfixOp(Identifier(i)++)), IfStmt(if BinaryOp(Identifier(i), ==, IntLiteral(5)) then BreakStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_auto_init():
    source = "void main() { for (auto i = 0; i < 5; ++i) print(i); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(5)); PrefixOp(++Identifier(i)) do ExprStmt(FuncCall(print, [Identifier(i)])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_decl_empty():
    source = "struct Empty {};"
    expected = "Program([StructDecl(Empty, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_nested_block_return():
    source = "int f() { { return 1; } }"
    expected = "Program([FuncDecl(IntType(), f, [], BlockStmt([BlockStmt([ReturnStmt(return IntLiteral(1))])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_div_mod_chain():
    source = "void main() { x = a / b % c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), /, Identifier(b)), %, Identifier(c))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_not_and():
    source = "void main() { b = !flag1 && !flag2; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(b) = BinaryOp(PrefixOp(!Identifier(flag1)), &&, PrefixOp(!Identifier(flag2)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_paren_expression_mul():
    source = "void main() { res = (a + b) * (c + d); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(res) = BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), +, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_case_block():
    source = "void main() { switch(v) { case 1: { x=1; break; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(v) cases [CaseStmt(case IntLiteral(1): [BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1))), BreakStmt()])])])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_multi_assignment():
    source = "void main() { a = b = c = d = 0; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = AssignExpr(Identifier(c) = AssignExpr(Identifier(d) = IntLiteral(0))))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_nested_no_else():
    source = "void main() { if (1) { if (2) { return; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([IfStmt(if IntLiteral(2) then BlockStmt([ReturnStmt(return)]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_no_update():
    source = "void main() { for (i=0; i<10; ) { i++; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(10)); None do BlockStmt([ExprStmt(PostfixOp(Identifier(i)++))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_decl_multi_fields():
    source = "struct S { int x; float y; string z; };"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x), MemberDecl(FloatType(), y), MemberDecl(StringType(), z)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_multiple_void_funcs():
    source = "void f() {} void g() {}"
    expected = "Program([FuncDecl(VoidType(), f, [], BlockStmt([])), FuncDecl(VoidType(), g, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_complex_unary_chain():
    source = "void main() { x = - + ! ! y; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PrefixOp(-PrefixOp(+PrefixOp(!PrefixOp(!Identifier(y)))))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_member_access_chain():
    source = "void main() { a.b.c.d = 10; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(MemberAccess(MemberAccess(Identifier(a).b).c).d) = IntLiteral(10)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_member_assign():
    source = "void main() { func(1, 2, 3).member = 0; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(FuncCall(func, [IntLiteral(1), IntLiteral(2), IntLiteral(3)]).member) = IntLiteral(0)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_array_access_nested():
    source = "void main() { data[i][j] = val; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(BinaryOp(BinaryOp(Identifier(data), [], Identifier(i)), [], Identifier(j)) = Identifier(val)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_default_break():
    source = "void main() { switch(status) { case 0: return; default: break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(status) cases [CaseStmt(case IntLiteral(0): [ReturnStmt(return)])], default DefaultStmt(default: [BreakStmt()]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_return():
    source = "void main() { if (a > b) return a; else return b; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if BinaryOp(Identifier(a), >, Identifier(b)) then ReturnStmt(return Identifier(a)), else ReturnStmt(return Identifier(b)))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_ast_struct_recursive_member():
    source = "struct Node { int val; struct Node next; };"
    expected = "Program([StructDecl(Node, [MemberDecl(IntType(), val), MemberDecl(StructType(Node), next)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_auto_var_member_array():
    source = "void main() { auto x = func().member[0]; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(MemberAccess(FuncCall(func, []).member), [], IntLiteral(0)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_math_precedence_mix():
    source = "void main() { x = (1 + 2) * (3 - 4) / 5; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, BinaryOp(IntLiteral(3), -, IntLiteral(4))), /, IntLiteral(5))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_continue_nested():
    source = "void main() { while (flag) { do_a(); if (cond) continue; do_b(); } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(flag) do BlockStmt([ExprStmt(FuncCall(do_a, [])), IfStmt(if Identifier(cond) then ContinueStmt()), ExprStmt(FuncCall(do_b, []))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_relational_equality_mix():
    source = "void main() { x = a < b == c > d; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), <, Identifier(b)), ==, BinaryOp(Identifier(c), >, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_not_or_and():
    source = "void main() { x = !a || b && c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(PrefixOp(!Identifier(a)), ||, BinaryOp(Identifier(b), &&, Identifier(c)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_mixed_unary_binary():
    source = "void main() { x = ++a + b--; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(PrefixOp(++Identifier(a)), +, PostfixOp(Identifier(b)--))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_method_chain_assign():
    source = "void main() { obj.method(1).field = 2; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(FuncCall(MemberAccess(Identifier(obj).method), [IntLiteral(1)]).field) = IntLiteral(2)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_multi_var_decl_assign():
    source = "void main() { int x, y, z; x = y = z = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(IntType(), x), VarDecl(IntType(), y), VarDecl(IntType(), z), ExprStmt(AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = AssignExpr(Identifier(z) = IntLiteral(1)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_case_fallthrough_logic():
    source = "void main() { switch(x) { case 1: case 2: return 0; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): []), CaseStmt(case IntLiteral(2): [ReturnStmt(return IntLiteral(0))])])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_blocks():
    source = "void main() { if (a) { return; } else { x=1; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then BlockStmt([ReturnStmt(return)]), else BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_ast_struct_nesting():
    source = "struct A { int x; }; struct B { struct A a; };"
    expected = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(StructType(A), a)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_paren_assign_binop():
    source = "void main() { x = a + (b = c + d); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(a), +, AssignExpr(Identifier(b) = BinaryOp(Identifier(c), +, Identifier(d))))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_member_access_multi_assign():
    source = "void main() { p.x = q.y = r.z; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(MemberAccess(Identifier(p).x) = AssignExpr(MemberAccess(Identifier(q).y) = MemberAccess(Identifier(r).z))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_nested_args():
    source = "void main() { x = f(g(h())); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(f, [FuncCall(g, [FuncCall(h, [])])])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_array_assign_struct_literal():
    source = "void main() { arr[0] = {1, 2, 3}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(BinaryOp(Identifier(arr), [], IntLiteral(0)) = StructLiteral({IntLiteral(1), IntLiteral(2), IntLiteral(3)})))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_while_break():
    source = "void main() { if (x) { while(y) break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(x) then BlockStmt([WhileStmt(while Identifier(y) do BreakStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_only_default():
    source = "void main() { switch(x) { default: { return; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [], default DefaultStmt(default: [BlockStmt([ReturnStmt(return)])]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_nested_for():
    source = "void main() { for(int i=0; i<10; i++) { for(int j=0; j<10; j++) {} } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([ForStmt(for VarDecl(IntType(), j = IntLiteral(0)); BinaryOp(Identifier(j), <, IntLiteral(10)); PostfixOp(Identifier(j)++) do BlockStmt([]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_decl_with_var_init():
    source = "struct S { int x; }; void main() { struct S s = {1}; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1)}))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_relational_logical_and():
    source = "void main() { x = (a == b) && (c != d); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), ==, Identifier(b)), &&, BinaryOp(Identifier(c), !=, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_complex_math_ops():
    source = "void main() { x = a * b + c / d - e % f; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), *, Identifier(b)), +, BinaryOp(Identifier(c), /, Identifier(d))), -, BinaryOp(Identifier(e), %, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_mixed_unary_ops_assign():
    source = "void main() { x = -a + +b - !c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(PrefixOp(-Identifier(a)), +, PrefixOp(+Identifier(b))), -, PrefixOp(!Identifier(c)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_member_access_array_nested():
    source = "void main() { p.x.y[0] = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(BinaryOp(MemberAccess(MemberAccess(Identifier(p).x).y), [], IntLiteral(0)) = IntLiteral(1)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_auto_string_indexing():
    source = "void main() { auto x = \"str\"[1]; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(auto, x = BinaryOp(StringLiteral('str'), [], IntLiteral(1)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_mixed_literals():
    source = "void main() { x = f(1, {2, 3}, 4); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(f, [IntLiteral(1), StructLiteral({IntLiteral(2), IntLiteral(3)}), IntLiteral(4)])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_with_while_continue():
    source = "void main() { if (a) { if (b) break; } else { while(c) continue; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then BlockStmt([IfStmt(if Identifier(b) then BreakStmt())]), else BlockStmt([WhileStmt(while Identifier(c) do ContinueStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_multi_case_stmts():
    source = "void main() { switch(x) { case 1: x++; case 2: x--; default: x=0; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(PostfixOp(Identifier(x)++))]), CaseStmt(case IntLiteral(2): [ExprStmt(PostfixOp(Identifier(x)--))])], default DefaultStmt(default: [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(0)))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_no_update_assign_body():
    source = "void main() { for(int i=0; i<5; ) { i = i + 1; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(5)); None do BlockStmt([ExprStmt(AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1))))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_decl_param_struct():
    source = "struct S { int a; }; void f(struct S s) { return s.a; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), a)]), FuncDecl(VoidType(), f, [Param(StructType(S), s)], BlockStmt([ReturnStmt(return MemberAccess(Identifier(s).a))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_complex_logical_relational():
    source = "void main() { x = a > b || c <= d && e != f; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), >, Identifier(b)), ||, BinaryOp(BinaryOp(Identifier(c), <=, Identifier(d)), &&, BinaryOp(Identifier(e), !=, Identifier(f))))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_nested_parentheses():
    source = "void main() { x = ( ( (a) ) ); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = Identifier(a)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_assign_args():
    source = "void main() { x = func(a=1, b=2); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(func, [AssignExpr(Identifier(a) = IntLiteral(1)), AssignExpr(Identifier(b) = IntLiteral(2))])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_array_member_array_assign():
    source = "void main() { a[i+1] = b.c[j*2]; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(BinaryOp(Identifier(a), [], BinaryOp(Identifier(i), +, IntLiteral(1))) = BinaryOp(MemberAccess(Identifier(b).c), [], BinaryOp(Identifier(j), *, IntLiteral(2)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_empty_blocks():
    source = "void main() { if (flag) { } else { } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(flag) then BlockStmt([]), else BlockStmt([]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_if_break():
    source = "void main() { while(1) { if(a) { break; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([IfStmt(if Identifier(a) then BlockStmt([BreakStmt()]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_auto_no_cond():
    source = "void main() { for(auto i=0; ; ) { break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(auto, i = IntLiteral(0)); None; None do BlockStmt([BreakStmt()]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_deep_struct_member_assign():
    source = "struct A { int x; }; struct B { struct A a; }; void main() { struct B b; b.a.x = 1; }"
    expected = "Program([StructDecl(A, [MemberDecl(IntType(), x)]), StructDecl(B, [MemberDecl(StructType(A), a)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(B), b), ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier(b).a).x) = IntLiteral(1)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_math_precedence_complex():
    source = "void main() { x = (a+b)*(c-d)/(e+f); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), -, Identifier(d))), /, BinaryOp(Identifier(e), +, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_case_if_break():
    source = "void main() { switch(x) { case 1: { if(y) break; } default: return; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BlockStmt([IfStmt(if Identifier(y) then BreakStmt())])])], default DefaultStmt(default: [ReturnStmt(return)]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_and_or_precedence():
    source = "void main() { x = a && b || c && d; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, BinaryOp(Identifier(c), &&, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_double_unary_ops():
    source = "void main() { x = !!y; z = --++i; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = PrefixOp(!PrefixOp(!Identifier(y))))), ExprStmt(AssignExpr(Identifier(z) = PrefixOp(--PrefixOp(++Identifier(i)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_with_continue_print():
    source = "void main() { for(int i=0; i<10; i++) { if(i%2==0) continue; print(i); } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([IfStmt(if BinaryOp(BinaryOp(Identifier(i), %, IntLiteral(2)), ==, IntLiteral(0)) then ContinueStmt()), ExprStmt(FuncCall(print, [Identifier(i)]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_init_member_access():
    source = "struct S { int x; }; void main() { struct S s = {10}; print(s.x); }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(10)})), ExprStmt(FuncCall(print, [MemberAccess(Identifier(s).x)]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_multi_level_array_member():
    source = "void main() { x = a[i].b[j].c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = MemberAccess(BinaryOp(MemberAccess(BinaryOp(Identifier(a), [], Identifier(i)).b), [], Identifier(j)).c)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_loop_return():
    source = "void main() { while(a < b) { a = a + 1; if(a == 5) return; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while BinaryOp(Identifier(a), <, Identifier(b)) do BlockStmt([ExprStmt(AssignExpr(Identifier(a) = BinaryOp(Identifier(a), +, IntLiteral(1)))), IfStmt(if BinaryOp(Identifier(a), ==, IntLiteral(5)) then ReturnStmt(return))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_comparison_chain():
    source = "void main() { x = a >= b && c <= d || e == f; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), >=, Identifier(b)), &&, BinaryOp(Identifier(c), <=, Identifier(d))), ||, BinaryOp(Identifier(e), ==, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_nested_func_calls():
    source = "void main() { x = f(1, g(2, h(3))); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(f, [IntLiteral(1), FuncCall(g, [IntLiteral(2), FuncCall(h, [IntLiteral(3)])])])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_deeply_nested_if():
    source = "void main() { if (1) { if (0) { } else { return; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([IfStmt(if IntLiteral(0) then BlockStmt([]), else BlockStmt([ReturnStmt(return)]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_no_cond_break():
    source = "void main() { for(int i=0; ; ) { i++; if(i>10) break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); None; None do BlockStmt([ExprStmt(PostfixOp(Identifier(i)++)), IfStmt(if BinaryOp(Identifier(i), >, IntLiteral(10)) then BreakStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_var_scoped_assign():
    source = "struct S { int x; }; void main() { struct S s; s.x = 1; { s.x = 2; } }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s), ExprStmt(AssignExpr(MemberAccess(Identifier(s).x) = IntLiteral(1))), BlockStmt([ExprStmt(AssignExpr(MemberAccess(Identifier(s).x) = IntLiteral(2)))])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_arithmetic_func_array_mix():
    source = "void main() { x = a[0] + b.c - f(d); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), [], IntLiteral(0)), +, MemberAccess(Identifier(b).c)), -, FuncCall(f, [Identifier(d)]))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_case_while_break():
    source = "void main() { switch(x) { case 1: { while(1) break; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BlockStmt([WhileStmt(while IntLiteral(1) do BreakStmt())])])])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_math_paren_precedence():
    source = "void main() { x = a * (b + c) / (d - e); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), *, BinaryOp(Identifier(b), +, Identifier(c))), /, BinaryOp(Identifier(d), -, Identifier(e)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_not_binop():
    source = "void main() { x = ! (a == b) || c != d; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(PrefixOp(!BinaryOp(Identifier(a), ==, Identifier(b))), ||, BinaryOp(Identifier(c), !=, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_switch_break():
    source = "void main() { for(int i=0; i<10; i++) { switch(i) { case 0: break; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([SwitchStmt(switch Identifier(i) cases [CaseStmt(case IntLiteral(0): [BreakStmt()])])]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_method_call_member_array():
    source = "void main() { x = a.b(1).c[0]; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(MemberAccess(FuncCall(MemberAccess(Identifier(a).b), [IntLiteral(1)]).c), [], IntLiteral(0))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_return_struct_literal():
    source = "void main() { if (a) { return {1, 2}; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then BlockStmt([ReturnStmt(return StructLiteral({IntLiteral(1), IntLiteral(2)}))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_full_arithmetic_precedence():
    source = "void main() { x = a + b - c * d / e % f; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), -, BinaryOp(BinaryOp(BinaryOp(Identifier(c), *, Identifier(d)), /, Identifier(e)), %, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_if_else_control():
    source = "void main() { while(1) { if(a) break; else continue; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while IntLiteral(1) do BlockStmt([IfStmt(if Identifier(a) then BreakStmt(), else ContinueStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_nested_for_loops_break():
    source = "void main() { for(int i=0; ; ) { for(int j=0; ; ) { break; } break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); None; None do BlockStmt([ForStmt(for VarDecl(IntType(), j = IntLiteral(0)); None; None do BlockStmt([BreakStmt()])), BreakStmt()]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_member_func_call_assign():
    source = "struct S { int x; }; void main() { struct S s; s.x = func(1, 2); }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s), ExprStmt(AssignExpr(MemberAccess(Identifier(s).x) = FuncCall(func, [IntLiteral(1), IntLiteral(2)])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_complex_array_member_access():
    source = "void main() { x = a[i+j].b.c[k*2]; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(MemberAccess(MemberAccess(BinaryOp(Identifier(a), [], BinaryOp(Identifier(i), +, Identifier(j))).b).c), [], BinaryOp(Identifier(k), *, IntLiteral(2)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_switch_case_nested_if_return():
    source = "void main() { switch(x) { case 1: { if(a) { return; } } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [BlockStmt([IfStmt(if Identifier(a) then BlockStmt([ReturnStmt(return)]))])])])]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_logical_and_or_chain():
    source = "void main() { x = (a && b) || (c && d) || (e && f); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, BinaryOp(Identifier(c), &&, Identifier(d))), ||, BinaryOp(Identifier(e), &&, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_mixed_prefix_postfix_arithmetic():
    source = "void main() { x = ++a + b-- * c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(PrefixOp(++Identifier(a)), +, BinaryOp(PostfixOp(Identifier(b)--), *, Identifier(c)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_loop_with_assignment_and_return():
    source = "void main() { for(int i=0; i<10; i++) { x = x + i; if(x > 100) return; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(Identifier(x), +, Identifier(i)))), IfStmt(if BinaryOp(Identifier(x), >, IntLiteral(100)) then ReturnStmt(return))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_multiple_var_decl_chained_assign():
    source = "struct S { int x; }; void main() { struct S s1, s2; s1.x = s2.x = 0; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s1), VarDecl(StructType(S), s2), ExprStmt(AssignExpr(MemberAccess(Identifier(s1).x) = AssignExpr(MemberAccess(Identifier(s2).x) = IntLiteral(0))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_deep_member_access_array_func_call():
    source = "void main() { x = a.b.c[i+1].d(1); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(MemberAccess(BinaryOp(MemberAccess(MemberAccess(Identifier(a).b).c), [], BinaryOp(Identifier(i), +, IntLiteral(1))).d), [IntLiteral(1)])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_nested_while_with_breaks():
    source = "void main() { while(a) { while(b) { if(c) break; } if(d) break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(a) do BlockStmt([WhileStmt(while Identifier(b) do BlockStmt([IfStmt(if Identifier(c) then BreakStmt())])), IfStmt(if Identifier(d) then BreakStmt())]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_relational_equality_complex_chain():
    source = "void main() { x = a >= b == c <= d; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(Identifier(a), >=, Identifier(b)), ==, BinaryOp(Identifier(c), <=, Identifier(d)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_multiple_nested_args():
    source = "void main() { x = f(g(1), h(2), k(3)); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(f, [FuncCall(g, [IntLiteral(1)]), FuncCall(h, [IntLiteral(2)]), FuncCall(k, [IntLiteral(3)])])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_if_else_structure():
    source = "void main() { if (1) { x=1; } else if (0) { x=2; } else { x=3; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))]), else IfStmt(if IntLiteral(0) then BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))]), else BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(3)))])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_multi_parentheses_arithmetic_mul():
    source = "void main() { x = (a+b)*(c+d)*(e+f); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), +, Identifier(d))), *, BinaryOp(Identifier(e), +, Identifier(f)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_loop_switch_default_print():
    source = "void main() { for(int i=0; i<10; i++) { switch(i%2) { case 0: print(0); break; default: print(1); } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([SwitchStmt(switch BinaryOp(Identifier(i), %, IntLiteral(2)) cases [CaseStmt(case IntLiteral(0): [ExprStmt(FuncCall(print, [IntLiteral(0)])), BreakStmt()])], default DefaultStmt(default: [ExprStmt(FuncCall(print, [IntLiteral(1)]))]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_init_with_func_call():
    source = "struct S { int x; }; void main() { struct S s = {f(1)}; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({FuncCall(f, [IntLiteral(1)])}))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_long_member_access_chain():
    source = "void main() { x = a.b.c.d.e; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = MemberAccess(MemberAccess(MemberAccess(MemberAccess(Identifier(a).b).c).d).e)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_return_nested_func_calls():
    source = "void main() { if (a) { return f(g(h())); } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if Identifier(a) then BlockStmt([ReturnStmt(return FuncCall(f, [FuncCall(g, [FuncCall(h, [])])]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_deeply_nested_if_break():
    source = "void main() { while(a) { if(b) { if(c) { break; } } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(a) do BlockStmt([IfStmt(if Identifier(b) then BlockStmt([IfStmt(if Identifier(c) then BlockStmt([BreakStmt()]))]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_mixed_prefix_unary_ops():
    source = "void main() { x = --a + ++b - !c; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(PrefixOp(--Identifier(a)), +, PrefixOp(++Identifier(b))), -, PrefixOp(!Identifier(c)))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_if_switch_nested_control():
    source = "void main() { for(int i=0; i<10; i++) { if(i==5) { switch(i) { case 5: break; } } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([IfStmt(if BinaryOp(Identifier(i), ==, IntLiteral(5)) then BlockStmt([SwitchStmt(switch Identifier(i) cases [CaseStmt(case IntLiteral(5): [BreakStmt()])])]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_member_assign_mixed_ops():
    source = "struct S { int x; }; void main() { struct S s; s.x = a[i] + b.c; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s), ExprStmt(AssignExpr(MemberAccess(Identifier(s).x) = BinaryOp(BinaryOp(Identifier(a), [], Identifier(i)), +, MemberAccess(Identifier(b).c))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_chained_func_calls_member_access():
    source = "void main() { x = f(1).g(2).h(3); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(MemberAccess(FuncCall(MemberAccess(FuncCall(f, [IntLiteral(1)]).g), [IntLiteral(2)]).h), [IntLiteral(3)])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_while_complex_if_else_control():
    source = "void main() { while(a) { if(b) break; else if(c) continue; else return; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([WhileStmt(while Identifier(a) do BlockStmt([IfStmt(if Identifier(b) then BreakStmt(), else IfStmt(if Identifier(c) then ContinueStmt(), else ReturnStmt(return)))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected


def test_ast_deeply_nested_func_calls():
    source = "void main() { x = f(g(h(k(1)))); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(f, [FuncCall(g, [FuncCall(h, [FuncCall(k, [IntLiteral(1)])])])])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_if_else_explicit_blocks():
    source = "void main() { if (1) { x=1; } else { if (0) { x=2; } else { x=3; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([IfStmt(if IntLiteral(1) then BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))]), else BlockStmt([IfStmt(if IntLiteral(0) then BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(2)))]), else BlockStmt([ExprStmt(AssignExpr(Identifier(x) = IntLiteral(3)))]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_complex_arithmetic_precedence_mix():
    source = "void main() { x = (a+b)*(c+d)/(e+f)*g; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, BinaryOp(Identifier(c), +, Identifier(d))), /, BinaryOp(Identifier(e), +, Identifier(f))), *, Identifier(g))))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_for_loop_if_else_continue():
    source = "void main() { for(int i=0; i<10; i++) { if(i%2==0) { print(i); } else { continue; } } }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([IfStmt(if BinaryOp(BinaryOp(Identifier(i), %, IntLiteral(2)), ==, IntLiteral(0)) then BlockStmt([ExprStmt(FuncCall(print, [Identifier(i)]))]), else BlockStmt([ContinueStmt()]))]))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_struct_init_and_member_access():
    source = "struct S { int x; }; void main() { struct S s = {1}; x = s.x; }"
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), x)]), FuncDecl(VoidType(), main, [], BlockStmt([VarDecl(StructType(S), s = StructLiteral({IntLiteral(1)})), ExprStmt(AssignExpr(Identifier(x) = MemberAccess(Identifier(s).x)))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_member_access_chain_with_func_call():
    source = "void main() { x = a.b.c.d.f(); }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = FuncCall(MemberAccess(MemberAccess(MemberAccess(MemberAccess(Identifier(a).b).c).d).f), [])))]))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_ast_func_call_chain_to_member():
    source = "void main() { x = f(1).g(2).h(3).k; }"
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([ExprStmt(AssignExpr(Identifier(x) = MemberAccess(FuncCall(MemberAccess(FuncCall(MemberAccess(FuncCall(f, [IntLiteral(1)]).g), [IntLiteral(2)]).h), [IntLiteral(3)]).k)))]))])"
    assert str(ASTGenerator(source).generate()) == expected