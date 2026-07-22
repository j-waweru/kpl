from dataclasses import dataclass, field


import kpl.Token.Token as Token


# Valid code is a list of statements
# Statement and expression nodes are dummy methods to satisfy the interfaces . I don't think I'll need them.


class Node:
    def token_literal(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class Expression(Node):
    pass


class Statement(Node):
    pass


@dataclass
class Program(Node):
    """Root of the AST containing a list of statements"""

    statements: list[Statement] = field(default_factory=list)

    def token_literal(self):
        if self.statements:
            return self.statements[0].token_literal()
        return ""

    def __str__(self):
        return "".join(str(stmt) for stmt in self.statements)


@dataclass
class Identifier(Expression):
    Token: Token.Token
    Value: str

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.Token.Literal

    def __str__(self):
        return self.Value


@dataclass
class ExpressionStatement(Statement):
    Token: Token.Token
    Expression: Expression | None = None

    def statement_node(self):
        pass

    def token_literal(self) -> str:

        return self.Token.Literal

    def __str__(self):
        if self.Expression is not None:
            return str(self.Expression)


@dataclass
class RekaStatement(Statement):
    # name of the var pointing to the left expression
    # track the node associated with

    Token: Token.Token

    Name: Identifier | None = None
    Value: Expression | None = None

    def statement_node(self):
        pass

    def token_literal(self) -> str:

        return self.Token.Literal

    def __str__(self):
        out = []
        out.append(self.token_literal())
        out.append(" ")
        out.append(str(self.Name))
        out.append(" = ")
        if self.Value is not None:
            out.append(str(self.Value))
        out.append("$")
        return "".join(out)


@dataclass
class ChokiaStatement(Statement):
    Token: Token.Token
    ReturnValue: Expression | None = None

    def statement_node(self):
        pass

    def token_literal(self) -> str:

        return self.Token.Literal

    def __str__(self):
        out = []

        out.append(self.token_literal())
        out.append(" ")

        if self.ReturnValue is not None:
            out.append(str(self.ReturnValue))

        out.append("$")

        return "".join(out)


@dataclass
class IntegerLiteral(Expression):
    Token: Token.Token
    Value: int

    def expression_node():
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        return str(self.Token.Literal)


@dataclass
class PrefixExpression(Expression):
    Token: Token.Token  # Prefix token (!, -, etc.)
    Operator: str
    Right: Expression | None = None

    def expression_node(self):
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        out = []

        out.append("(")
        out.append(self.Operator)

        if self.Right is not None:
            out.append(str(self.Right))

        out.append(")")

        return "".join(out)


@dataclass
class InfixExpression(Expression):
    Token: Token.Token  # Operator token (+, -, *, etc.)
    Left: Expression
    Operator: str
    Right: Expression | None = None

    def expression_node(self):
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        out = []

        out.append("(")
        out.append(str(self.Left))
        out.append(f" {self.Operator} ")

        if self.Right is not None:
            out.append(str(self.Right))

        out.append(")")

        return "".join(out)


@dataclass
class Boolean(Expression):
    Token: Token.Token
    Value: bool

    def expression_node():
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        return str(self.Token.Literal)


@dataclass
class BlockStatement(Statement):
    Token: Token.Token  # Anjiriria token
    Statements: list[Statement] = field(default_factory=list)

    def statement_node(self):
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        return "".join(str(stmt) for stmt in self.Statements)


@dataclass
class AkorwoExpression(Expression):
    Token: Token.Token  # Akorwo token
    Condition: Expression | None = None
    Consequence: BlockStatement | None = None
    Alternative: BlockStatement | None = None

    def expression_node(self):
        pass

    def token_literal(self):
        return self.Token.Literal

    def __str__(self):
        out = []

        out.append("Akorwo")
        out.append(str(self.Condition))
        out.append(" ")
        out.append(str(self.Consequence))

        if self.Alternative is not None:
            out.append(" Tiguo ")
            out.append(str(self.Alternative))

        return "".join(out)


@dataclass
class FunctionLiteral(Expression):
    Token: Token.Token  # 'fn' token
    Parameters: list[Identifier] = field(default_factory=list)
    Body: BlockStatement | None = None

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.Token.Literal

    def __str__(self) -> str:
        params = ", ".join(str(param) for param in self.Parameters)

        out = []
        out.append(self.token_literal())  # fn
        out.append("(")
        out.append(params)
        out.append(") ")

        if self.Body is not None:
            out.append(str(self.Body))

        return "".join(out)


@dataclass
class CallExpression(Expression):
    Token: Token.Token  # '(' token
    Function: Expression | None = None
    Arguments: list[Expression] = field(default_factory=list)

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.Token.Literal

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.Arguments)
        return f"{self.Function}({args})"


# noh
