"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *
from antlr4.tree.Tree import TerminalNode

class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    def flatten(self, lst):
        res = []
        for item in lst:
            if isinstance(item, list):
                res.extend(self.flatten(item))
            elif item is not None:
                res.append(item)
        return res

    # =========================================================
    # Program & Declarations
    # =========================================================
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        decls = self.flatten(self.visit(ctx.unit()))
        return Program(decls)

    def visitUnit(self, ctx: TyCParser.UnitContext):
        return [self.visit(d) for d in ctx.declaration()]

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        name = ctx.ID().getText()
        members = [self.visit(f) for f in ctx.fieldDecl()]
        return StructDecl(name, members)

    def visitFieldDecl(self, ctx: TyCParser.FieldDeclContext):
        typ = self.visit(ctx.typeSpec())
        var_name = ctx.varRef().ID().getText()
        return MemberDecl(typ, var_name)

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        return_type = self.visit(ctx.returnType()) if ctx.returnType() else None
        name = ctx.ID().getText()
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        return [self.visit(p) for p in ctx.param()]

    def visitParam(self, ctx: TyCParser.ParamContext):
        typ = self.visit(ctx.typeSpec())
        name = ctx.varRef().ID().getText()
        return Param(typ, name)

    # =========================================================
    # Types
    # =========================================================
    def visitReturnType(self, ctx: TyCParser.ReturnTypeContext):
        if ctx.VOID():
            return VoidType()
        if ctx.AUTO():
            return None  
        return self.visit(ctx.typeSpec())

    def visitTypeSpec(self, ctx: TyCParser.TypeSpecContext):
        if ctx.INT(): return IntType()
        if ctx.FLOAT(): return FloatType()
        if ctx.STRING(): return StringType()
        return StructType(ctx.ID().getText())

    # =========================================================
    # Statements
    # =========================================================
    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        stmts = self.flatten([self.visit(s) for s in ctx.stmt()])
        return BlockStmt(stmts)

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        typ = self.visit(ctx.returnType())
        var_init_list = self.visit(ctx.varInitList())
        return [VarDecl(typ, name, init) for name, init in var_init_list]

    def visitVarInitList(self, ctx: TyCParser.VarInitListContext):
        return [self.visit(v) for v in ctx.varInit()]

    def visitVarInit(self, ctx: TyCParser.VarInitContext):
        name = ctx.varRef().ID().getText()
        init = self.visit(ctx.expr()) if ctx.expr() else None
        return (name, init)

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        cond = self.visit(ctx.expr())
        then_stmt = self.visit(ctx.stmt(0))
        else_stmt = self.visit(ctx.stmt(1)) if ctx.ELSE() else None
        return IfStmt(cond, then_stmt, else_stmt)

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        return WhileStmt(self.visit(ctx.expr()), self.visit(ctx.stmt()))

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        init = None
        if ctx.varDecl():
            # AST Node ForStmt chỉ chấp nhận 1 VarDecl duy nhất cho init
            init = self.visit(ctx.varDecl())[0] 
        elif ctx.exprStmt():
            init = self.visit(ctx.exprStmt())

        cond = None
        update = None
        
        # State machine để bắt chính xác điều kiện và bước nhảy
        state = 0 
        for child in ctx.getChildren():
            if child == ctx.varDecl() or child == ctx.exprStmt():
                state = 1
            elif isinstance(child, TerminalNode) and child.getText() == ';':
                state += 1
            elif isinstance(child, TyCParser.ExprContext):
                if state == 1:
                    cond = self.visit(child)
                elif state == 2:
                    update = self.visit(child)

        body = self.visit(ctx.stmt())
        return ForStmt(init, cond, update, body)

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        expr = self.visit(ctx.expr())
        cases = [self.visit(c) for c in ctx.caseStmt()]
        default = self.visit(ctx.defaultStmt()) if ctx.defaultStmt() else None
        return SwitchStmt(expr, cases, default)

    def visitCaseStmt(self, ctx: TyCParser.CaseStmtContext):
        expr = self.visit(ctx.expr())
        stmts = self.flatten([self.visit(s) for s in ctx.stmt()])
        return CaseStmt(expr, stmts)

    def visitDefaultStmt(self, ctx: TyCParser.DefaultStmtContext):
        stmts = self.flatten([self.visit(s) for s in ctx.stmt()])
        return DefaultStmt(stmts)

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ReturnStmt(expr)

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        expr = self.visit(ctx.expr()) if ctx.expr() else None
        return ExprStmt(expr)

    # =========================================================
    # Expressions
    # =========================================================
    def visitParenExpr(self, ctx: TyCParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitArrayExpr(self, ctx: TyCParser.ArrayExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), "[]", self.visit(ctx.expr(1)))

    def visitCallExpr(self, ctx: TyCParser.CallExprContext):
        func = self.visit(ctx.expr())
        args = self.visit(ctx.argList()) if ctx.argList() else []
        # Hàm trong TyC luôn là toàn cục, Node FuncCall bắt buộc name là chuỗi
        func_name = func.name if isinstance(func, Identifier) else str(func)
        return FuncCall(func_name, args)

    def visitMemberExpr(self, ctx: TyCParser.MemberExprContext):
        obj = self.visit(ctx.expr())
        member = ctx.ID().getText()
        return MemberAccess(obj, member)

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        return PostfixOp(ctx.getChild(1).getText(), self.visit(ctx.expr()))

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.expr()))

    def visitMulExpr(self, ctx: TyCParser.MulExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), ctx.getChild(1).getText(), self.visit(ctx.expr(1)))

    def visitAddExpr(self, ctx: TyCParser.AddExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), ctx.getChild(1).getText(), self.visit(ctx.expr(1)))

    def visitRelExpr(self, ctx: TyCParser.RelExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), ctx.getChild(1).getText(), self.visit(ctx.expr(1)))

    def visitEqExpr(self, ctx: TyCParser.EqExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), ctx.getChild(1).getText(), self.visit(ctx.expr(1)))

    def visitAndExpr(self, ctx: TyCParser.AndExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), "&&", self.visit(ctx.expr(1)))

    def visitOrExpr(self, ctx: TyCParser.OrExprContext):
        return BinaryOp(self.visit(ctx.expr(0)), "||", self.visit(ctx.expr(1)))

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        return AssignExpr(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        return self.visit(ctx.primary())

    def visitIdExpr(self, ctx: TyCParser.IdExprContext):
        return Identifier(ctx.ID().getText())

    def visitIntExpr(self, ctx: TyCParser.IntExprContext):
        return IntLiteral(int(ctx.INT_LIT().getText()))

    def visitFloatExpr(self, ctx: TyCParser.FloatExprContext):
        return FloatLiteral(float(ctx.FLOAT_LIT().getText()))

    def visitStringExpr(self, ctx: TyCParser.StringExprContext):
        return StringLiteral(ctx.STRING_LIT().getText().strip('"'))

    def visitStructExpr(self, ctx: TyCParser.StructExprContext):
        values = self.visit(ctx.argList()) if ctx.argList() else []
        return StructLiteral(values)

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        return [self.visit(e) for e in ctx.expr()]