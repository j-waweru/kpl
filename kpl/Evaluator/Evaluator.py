import kpl.Object.Object as Object
import kpl.Ast.Ast as Ast


MA = Object.Boolean(True)
MAHENI = Object.Boolean(False)
GUTIRI = Object.Gutiri()


def evals(node):

    def eval_program(stmts):

        result = Object.Object()

        for statement in stmts:
            result = evals(statement)

            if isinstance(result, Object.ChokiaValue):
                return result.Value
            if isinstance(result, Object.Error):
                return result

        return result

    def native_bool_to_boolean(item):
        if item:
            return MA
        else:
            return MAHENI

    def eval_bang_operator_expression(right):
        if right == MA:
            return MAHENI
        elif right == MAHENI or right == GUTIRI:
            return MA
        else:
            return MAHENI

    def eval_minus_prefix_operator_expression(right):

        if right.Type() != Object.INTEGER_OBJ:
            return new_error(f"Dioi Operator: -{right.Type()}")
        value = right.Value

        return Object.Integer(Value=-value)

    def eval_prefix_expression(operator, right):
        match operator:
            case "!":
                return eval_bang_operator_expression(right)
            case "-":
                return eval_minus_prefix_operator_expression(right)
            case _:
                return new_error(f"Dioi Operator: {operator} {right.Type()}")

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
                return native_bool_to_boolean(type(left_val) == type(right_val))
            case "===":
                return native_bool_to_boolean(left_val == right_val)
            case "====":
                return native_bool_to_boolean(left_val is right_val)
            case "=====":
                return MAHENI
            case "!=":
                return native_bool_to_boolean(left_val != right_val)

            case _:
                return new_error(
                    f"Dioi Operator: {left.Type()} {operator} {right.Type()}"
                )

    def eval_infix_expression(operator, left, right):

        if left.Type() == Object.INTEGER_OBJ and right.Type() == Object.INTEGER_OBJ:
            return eval_integer_infinix_expression(operator, left, right)

        elif operator == "==":
            return native_bool_to_boolean(left == right)

        elif operator == "!=":
            return native_bool_to_boolean(left != right)
        elif left.Type() != right.Type():
            return new_error(
                f"Mithemba ndihainaine: {left.Type()} {operator} {right.Type()}"
            )

        else:
            return new_error(f"Dioi Operator: {left.Type()} {operator} {right.Type()}")

    def is_truthy(obj) -> bool:

        if obj == GUTIRI or obj == MAHENI:
            return False

        elif obj == MA:
            return True

        else:
            return True

    def eval_akorwo_expression(node: Ast.AkorwoExpression):

        condition = evals(node.Condition)

        if is_error(condition):
            return condition

        if is_truthy(condition):
            return evals(node.Consequence)

        elif node.Alternative is not None:
            return evals(node.Alternative)

        else:
            return GUTIRI

    def eval_block_statement(block: Ast.BlockStatement):
        result = Object.Object()

        for statement in block.Statements:
            result = evals(statement)

            if result is not None:
                rt = result.Type() == Object.CHOKIA_VALUE_OBJ
                if rt == Object.CHOKIA_VALUE_OBJ or rt == Object.ERROR_OBJ:
                    return result
                return result

            return result

    def new_error(a):
        return Object.Error(Message=a)

    def is_error(obj: Object.Object) -> bool:
        if obj is not None:
            return obj.Type() == Object.ERROR_OBJ
        else:
            return False

    if isinstance(node, Ast.Program):
        return eval_program(node.statements)

    elif isinstance(node, Ast.BlockStatement):
        return eval_block_statement(node)

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

        if is_error(right):
            return right

        return eval_prefix_expression(node.Operator, right)

    elif isinstance(node, Ast.InfixExpression):
        left = evals(node.Left)

        if is_error(left):
            return left
        right = evals(node.Right)

        if is_error(right):
            return right

        return eval_infix_expression(node.Operator, left, right)

    elif isinstance(node, Ast.ChokiaStatement):
        val = evals(node.ReturnValue)
        return Object.ChokiaValue(Value=val)

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
