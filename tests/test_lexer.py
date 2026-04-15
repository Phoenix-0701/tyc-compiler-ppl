"""
Lexer test cases for TyC compiler
100 extended test cases
"""

import pytest
from tests.utils import Tokenizer
from lexererr import UncloseString, IllegalEscape, ErrorToken


def test_01_keyword_auto():
    assert Tokenizer("auto").get_tokens_as_string() == "auto,<EOF>"

def test_02_keyword_int():
    assert Tokenizer("int").get_tokens_as_string() == "int,<EOF>"

def test_03_keyword_float():
    assert Tokenizer("float").get_tokens_as_string() == "float,<EOF>"

def test_04_keyword_void():
    assert Tokenizer("void").get_tokens_as_string() == "void,<EOF>"

def test_05_keyword_struct():
    assert Tokenizer("struct").get_tokens_as_string() == "struct,<EOF>"

def test_06_keyword_if():
    assert Tokenizer("if").get_tokens_as_string() == "if,<EOF>"

def test_07_keyword_else():
    assert Tokenizer("else").get_tokens_as_string() == "else,<EOF>"

def test_08_keyword_for():
    assert Tokenizer("for").get_tokens_as_string() == "for,<EOF>"

def test_09_keyword_while():
    assert Tokenizer("while").get_tokens_as_string() == "while,<EOF>"

def test_10_keyword_return():
    assert Tokenizer("return").get_tokens_as_string() == "return,<EOF>"



def test_11_id_simple():
    assert Tokenizer("x").get_tokens_as_string() == "x,<EOF>"

def test_12_id_with_number():
    assert Tokenizer("x1").get_tokens_as_string() == "x1,<EOF>"

def test_13_id_underscore():
    assert Tokenizer("_abc").get_tokens_as_string() == "_abc,<EOF>"

def test_14_id_long():
    assert Tokenizer("thisIsALongIdentifier").get_tokens_as_string() == "thisIsALongIdentifier,<EOF>"

def test_15_id_mixed():
    assert Tokenizer("a_b_c123").get_tokens_as_string() == "a_b_c123,<EOF>"

def test_16_id_keyword_like():
    assert Tokenizer("auto1").get_tokens_as_string() == "auto1,<EOF>"

def test_17_id_uppercase():
    assert Tokenizer("ABC").get_tokens_as_string() == "ABC,<EOF>"

def test_18_id_snake_case():
    assert Tokenizer("snake_case").get_tokens_as_string() == "snake_case,<EOF>"

def test_19_id_single_char():
    assert Tokenizer("i").get_tokens_as_string() == "i,<EOF>"

def test_20_id_with_digits():
    assert Tokenizer("var2025").get_tokens_as_string() == "var2025,<EOF>"



def test_21_int_zero():
    assert Tokenizer("0").get_tokens_as_string() == "0,<EOF>"

def test_22_int_positive():
    assert Tokenizer("123").get_tokens_as_string() == "123,<EOF>"

def test_23_float_simple():
    assert Tokenizer("3.14").get_tokens_as_string() == "3.14,<EOF>"

def test_24_float_no_fraction():
    assert Tokenizer("10.").get_tokens_as_string() == "10.,<EOF>"

def test_25_float_leading_dot():
    assert Tokenizer(".5").get_tokens_as_string() == ".5,<EOF>"

def test_26_float_scientific():
    assert Tokenizer("1e10").get_tokens_as_string() == "1e10,<EOF>"

def test_27_float_scientific_upper():
    assert Tokenizer("2E3").get_tokens_as_string() == "2E3,<EOF>"

def test_28_float_scientific_sign():
    assert Tokenizer("1.2e-3").get_tokens_as_string() == "1.2e-3,<EOF>"

def test_29_int_in_expr():
    assert Tokenizer("1+2").get_tokens_as_string() == "1,+,2,<EOF>"

def test_30_float_in_expr():
    assert Tokenizer("1.5*2").get_tokens_as_string() == "1.5,*,2,<EOF>"



def test_41_string_simple():
    assert Tokenizer('"hello"').get_tokens_as_string() == "hello,<EOF>"

def test_42_string_space():
    assert Tokenizer('"hello world"').get_tokens_as_string() == "hello world,<EOF>"

def test_43_string_escape_n():
    assert Tokenizer('"a\\n"').get_tokens_as_string() == "a\\n,<EOF>"

def test_44_string_escape_t():
    assert Tokenizer('"a\\t"').get_tokens_as_string() == "a\\t,<EOF>"

def test_45_string_escape_quote():
    assert Tokenizer('"a\\""').get_tokens_as_string() == 'a\\",<EOF>'

def test_46_string_empty():
    assert Tokenizer('""').get_tokens_as_string() == ",<EOF>"

def test_47_string_many_chars():
    assert Tokenizer('"abcdef123"').get_tokens_as_string() == "abcdef123,<EOF>"

def test_48_string_symbols():
    assert Tokenizer('"!@#$%"').get_tokens_as_string() == "!@#$%,<EOF>"

def test_49_string_number():
    assert Tokenizer('"123"').get_tokens_as_string() == "123,<EOF>"

def test_50_string_mixed():
    assert Tokenizer('"a1_b2"').get_tokens_as_string() == "a1_b2,<EOF>"



def test_56_assign():
    assert Tokenizer("=").get_tokens_as_string() == "=,<EOF>"

def test_57_equal():
    assert Tokenizer("==").get_tokens_as_string() == "==,<EOF>"

def test_58_not_equal():
    assert Tokenizer("!=").get_tokens_as_string() == "!=,<EOF>"

def test_59_plus():
    assert Tokenizer("+").get_tokens_as_string() == "+,<EOF>"

def test_60_minus():
    assert Tokenizer("-").get_tokens_as_string() == "-,<EOF>"

def test_61_mul():
    assert Tokenizer("*").get_tokens_as_string() == "*,<EOF>"

def test_62_div():
    assert Tokenizer("/").get_tokens_as_string() == "/,<EOF>"

def test_63_mod():
    assert Tokenizer("%").get_tokens_as_string() == "%,<EOF>"

def test_64_and():
    assert Tokenizer("&&").get_tokens_as_string() == "&&,<EOF>"

def test_65_or():
    assert Tokenizer("||").get_tokens_as_string() == "||,<EOF>"

def test_66_inc():
    assert Tokenizer("++").get_tokens_as_string() == "++,<EOF>"

def test_67_dec():
    assert Tokenizer("--").get_tokens_as_string() == "--,<EOF>"

def test_68_semi():
    assert Tokenizer(";").get_tokens_as_string() == ";,<EOF>"

def test_69_comma():
    assert Tokenizer(",").get_tokens_as_string() == ",,<EOF>"

def test_70_paren():
    assert Tokenizer("()").get_tokens_as_string() == "(,),<EOF>"

def test_71_brace():
    assert Tokenizer("{}").get_tokens_as_string() == "{,},<EOF>"

def test_72_square():
    assert Tokenizer("[]").get_tokens_as_string() == "[,],<EOF>"

def test_73_colon():
    assert Tokenizer(":").get_tokens_as_string() == ":,<EOF>"

def test_74_dot():
    assert Tokenizer(".").get_tokens_as_string() == ".,<EOF>"

def test_75_complex_ops():
    assert Tokenizer("a+=1").get_tokens_as_string() == "a,+,=,1,<EOF>"



def test_76_line_comment():
    assert Tokenizer("// hello").get_tokens_as_string() == "<EOF>"

def test_77_block_comment():
    assert Tokenizer("/* comment */").get_tokens_as_string() == "<EOF>"

def test_78_block_comment_nested_text():
    assert Tokenizer("/* abc * def */").get_tokens_as_string() == "<EOF>"

def test_79_comment_with_code():
    assert Tokenizer("int x; // comment").get_tokens_as_string() == "int,x,;,<EOF>"

def test_80_whitespace():
    assert Tokenizer("   \n\t ").get_tokens_as_string() == "<EOF>"

def test_81_newline_tokens():
    assert Tokenizer("int\nx").get_tokens_as_string() == "int,x,<EOF>"

def test_82_tabs():
    assert Tokenizer("int\tx").get_tokens_as_string() == "int,x,<EOF>"

def test_83_multiple_lines():
    assert Tokenizer("int x;\nfloat y;").get_tokens_as_string() == "int,x,;,float,y,;,<EOF>"

def test_84_comment_after_code():
    assert Tokenizer("x=1/*c*/").get_tokens_as_string() == "x,=,1,<EOF>"

def test_85_comment_only():
    assert Tokenizer("/* only comment */").get_tokens_as_string() == "<EOF>"



def test_86_multiple_identifiers():
    tokenizer = Tokenizer("a b c")
    assert tokenizer.get_tokens_as_string() == "a,b,c,<EOF>"


def test_87_assignment_chain():
    tokenizer = Tokenizer("a = b = 10")
    assert tokenizer.get_tokens_as_string() == "a,=,b,=,10,<EOF>"


def test_88_arithmetic_sequence():
    tokenizer = Tokenizer("1 + 2 - 3 * 4 / 5")
    assert tokenizer.get_tokens_as_string() == "1,+,2,-,3,*,4,/,5,<EOF>"


def test_89_parenthesized_expression():
    tokenizer = Tokenizer("(1 + 2) * 3")
    assert tokenizer.get_tokens_as_string() == "(,1,+,2,),*,3,<EOF>"


def test_90_function_like_call():
    tokenizer = Tokenizer("foo(1,2)")
    assert tokenizer.get_tokens_as_string() == "foo,(,1,,,2,),<EOF>"


def test_91_block_statement():
    tokenizer = Tokenizer("{ x = 1; }")
    assert tokenizer.get_tokens_as_string() == "{,x,=,1,;,},<EOF>"


def test_92_comparison_expression():
    tokenizer = Tokenizer("a == b")
    assert tokenizer.get_tokens_as_string() == "a,==,b,<EOF>"


def test_93_mixed_comparisons():
    tokenizer = Tokenizer("x != y")
    assert tokenizer.get_tokens_as_string() == "x,!=,y,<EOF>"


def test_94_float_expression():
    tokenizer = Tokenizer("1.5 + 2.0")
    assert tokenizer.get_tokens_as_string() == "1.5,+,2.0,<EOF>"


def test_95_variable_declaration_simple():
    tokenizer = Tokenizer("auto y = 10;")
    assert tokenizer.get_tokens_as_string() == "auto,y,=,10,;,<EOF>"


def test_96_multiple_statements():
    tokenizer = Tokenizer("x=1;y=2;")
    assert tokenizer.get_tokens_as_string() == "x,=,1,;,y,=,2,;,<EOF>"


def test_97_nested_parentheses():
    tokenizer = Tokenizer("((x))")
    assert tokenizer.get_tokens_as_string() == "(,(,x,),),<EOF>"


def test_98_comment_after_code():
    tokenizer = Tokenizer("x = 1; // comment")
    assert tokenizer.get_tokens_as_string() == "x,=,1,;,<EOF>"


def test_99_long_identifier():
    tokenizer = Tokenizer("thisIsAVeryLongIdentifier")
    assert tokenizer.get_tokens_as_string() == "thisIsAVeryLongIdentifier,<EOF>"


def test_100_simple_program():
    tokenizer = Tokenizer("auto a=1; auto b=2;")
    assert tokenizer.get_tokens_as_string() == "auto,a,=,1,;,auto,b,=,2,;,<EOF>"


def test_101_boolean_true():
    """101. Boolean literal true"""
    tokenizer = Tokenizer("true")
    assert tokenizer.get_tokens_as_string() == "true,<EOF>"


def test_102_boolean_false():
    """102. Boolean literal false"""
    tokenizer = Tokenizer("false")
    assert tokenizer.get_tokens_as_string() == "false,<EOF>"


def test_103_multiple_identifiers():
    """103. Multiple identifiers"""
    tokenizer = Tokenizer("a b c")
    assert tokenizer.get_tokens_as_string() == "a,b,c,<EOF>"


def test_104_nested_parentheses():
    """104. Nested parentheses"""
    tokenizer = Tokenizer("((x))")
    assert tokenizer.get_tokens_as_string() == "(,(,x,),),<EOF>"


def test_105_array_indexing():
    """105. Array indexing"""
    tokenizer = Tokenizer("a[10]")
    assert tokenizer.get_tokens_as_string() == "a,[,10,],<EOF>"


def test_106_function_call_no_args():
    """106. Function call without arguments"""
    tokenizer = Tokenizer("foo()")
    assert tokenizer.get_tokens_as_string() == "foo,(,),<EOF>"


def test_107_function_call_with_args():
    """107. Function call with arguments"""
    tokenizer = Tokenizer("foo(1,2)")
    assert tokenizer.get_tokens_as_string() == "foo,(,1,,,2,),<EOF>"


def test_108_increment_prefix():
    """108. Prefix increment"""
    tokenizer = Tokenizer("++i")
    assert tokenizer.get_tokens_as_string() == "++,i,<EOF>"


def test_109_increment_postfix():
    """109. Postfix increment"""
    tokenizer = Tokenizer("i++")
    assert tokenizer.get_tokens_as_string() == "i,++,<EOF>"


def test_110_decrement_prefix():
    """110. Prefix decrement"""
    tokenizer = Tokenizer("--i")
    assert tokenizer.get_tokens_as_string() == "--,i,<EOF>"


def test_111_relational_operator():
    """111. Relational operator"""
    tokenizer = Tokenizer("a<=b")
    assert tokenizer.get_tokens_as_string() == "a,<=,b,<EOF>"


def test_112_logical_and():
    """112. Logical AND"""
    tokenizer = Tokenizer("a&&b")
    assert tokenizer.get_tokens_as_string() == "a,&&,b,<EOF>"


def test_113_logical_or():
    """113. Logical OR"""
    tokenizer = Tokenizer("a||b")
    assert tokenizer.get_tokens_as_string() == "a,||,b,<EOF>"


def test_114_not_operator():
    """114. Logical NOT"""
    tokenizer = Tokenizer("!a")
    assert tokenizer.get_tokens_as_string() == "!,a,<EOF>"


def test_115_assignment_chain():
    """115. Chained assignment"""
    tokenizer = Tokenizer("a=b=c")
    assert tokenizer.get_tokens_as_string() == "a,=,b,=,c,<EOF>"


def test_116_empty_braces():
    """116. Empty braces"""
    tokenizer = Tokenizer("{}")
    assert tokenizer.get_tokens_as_string() == "{,},<EOF>"


def test_117_return_statement():
    """117. Return statement"""
    tokenizer = Tokenizer("return 0;")
    assert tokenizer.get_tokens_as_string() == "return,0,;,<EOF>"


def test_118_struct_keyword():
    """118. Struct keyword"""
    tokenizer = Tokenizer("struct")
    assert tokenizer.get_tokens_as_string() == "struct,<EOF>"


def test_119_typedef_like_identifier():
    """119. Typedef-like identifier"""
    tokenizer = Tokenizer("MyType")
    assert tokenizer.get_tokens_as_string() == "MyType,<EOF>"


def test_120_multiple_separators():
    """120. Multiple separators"""
    tokenizer = Tokenizer("int a = 6;")
    assert tokenizer.get_tokens_as_string() == "int,a,=,6,;,<EOF>"
