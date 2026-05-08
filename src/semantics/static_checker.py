"""
Static Semantic Checker for TyC Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, TYPE_CHECKING
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .static_error import *

TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]

class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Optional[Type]]] = [{}]
        self.current_func_params: Set[str] = set()

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name: str, var_type: Optional[Type], kind: str):
        if name in self.scopes[-1]:
            raise Redeclared(kind, name)
        if kind == "Variable" and name in self.current_func_params:
            raise Redeclared("Variable", name)
            
        self.scopes[-1][name] = var_type

    def lookup(self, name: str) -> Optional[Type]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise UndeclaredIdentifier(name)

    def update_type(self, name: str, new_type: Type):
        for scope in reversed(self.scopes):
            if name in scope:
                if scope[name] is None:
                    scope[name] = new_type
                return


class StaticChecker(ASTVisitor):
    def __init__(self):
        self.sym_table = SymbolTable()
        self.structs: Dict[str, Dict[str, Type]] = {}
        self.functions: Dict[str, Tuple[Optional[Type], List[Type]]] = {}
        
        self.loop_depth = 0
        self.switch_depth = 0
        self.current_func_name = ""
        self.current_func_return: Optional[Type] = None
        
        self._init_builtins()

    def check_program(self, ast):
        return ast.accept(self, None)
    
    def _init_builtins(self):
        self.functions['readInt'] = (IntType(), [])
        self.functions['readFloat'] = (FloatType(), [])
        self.functions['readString'] = (StringType(), [])
        self.functions['printInt'] = (VoidType(), [IntType()])
        self.functions['printFloat'] = (VoidType(), [FloatType()])
        self.functions['printString'] = (VoidType(), [StringType()])

    def is_same_type(self, type1: Type, type2: Type) -> bool:
        if type(type1) != type(type2):
            return False
        if isinstance(type1, StructType) and isinstance(type2, StructType):
            return type1.struct_name == type2.struct_name
        return True

    # =========================================================================
    # Program & Declarations
    # =========================================================================
    def visit_program(self, node: Program, o: Any = None):
        for decl in node.decls:
            decl.accept(self, o)


    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        if node.name in self.structs:
            raise Redeclared("Struct", node.name)
        
        members = {}
        for member in node.members:
            if member.name in members:
                raise Redeclared("Member", member.name)
            
            if isinstance(member.member_type, StructType):
                if member.member_type.struct_name not in self.structs:
                    raise UndeclaredStruct(member.member_type.struct_name)
                    
            members[member.name] = member.member_type
            
        self.structs[node.name] = members

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        pass

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        if node.name in self.functions:
            raise Redeclared("Function", node.name)
            
        param_types = []
        for param in node.params:
            if isinstance(param.param_type, StructType) and param.param_type.struct_name not in self.structs:
                raise UndeclaredStruct(param.param_type.struct_name)
            param_types.append(param.param_type)
            
        self.functions[node.name] = (node.return_type, param_types)
        
        self.current_func_name = node.name
        self.current_func_return = node.return_type
        
        self.sym_table = SymbolTable()
        self.sym_table.current_func_params = {p.name for p in node.params}
        self.sym_table.enter_scope() 
        
        for param in node.params:
            self.sym_table.declare(param.name, param.param_type, "Parameter")
            
        node.body.accept(self, o)
        
        self.sym_table.exit_scope()
        self.current_func_return = None
        self.current_func_name = ""

    def visit_param(self, node: Param, o: Any = None):
        pass

    def visit_var_decl(self, node: VarDecl, o: Any = None):
        init_type = node.init_value.accept(self, node.var_type) if node.init_value else None
        
        if node.var_type is None:
            if init_type is None:
                self.sym_table.declare(node.name, None, "Variable")
            else:
                self.sym_table.declare(node.name, init_type, "Variable")
        else:
            if isinstance(node.var_type, StructType) and node.var_type.struct_name not in self.structs:
                raise UndeclaredStruct(node.var_type.struct_name)
            
            if init_type is not None:
                if not self.is_same_type(node.var_type, init_type):
                    raise TypeMismatchInStatement(node)
                    
            self.sym_table.declare(node.name, node.var_type, "Variable")

    # =========================================================================
    # Statements
    # =========================================================================
    def visit_block_stmt(self, node: BlockStmt, o: Any = None):
        self.sym_table.enter_scope()
        for stmt in node.statements:
            stmt.accept(self, o)
            
        for name, var_type in self.sym_table.scopes[-1].items():
            if var_type is None:
                raise TypeCannotBeInferred(node)
                
        self.sym_table.exit_scope()

    def visit_if_stmt(self, node: IfStmt, o: Any = None):
        cond_type = node.condition.accept(self, o)
        if cond_type is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
            
        node.then_stmt.accept(self, o)
        if node.else_stmt:
            node.else_stmt.accept(self, o)

    def visit_while_stmt(self, node: WhileStmt, o: Any = None):
        cond_type = node.condition.accept(self, o)
        if cond_type is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(cond_type, IntType):
            raise TypeMismatchInStatement(node)
            
        self.loop_depth += 1
        node.body.accept(self, o)
        self.loop_depth -= 1

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        self.sym_table.enter_scope()
        
        if node.init:
            node.init.accept(self, o)
            
        if node.condition:
            cond_type = node.condition.accept(self, o)
            if cond_type is None:
                raise TypeCannotBeInferred(node)
            if not isinstance(cond_type, IntType):
                raise TypeMismatchInStatement(node)
                
        if node.update:
            node.update.accept(self, o)
            
        self.loop_depth += 1
        node.body.accept(self, o)
        self.loop_depth -= 1
        
        self.sym_table.exit_scope()

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        expr_type = node.expr.accept(self, o)
        if expr_type is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(expr_type, IntType):
            raise TypeMismatchInStatement(node)
            
        self.switch_depth += 1
        for case_stmt in node.cases:
            case_stmt.accept(self, o)
        if node.default_case:
            node.default_case.accept(self, o)
        self.switch_depth -= 1

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        case_expr_type = node.expr.accept(self, o)
        if case_expr_type is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(case_expr_type, IntType):
            raise TypeMismatchInStatement(node)
            
        self.sym_table.enter_scope()
        for stmt in node.statements:
            stmt.accept(self, o)
        self.sym_table.exit_scope()

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        self.sym_table.enter_scope()
        for stmt in node.statements:
            stmt.accept(self, o)
        self.sym_table.exit_scope()

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        if self.loop_depth == 0 and self.switch_depth == 0:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        if self.loop_depth == 0:
            raise MustInLoop(node)

    def visit_return_stmt(self, node: ReturnStmt, o: Any = None):
        ret_type = node.expr.accept(self, self.current_func_return) if node.expr else VoidType()

        if ret_type is None:
            raise TypeCannotBeInferred(node)
        
        if self.current_func_return is None:
            self.current_func_return = ret_type
            params = self.functions[self.current_func_name][1]
            self.functions[self.current_func_name] = (ret_type, params)
        else:
            if not self.is_same_type(self.current_func_return, ret_type):
                raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: ExprStmt, o: Any = None):
        node.expr.accept(self, o)

    # =========================================================================
    # Expressions
    # =========================================================================
    def visit_binary_op(self, node: BinaryOp, o: Any = None):
        # KHÔNG TRUYỀN `o` XUỐNG DƯỚI NỮA!
        left_type = node.left.accept(self, None)
        right_type = node.right.accept(self, None)
        
        if left_type is None and isinstance(node.right, IntLiteral):
            left_type = IntType()
            if isinstance(node.left, Identifier):
                self.sym_table.update_type(node.left.name, left_type)
                
        if right_type is None and isinstance(node.left, IntLiteral):
            right_type = IntType()
            if isinstance(node.right, Identifier):
                self.sym_table.update_type(node.right.name, right_type)

        if left_type is None or right_type is None:
             raise TypeCannotBeInferred(node)

        op = node.operator
        if op in ['+', '-', '*', '/']:
            if not isinstance(left_type, (IntType, FloatType)) or not isinstance(right_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
                return FloatType()
            return IntType()
            
        elif op == '%':
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif op in ['<', '<=', '>', '>=', '==', '!=']:
            if not isinstance(left_type, (IntType, FloatType)) or not isinstance(right_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif op in ['&&', '||']:
            if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif op == '[]':
            raise TypeMismatchInExpression(node)
    
    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        op_type = node.operand.accept(self, None) # Không truyền o
        if op_type is None:
            raise TypeCannotBeInferred(node)

        if node.operator in ['+', '-']:
            if not isinstance(op_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return op_type
            
        elif node.operator == '!':
            if not isinstance(op_type, IntType):
                raise TypeMismatchInExpression(node)
            return IntType()
            
        elif node.operator in ['++', '--']:
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            if not isinstance(op_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return op_type

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        op_type = node.operand.accept(self, None) # Không truyền o
        if op_type is None:
            raise TypeCannotBeInferred(node)

        if node.operator in ['++', '--']:
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
            if not isinstance(op_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return op_type

    def visit_assign_expr(self, node: AssignExpr, o: Any = None):
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        lhs_type = node.lhs.accept(self, o)
        rhs_type = node.rhs.accept(self, lhs_type)

        if lhs_type is None and rhs_type is not None:
            if isinstance(node.lhs, Identifier):
                self.sym_table.update_type(node.lhs.name, rhs_type)
                lhs_type = rhs_type
                
        if rhs_type is None and lhs_type is not None:
            if isinstance(node.rhs, Identifier):
                self.sym_table.update_type(node.rhs.name, lhs_type)
                rhs_type = lhs_type
        
        if lhs_type is None or rhs_type is None:
            raise TypeCannotBeInferred(node)
            
        if not self.is_same_type(lhs_type, rhs_type):
            raise TypeMismatchInExpression(node)
            
        return lhs_type

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        obj_type = node.obj.accept(self, o)
        if obj_type is None:
            raise TypeCannotBeInferred(node)
        if not isinstance(obj_type, StructType):
            raise TypeMismatchInExpression(node)
            
        struct_name = obj_type.struct_name
        if struct_name not in self.structs:
            raise UndeclaredStruct(struct_name)
            
        struct_members = self.structs[struct_name]
        if node.member not in struct_members:
            raise TypeMismatchInExpression(node)
            
        return struct_members[node.member]

    def visit_func_call(self, node: FuncCall, o: Any = None):
        # TyC không hỗ trợ gọi function pointers / method (Ví dụ: f(1).g())
        if not isinstance(node.name, str):
            raise TypeMismatchInExpression(node)
            
        if node.name not in self.functions:
            raise UndeclaredFunction(node.name)

        ret_type, param_types = self.functions[node.name]

        if len(node.args) != len(param_types):
            raise TypeMismatchInExpression(node)

        for arg, param_type in zip(node.args, param_types):
            arg_type = arg.accept(self, param_type)
            
            if arg_type is None:
                if isinstance(arg, Identifier):
                    self.sym_table.update_type(arg.name, param_type)
                    arg_type = param_type
                else:
                    raise TypeCannotBeInferred(arg)
            
            if not self.is_same_type(arg_type, param_type):
                raise TypeMismatchInExpression(node)

        return ret_type

    def visit_identifier(self, node: Identifier, o: Any = None):
        var_type = self.sym_table.lookup(node.name)
        if var_type is None and o is not None:
            self.sym_table.update_type(node.name, o)
            return o
        return var_type

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        if not isinstance(o, StructType):
            raise TypeMismatchInExpression(node)
            
        struct_name = o.struct_name
        if struct_name not in self.structs:
            raise UndeclaredStruct(struct_name)
            
        struct_members = self.structs[struct_name]
        if len(node.values) != len(struct_members):
            raise TypeMismatchInExpression(node)
            
        for arg, (member_name, expected_type) in zip(node.values, struct_members.items()):
            arg_type = arg.accept(self, expected_type)
            
            if arg_type is None:
                if isinstance(arg, Identifier):
                    self.sym_table.update_type(arg.name, expected_type)
                    arg_type = expected_type
                else:
                    raise TypeCannotBeInferred(node)
                    
            if not self.is_same_type(arg_type, expected_type):
                raise TypeMismatchInExpression(node)
                
        return o

    # =========================================================================
    # Literals & Types Base Methods
    # =========================================================================
    def visit_int_literal(self, node: IntLiteral, o: Any = None): return IntType()
    def visit_float_literal(self, node: FloatLiteral, o: Any = None): return FloatType()
    def visit_string_literal(self, node: StringLiteral, o: Any = None): return StringType()

    def visit_int_type(self, node: IntType, o: Any = None): return node
    def visit_float_type(self, node: FloatType, o: Any = None): return node
    def visit_string_type(self, node: StringType, o: Any = None): return node
    def visit_void_type(self, node: VoidType, o: Any = None): return node
    def visit_struct_type(self, node: StructType, o: Any = None): return node