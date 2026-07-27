import kpl.Object.Object as Object
import kpl.Ast.Ast as Ast


MA = Object.Boolean(True)
MAHENI = Object.Boolean(False)
GUTIRI = Object.Gutiri()


def evals(node):

    def eval_statements(stmts):

        result = Object.Object()

        for statement in stmts:
            return evals(statement)

        return result

    def native_bool_to_boolean(item):
        if item:
            return MA
        else:
            return MAHENI

    def eval_bang_operator_expression(right):
        if right == MA:
            return MAHENI
        elif right == MAHENI:
            return MA
        elif right == GUTIRI:
            return MA
        else:
            return MAHENI

    def eval_minus_prefix_operator_expression(right):

        if right.Type() != Object.INTEGER_OBJ:
            return GUTIRI
        value = right.Value

        return Object.Integer(Value=-value)

    def eval_prefix_expression(operator, right):
        match operator:
            case "!":
                return eval_bang_operator_expression(right)
            case "-":
                return eval_minus_prefix_operator_expression(right)
            case _:
                return None

    def eval_integer_infinix_expression(operator, left, right):

        left_val = left.Value
        right_val = right.Value

        match operator:
            case "+":
                return Object.Integer(Value=(left_val + right_val))
            case "-":
                return Object.Integer(Value=left_val - right_val)
            case "*":
                return Object.Integer(Value=left_val * right_val)
            case "/":
                return Object.Integer(Value=left_val / right_val)
            case "%":
                return Object.Integer(Value=left_val % right_val)

            case "<":
                return native_bool_to_boolean(left_val < right_val)
            case ">":
                return native_bool_to_boolean(left_val > right_val)
            case "==":
                return native_bool_to_boolean(left_val == right_val)
            case "!=":
                return native_bool_to_boolean(left_val != right_val)

            case _:
                return GUTIRI

    def eval_infix_expression(operator, left, right):

        if operator == "==":
            return native_bool_to_boolean(left == right)

        elif operator == "!=":
            return native_bool_to_boolean(left != right)

        elif left.Type() == Object.INTEGER_OBJ and right.Type() == Object.INTEGER_OBJ:
            return eval_integer_infinix_expression(operator, left, right)

        else:
            return GUTIRI

    def is_truthy(obj) -> bool:

        if obj == GUTIRI:
            return False

        elif obj == MA:
            return True

        elif obj == MAHENI:
            return False

        else:
            return True

    def eval_akorwo_expression(node: Ast.AkorwoExpression):

        condition = evals(node.Condition)

        if is_truthy(condition):
            return evals(node.Consequence)

        elif node.Alternative is not None:
            return evals(node.Alternative)

        else:
            return GUTIRI

    if isinstance(node, Ast.Program):
        return eval_statements(node.statements)

    elif isinstance(node, Ast.BlockStatement):
        return eval_statements(node.Statements)

    elif isinstance(node, Ast.AkorwoExpression):
        return eval_akorwo_expression(node)

    elif isinstance(node, Ast.ExpressionStatement):
        return evals(node.Expression)

    elif isinstance(node, Ast.IntegerLiteral):
        return Object.Integer(node.Value)

    elif isinstance(node, Ast.Boolean):
        return native_bool_to_boolean(node.Value)

    elif isinstance(node, Ast.PrefixExpression):
        right = evals(node.Right)
        return eval_prefix_expression(node.Operator, right)

    elif isinstance(node, Ast.InfixExpression):
        left = evals(node.Left)
        right = evals(node.Right)
        return eval_infix_expression(node.Operator, left, right)

    # match node:
    #     case Ast.Program:
    #         return eval_statements(node.statements)
    #
    #     case Ast.ExpressionStatement:
    #         return evals(node.Expression)
    #
    #     case Ast.IntegerLiteral:
    #         return Object.Integer(Value=node.Value)

    return None
    # return Object.Gutiri()
