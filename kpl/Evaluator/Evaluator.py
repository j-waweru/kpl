import kpl.Object.Object as Object
import kpl.Ast.Ast as Ast
import kpl.Evaluator.Builtins as Builtins

MA = Object.Boolean(True)
MAHENI = Object.Boolean(False)
GUTIRI = Object.Gutiri()


def evals(node, env):

    def eval_program(stmts):

        result = Object.Object()

        for statement in stmts:
            result = evals(statement, env)

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
                # Always returns false
                return MAHENI
            case "!=":
                return native_bool_to_boolean(left_val != right_val)

            case _:
                return new_error(
                    f"Dioi Operator: {left.Type()} {operator} {right.Type()}"
                )

    def eval_string_infix_expression(operator, left, right):
        left_val = left.Value
        right_val = right.Value

        match operator:
            case "+":
                return Object.String(Value=left_val + right_val)

            case "-":
                left_unique = "".join(ch for ch in left_val if ch not in right_val)

                right_unique = "".join(ch for ch in right_val if ch not in left_val)

                return Object.String(Value=left_unique + right_unique)

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

        elif left.Type() == Object.STRING_OBJ and right.Type() == Object.STRING_OBJ:
            return eval_string_infix_expression(operator, left, right)

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

        condition = evals(node.Condition, env)

        if is_error(condition):
            return condition
        if is_truthy(condition):
            return evals(node.Consequence, env)

        elif node.Alternative is not None:
            return evals(node.Alternative, env)

        else:
            return GUTIRI

    def eval_block_statement(block):
        result = None

        for statement in block.Statements:
            result = evals(statement, env)

            if result is not None:
                if (
                    result.Type() == Object.CHOKIA_VALUE_OBJ
                    or result.Type() == Object.ERROR_OBJ
                ):
                    return result
            return result

    def new_error(a):
        return Object.Error(Message=a)

    def is_error(obj: Object.Object) -> bool:
        if obj is not None:
            return obj.Type() == Object.ERROR_OBJ
        else:
            return False

    def eval_identifier(node, env):
        val = env.get(node.Value)

        if val is not None:
            return val

        builtin = Builtins.builtins.get(node.Value)

        if builtin is not None:
            return builtin

        return new_error(f"Identifier dinonwo: {node.Value}")

    def eval_expressions(exps, env):
        result = []

        for exp in exps:
            evaluated = evals(exp, env)

            if is_error(evaluated):
                return [evaluated]

            result.append(evaluated)

        return result

    def extend_function_env(fn, args):
        env = Object.new_enclosed_environment(fn.Env)

        for param, arg in zip(fn.Parameters, args):
            env.set(param.Value, arg)

        return env

    def unwrap_return_value(obj):
        if isinstance(obj, Object.ChokiaValue):
            return obj.Value

        return obj

    def apply_function(fn, args):

        if isinstance(fn, Object.Function):
            extended_env = extend_function_env(fn, args)
            evaluated = evals(fn.Body, extended_env)
            return unwrap_return_value(evaluated)

        elif isinstance(fn, Object.Builtin):
            return fn.Fn(*args)

        return new_error(f"Not a function: {fn.Type()}")

    def eval_array_index_expression(array, index):
        array_object = array
        idx = index.Value

        max_index = len(array_object.Elements) - 1

        if idx < 0 or idx > max_index:
            return GUTIRI

        return array_object.Elements[idx]

    def eval_hash_index_expression(hash_obj, index):

        if not hasattr(index, "hash_key"):
            return new_error(f"unusable as hash key: {index.Type()}")

        pair = hash_obj.Pairs.get(index.hash_key())

        if pair is None:
            return GUTIRI

        return pair.Value

    def eval_index_expression(left, index):
        if left.Type() == Object.ARRAY_OBJ and index.Type() == Object.INTEGER_OBJ:
            return eval_array_index_expression(left, index)
        elif left.Type() == Object.HASH_OBJ:
            return eval_hash_index_expression(left, index)
        return new_error(f"index operator not supported: {left.Type()}")

    def eval_hash_literal(node):

        pairs = {}

        for key_node, value_node in node.Pairs:
            key = evals(key_node, env)

            if is_error(key):
                return key

            if not hasattr(key, "hash_key"):
                return new_error(f"unusable as hash key: {key.Type()}")

            value = evals(value_node, env)

            if is_error(value):
                return value

            hashed = key.hash_key()

            pairs[hashed] = Object.HashPair(
                Key=key,
                Value=value,
            )

        return Object.Hash(Pairs=pairs)

    if isinstance(node, Ast.Program):
        return eval_program(node.statements)

    elif isinstance(node, Ast.BlockStatement):
        return eval_block_statement(node)

    elif isinstance(node, Ast.AkorwoExpression):
        return eval_akorwo_expression(node)

    elif isinstance(node, Ast.ExpressionStatement):
        return evals(node.Expression, env)

    elif isinstance(node, Ast.IntegerLiteral):
        return Object.Integer(node.Value)

    elif isinstance(node, Ast.Boolean):
        return native_bool_to_boolean(node.Value)

    elif isinstance(node, Ast.PrefixExpression):
        right = evals(node.Right, env)

        if is_error(right):
            return right

        return eval_prefix_expression(node.Operator, right)

    elif isinstance(node, Ast.InfixExpression):
        left = evals(node.Left, env)

        if is_error(left):
            return left
        right = evals(node.Right, env)

        if is_error(right):
            return right

        return eval_infix_expression(node.Operator, left, right)

    elif isinstance(node, Ast.ChokiaStatement):
        val = evals(node.ReturnValue, env)
        return Object.ChokiaValue(Value=val)

    elif isinstance(node, Ast.RekaStatement):
        val = evals(node.Value, env)
        if is_error(val):
            return val
        env.set(node.Name.Value, val)

    elif isinstance(node, Ast.Identifier):
        return eval_identifier(node, env)

    elif isinstance(node, Ast.FunctionLiteral):
        params = node.Parameters
        body = node.Body
        return Object.Function(Parameters=params, Env=env, Body=body)

    elif isinstance(node, Ast.CallExpression):
        function = evals(node.Function, env)

        if is_error(function):
            return function

        args = eval_expressions(node.Arguments, env)

        if len(args) == 1 and is_error(args[0]):
            return args[0]

        return apply_function(function, args)

    elif isinstance(node, Ast.StringLiteral):
        return Object.String(Value=node.Value)

    elif isinstance(node, Ast.ArrayLiteral):
        elements = eval_expressions(node.Elements, env)

        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]

        return Object.Array(Elements=elements)
    elif isinstance(node, Ast.IndexExpression):
        left = evals(node.Left, env)

        if is_error(left):
            return left
        index = evals(node.Index, env)

        if is_error(index):
            return index
        return eval_index_expression(left, index)

    elif isinstance(node, Ast.HashLiteral):
        return eval_hash_literal(node)
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
