"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = "void greet() { printString(\"Hello\"); }"
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. While statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. For statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"


def test_block_only():
    """11. Empty block"""
    source = "{}"
    assert Parser(source).parse() != "success"


def test_multiple_functions():
    """12. Multiple function declarations"""
    source = """
        void foo() {}
        void bar() {}
    """
    assert Parser(source).parse() == "success"


def test_nested_blocks():
    """13. Nested blocks"""
    source = "void main() { { int x; } }"
    assert Parser(source).parse() == "success"


def test_var_decl_without_init():
    """14. Variable declaration without initialization"""
    source = "void main() { int x; }"
    assert Parser(source).parse() == "success"


def test_multiple_var_decl():
    """15. Multiple variable declarations"""
    source = "void main() { int x; int y; }"
    assert Parser(source).parse() == "success"


def test_if_else_statement():
    """16. If-else statement"""
    source = "void main() { if (1) x = 1; else x = 2; }"
    assert Parser(source).parse() == "success"


def test_while_with_block():
    """17. While loop with block"""
    source = "void main() { while (1) { printInt(1); } }"
    assert Parser(source).parse() == "success"


def test_for_with_block():
    """18. For loop with block"""
    source = "void main() { for (auto i = 0; i < 5; ++i) { printInt(i); } }"
    assert Parser(source).parse() == "success"


def test_return_no_value():
    """19. Return without value"""
    source = "void main() { return; }"
    assert Parser(source).parse() == "success"


def test_return_with_value():
    """20. Return with value"""
    source = "int foo() { return 1; }"
    assert Parser(source).parse() == "success"


def test_function_with_params():
    """21. Function with parameters"""
    source = "int add(int a, int b) { return a + b; }"
    assert Parser(source).parse() == "success"


def test_call_function_statement():
    """22. Function call as statement"""
    source = "void main() { foo(); }"
    assert Parser(source).parse() == "success"


def test_assignment_expression():
    """23. Assignment with expression"""
    source = "void main() { int x; x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_struct_with_multiple_fields():
    """24. Struct with multiple fields"""
    source = "struct Data { int a; int b; int c; };"
    assert Parser(source).parse() == "success"


def test_switch_multiple_cases():
    """25. Switch with multiple cases"""
    source = """
        void main() {
            switch (x) {
                case 1: x = 1; break;
                case 2: x = 2; break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_switch_with_default():
    """26. Switch with default"""
    source = """
        void main() {
            switch (x) {
                default: x = 0; break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_nested_if():
    """27. Nested if statements"""
    source = "void main() { if (1) if (0) x = 1; }"
    assert Parser(source).parse() == "success"


def test_expression_statement():
    """28. Expression as statement"""
    source = "void main() { 1 + 2; }"
    assert Parser(source).parse() == "success"


def test_empty_statement():
    """29. Empty statement"""
    source = "void main() { ; }"
    assert Parser(source).parse() == "success"


def test_multiple_statements():
    """30. Multiple statements in function"""
    source = "void main() { int x; x = 1; x = x + 1; }"
    assert Parser(source).parse() == "success"


def test_function_with_auto_return():
    """31. Function with auto return type"""
    source = "auto foo() { return 1; }"
    assert Parser(source).parse() == "success"


def test_function_multiple_params():
    """32. Function with multiple parameters"""
    source = "void f(int a, float b, string c) {}"
    assert Parser(source).parse() == "success"


def test_struct_empty():
    """33. Empty struct"""
    source = "struct Empty { };"
    assert Parser(source).parse() == "success"


def test_struct_inside_program():
    """34. Struct and function together"""
    source = """
        struct Point { int x; int y; };
        void main() {}
    """
    assert Parser(source).parse() == "success"


def test_nested_while():
    """35. Nested while loops"""
    source = "void main() { while (1) while (0) x = 1; }"
    assert Parser(source).parse() == "success"


def test_nested_for():
    """36. Nested for loops"""
    source = """
        void main() {
            for (auto i = 0; i < 10; ++i)
                for (auto j = 0; j < 5; ++j)
                    x = i + j;
        }
    """
    assert Parser(source).parse() == "success"


def test_for_without_condition():
    """37. For loop without condition"""
    source = "void main() { for (;;){ break; } }"
    assert Parser(source).parse() == "success"


def test_for_without_init():
    """38. For loop without initialization"""
    source = "void main() { for (; i < 10; ++i) x = i; }"
    assert Parser(source).parse() == "success"


def test_for_without_update():
    """39. For loop without update"""
    source = "void main() { for (i = 0; i < 10;) x = i; }"
    assert Parser(source).parse() == "success"


def test_do_multiple_assignments():
    """40. Multiple assignments"""
    source = "void main() { x = y = z = 5; }"
    assert Parser(source).parse() == "success"


def test_unary_expression():
    """41. Unary expression"""
    source = "void main() { x = -1; }"
    assert Parser(source).parse() == "success"


def test_prefix_increment():
    """42. Prefix increment"""
    source = "void main() { ++x; }"
    assert Parser(source).parse() == "success"


def test_postfix_increment():
    """43. Postfix increment"""
    source = "void main() { x++; }"
    assert Parser(source).parse() == "success"


def test_complex_boolean_expr():
    """44. Complex boolean expression"""
    source = "void main() { if (a && b || c) x = 1; }"
    assert Parser(source).parse() == "success"


def test_relational_expression():
    """45. Relational expression"""
    source = "void main() { if (a < b) x = 1; }"
    assert Parser(source).parse() == "success"


def test_equality_expression():
    """46. Equality expression"""
    source = "void main() { if (a == b) x = 1; }"
    assert Parser(source).parse() == "success"


def test_function_call_with_args():
    """47. Function call with arguments"""
    source = "void main() { foo(1, 2, 3); }"
    assert Parser(source).parse() == "success"


def test_nested_function_calls():
    """48. Nested function calls"""
    source = "void main() { foo(bar(1)); }"
    assert Parser(source).parse() == "success"


def test_struct_literal():
    """49. Struct literal"""
    source = "void main() { x = {1, 2}; }"
    assert Parser(source).parse() == "success"


def test_array_declaration():
    """50. Array declaration"""
    source = "void main() { int a[10]; }"
    assert Parser(source).parse() == "success"


def test_array_access():
    """51. Array access"""
    source = "void main() { a[0] = 1; }"
    assert Parser(source).parse() == "success"


def test_member_access():
    """52. Struct member access"""
    source = "void main() { p.x = 1; }"
    assert Parser(source).parse() == "success"


def test_chained_member_access():
    """53. Chained member access"""
    source = "void main() { a.b.c = 1; }"
    assert Parser(source).parse() == "success"


def test_switch_empty():
    """54. Empty switch"""
    source = "void main() { switch (x) { } }"
    assert Parser(source).parse() == "success"


def test_switch_case_no_stmt():
    """55. Case without statements"""
    source = "void main() { switch (x) { case 1: } }"
    assert Parser(source).parse() == "success"


def test_break_statement():
    """56. Break statement"""
    source = "void main() { while (1) break; }"
    assert Parser(source).parse() == "success"


def test_continue_statement():
    """57. Continue statement"""
    source = "void main() { while (1) continue; }"
    assert Parser(source).parse() == "success"


def test_return_expression_complex():
    """58. Return complex expression"""
    source = "int f() { return 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_multiple_return_paths():
    """59. Multiple return paths"""
    source = "int f() { if (1) return 1; return 2; }"
    assert Parser(source).parse() == "success"


def test_program_only_structs():
    """60. Program with only structs"""
    source = """
        struct A { int x; };
        struct B { float y; };
    """
    assert Parser(source).parse() == "success"


def test_long_expression_chain():
    """61. Long arithmetic expression"""
    source = "void main() { x = 1 + 2 - 3 * 4 / 5 % 6; }"
    assert Parser(source).parse() == "success"


def test_parenthesized_expression():
    """62. Parenthesized expression"""
    source = "void main() { x = (1 + 2) * (3 + 4); }"
    assert Parser(source).parse() == "success"


def test_nested_parentheses():
    """63. Deep nested parentheses"""
    source = "void main() { x = (((1))); }"
    assert Parser(source).parse() == "success"


def test_if_with_complex_condition():
    """64. If with complex condition"""
    source = "void main() { if ((a < b) && (c > d)) x = 1; }"
    assert Parser(source).parse() == "success"


def test_if_else_nested_blocks():
    """65. If-else with nested blocks"""
    source = "void main() { if (1) { x = 1; } else { x = 2; } }"
    assert Parser(source).parse() == "success"


def test_multiple_empty_statements():
    """66. Multiple empty statements"""
    source = "void main() { ;;; }"
    assert Parser(source).parse() == "success"


def test_for_all_empty_parts():
    """67. For loop with all empty parts"""
    source = "void main() { for (;;) x = 1; }"
    assert Parser(source).parse() == "success"


def test_while_with_empty_stmt():
    """68. While with empty statement"""
    source = "void main() { while (1) ; }"
    assert Parser(source).parse() == "success"


def test_switch_only_default():
    """69. Switch with only default"""
    source = "void main() { switch (x) { default: break; } }"
    assert Parser(source).parse() == "success"


def test_switch_case_fallthrough():
    """70. Switch case fallthrough"""
    source = """
        void main() {
            switch (x) {
                case 1:
                case 2:
                    x = 3;
                    break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_nested_switch():
    """71. Nested switch"""
    source = """
        void main() {
            switch (a) {
                case 1:
                    switch (b) {
                        case 2: x = 1; break;
                    }
                    break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_function_call_in_condition():
    """72. Function call in condition"""
    source = "void main() { if (foo()) x = 1; }"
    assert Parser(source).parse() == "success"


def test_function_call_in_expression():
    """73. Function call in expression"""
    source = "void main() { x = foo(1) + bar(2); }"
    assert Parser(source).parse() == "success"


def test_chained_function_calls():
    """74. Chained function calls"""
    source = "void main() { foo()(1); }"
    assert Parser(source).parse() == "success"


def test_array_access_expression():
    """75. Array access in expression"""
    source = "void main() { x = a[i + 1]; }"
    assert Parser(source).parse() == "success"


def test_array_access_nested():
    """76. Nested array access"""
    source = "void main() { x = a[b[c]]; }"
    assert Parser(source).parse() == "success"


def test_struct_member_expression():
    """77. Struct member in expression"""
    source = "void main() { x = p.a + p.b; }"
    assert Parser(source).parse() == "success"


def test_struct_member_function_call():
    """78. Function call on struct member"""
    source = "void main() { p.f(1); }"
    assert Parser(source).parse() == "success"


def test_assignment_to_member():
    """79. Assignment to struct member"""
    source = "void main() { p.x = 10; }"
    assert Parser(source).parse() == "success"


def test_assignment_to_array_member():
    """80. Assignment to array element"""
    source = "void main() { a[0] = 5; }"
    assert Parser(source).parse() == "success"


def test_prefix_and_postfix_mix():
    """81. Mix prefix and postfix"""
    source = "void main() { ++i; j++; }"
    assert Parser(source).parse() == "success"


def test_multiple_unary_ops():
    """82. Multiple unary operators"""
    source = "void main() { x = ---y; }"
    assert Parser(source).parse() == "success"


def test_not_operator_chain():
    """83. Chain of NOT operators"""
    source = "void main() { if (!!a) x = 1; }"
    assert Parser(source).parse() == "success"


def test_assignment_in_expression():
    """84. Assignment inside expression"""
    source = "void main() { x = (y = 3); }"
    assert Parser(source).parse() == "success"


def test_return_struct_literal():
    """85. Return struct literal"""
    source = "auto f() { return {1, 2}; }"
    assert Parser(source).parse() == "success"


def test_function_only_return():
    """86. Function with only return"""
    source = "int f() { return 0; }"
    assert Parser(source).parse() == "success"


def test_empty_parameter_list_spacing():
    """87. Empty parameter list with spaces"""
    source = "void main( ) { }"
    assert Parser(source).parse() == "success"


def test_multiple_functions_and_structs():
    """88. Multiple structs and functions"""
    source = """
        struct A { int x; };
        struct B { int y; };
        void f() {}
        void g() {}
    """
    assert Parser(source).parse() == "success"


def test_program_with_only_functions():
    """89. Program with only functions"""
    source = """
        int f() { return 1; }
        int g() { return 2; }
    """
    assert Parser(source).parse() == "success"


def test_deep_nested_blocks():
    """90. Deep nested blocks"""
    source = "void main() { {{{ x = 1; }}} }"
    assert Parser(source).parse() == "success"


def test_91_multiple_empty_blocks():
    """91. Multiple empty blocks"""
    source = "void main() { {} {} }"
    assert Parser(source).parse() == "success"


def test_92_if_with_empty_statement():
    """92. If with empty statement"""
    source = "void main() { if (1) ; }"
    assert Parser(source).parse() == "success"


def test_93_if_else_empty():
    """93. If-else with empty statements"""
    source = "void main() { if (1) ; else ; }"
    assert Parser(source).parse() == "success"


def test_94_while_with_break_block():
    """94. While loop with break in block"""
    source = "void main() { while (1) { break; } }"
    assert Parser(source).parse() == "success"


def test_95_while_with_continue_block():
    """95. While loop with continue in block"""
    source = "void main() { while (1) { continue; } }"
    assert Parser(source).parse() == "success"


def test_96_for_with_return():
    """96. For loop with return"""
    source = "void main() { for (;;) return; }"
    assert Parser(source).parse() == "success"


def test_97_switch_with_only_break():
    """97. Switch with only break"""
    source = "void main() { switch (x) { case 1: break; } }"
    assert Parser(source).parse() == "success"


def test_98_switch_multiple_defaults():
    """98. Switch with default and cases"""
    source = """
        void main() {
            switch (x) {
                case 1: x = 1; break;
                default: x = 0; break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_99_expression_only_program():
    """99. Expression inside function"""
    source = "void main() { (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"


def test_100_assignment_chain_long():
    """100. Long assignment chain"""
    source = "void main() { a = b = c = d = 1; }"
    assert Parser(source).parse() == "success"


def test_101_function_param_array():
    """101. Function parameter array"""
    source = "void f(int a[10]) {}"
    assert Parser(source).parse() == "success"


def test_102_local_array_decl():
    """102. Local array declaration"""
    source = "void main() { float b[5]; }"
    assert Parser(source).parse() == "success"


def test_103_array_index_expression():
    """103. Array index expression"""
    source = "void main() { x = arr[i * 2]; }"
    assert Parser(source).parse() == "success"


def test_104_struct_type_variable():
    """104. Struct type variable"""
    source = "struct A { int x; }; void main() { A a; }"
    assert Parser(source).parse() == "success"


def test_105_struct_type_param():
    """105. Struct type parameter"""
    source = "struct A { int x; }; void f(A a) {}"
    assert Parser(source).parse() == "success"


def test_106_auto_variable_no_init():
    """106. Auto variable without init"""
    source = "void main() { auto x; }"
    assert Parser(source).parse() == "success"


def test_107_auto_multiple_vars():
    """107. Auto multiple variables"""
    source = "void main() { auto x = 1, y = 2; }"
    assert Parser(source).parse() == "success"


def test_108_nested_function_blocks():
    """108. Nested blocks inside function"""
    source = "void main() { { { return; } } }"
    assert Parser(source).parse() == "success"


def test_109_function_call_as_expr_stmt():
    """109. Function call as expression statement"""
    source = "void main() { foo(1 + 2); }"
    assert Parser(source).parse() == "success"


def test_110_function_call_with_member_arg():
    """110. Function call with member argument"""
    source = "void main() { foo(p.x); }"
    assert Parser(source).parse() == "success"


def test_111_complex_member_chain():
    """111. Complex member chain"""
    source = "void main() { a.b.c.d = 1; }"
    assert Parser(source).parse() == "success"


def test_112_complex_array_chain():
    """112. Complex array chain"""
    source = "void main() { a[b[c[d]]] = 1; }"
    assert Parser(source).parse() == "success"


def test_113_mixed_array_member():
    """113. Mixed array and member access"""
    source = "void main() { a.b[c].d = 1; }"
    assert Parser(source).parse() == "success"


def test_114_return_array_access():
    """114. Return array access"""
    source = "int f() { return a[0]; }"
    assert Parser(source).parse() == "success"


def test_115_return_member_access():
    """115. Return member access"""
    source = "int f() { return p.x; }"
    assert Parser(source).parse() == "success"


def test_116_return_function_call():
    """116. Return function call"""
    source = "int f() { return foo(1); }"
    assert Parser(source).parse() == "success"


def test_117_switch_nested_if():
    """117. Switch with nested if"""
    source = """
        void main() {
            switch (x) {
                case 1:
                    if (x) y = 1;
                    break;
            }
        }
    """
    assert Parser(source).parse() == "success"


def test_118_for_with_complex_init():
    """118. For with complex init"""
    source = "void main() { for (i = j = 0; i < 10; i++) ; }"
    assert Parser(source).parse() == "success"


def test_119_while_with_complex_condition():
    """119. While with complex condition"""
    source = "void main() { while (a < b && b < c) x++; }"
    assert Parser(source).parse() == "success"


def test_120_full_program_mix():
    """120. Full mixed program"""
    source = """
        struct P { int x; int y; };
        int sum(int a, int b) { return a + b; }
        void main() {
            P p;
            p.x = sum(1, 2);
            while (p.x < 10) p.x++;
        }
    """
    assert Parser(source).parse() == "success"
