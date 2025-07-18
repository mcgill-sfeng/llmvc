import ast
import inspect
from typing import get_type_hints
from collections import defaultdict


class Analyzer(ast.NodeVisitor):
    def __init__(self, env):
        self.errors = defaultdict(set)
        self.variable_types = {}

        self.env = env

        super().__init__()

    def visit_Assign(self, node: ast.Assign):
        value_type = self.infer_type(node.value)

        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variable_types[target.id] = value_type

        for call_node in ast.walk(node.value):
            if isinstance(call_node, ast.Call):
                self.check_call(call_node, node.targets, node.lineno)

        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        for call_node in ast.walk(node.value):
            if isinstance(call_node, ast.Call):
                self.check_call(call_node, None, node.lineno)
        self.generic_visit(node)

    def check_call(self, node: ast.Call, targets: list[ast.expr] | None, lineno: int):
        func_obj = self.resolve_callable(node.func)

        if func_obj is None:
            name = self.get_readable_func_name(node.func)
            self.errors[lineno].add(f"Unresolved reference '{name}'")
            return

        if not (inspect.isfunction(func_obj) or inspect.ismethod(func_obj)):
            return

        try:
            sig = inspect.signature(func_obj)
            hints = get_type_hints(func_obj)
        except (TypeError, ValueError):
            name = self.get_readable_func_name(node.func)
            self.errors[lineno].add(f"Unable to retrieve signature of '{name}'")
            return

        actual_args = node.args
        expected_params = list(sig.parameters.values())

        if inspect.ismethod(func_obj) or (inspect.isfunction(func_obj) and isinstance(node.func, ast.Attribute)):
            if expected_params and expected_params[0].name == 'self':
                expected_params = expected_params[1:]

        if len(actual_args) < len(expected_params):
            for param in expected_params[len(actual_args):]:
                if param.default is inspect.Parameter.empty and param.kind not in (
                        inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                    self.errors[lineno].add(f"Parameter '{param.name}' unfilled")
        elif len(actual_args) > len(expected_params):
            self.errors[lineno].add(f"{len(actual_args) - len(expected_params)} unexpected argument(s)")

        for param, arg in zip(expected_params, actual_args):
            expected = hints.get(param.name)
            actual = self.infer_type(arg)
            if expected and actual and not Analyzer.match_types(expected, actual):
                self.errors[lineno].add(f"Expected type '{expected.__name__}', got '{actual.__name__}' instead")

        if hints.get('return') and targets:
            for target in targets:
                if isinstance(target, ast.Name):
                    self.variable_types[target.id] = hints['return']

    def resolve_callable(self, node: ast.expr) -> object | None:
        if isinstance(node, ast.Name):
            return self.env.get(node.id)

        elif isinstance(node, ast.Attribute):
            base_type = self.infer_type(node.value)
            if base_type:
                try:
                    return getattr(base_type, node.attr)
                except AttributeError:
                    return None

        return None

    def get_readable_func_name(self, node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_readable_func_name(node.value)}.{node.attr}"
        return "<unknown>"

    def infer_type(self, node: ast.expr):
        if isinstance(node, ast.Constant):
            return type(node.value)
        elif isinstance(node, ast.Name):
            return self.variable_types.get(node.id)
        elif isinstance(node, ast.Call):
            func_obj = self.resolve_callable(node.func)
            if func_obj:
                try:
                    return_type = get_type_hints(func_obj).get('return')
                    if return_type:
                        return return_type
                    elif inspect.isclass(func_obj):  # e.g., Dummy()
                        return func_obj
                except Exception:
                    return None
        elif isinstance(node, ast.Attribute):
            base_type = self.infer_type(node.value)
            if base_type:
                try:
                    attr = getattr(base_type, node.attr, None)
                    if callable(attr):
                        return get_type_hints(attr).get('return')
                except Exception:
                    return None
        return None

    @staticmethod
    def match_types(expected: type, actual: type) -> bool:
        try:
            return issubclass(actual, expected)
        except TypeError:
            return expected == actual


def annotate_lines(source_code, errors):
    lines = source_code.splitlines()
    return "\n".join(
        f"{line}{'  <- ' + ',  '.join(sorted(errors[i + 1])) if (i + 1) in errors else ''}"
        for i, line in enumerate(lines)
    )


def inspect_code(func_string: str, env):
    if env is None:
        raise ValueError("You must provide an environment (e.g., env=globals())")

    try:
        tree = ast.parse(func_string)
    except SyntaxError as e:
        return annotate_lines(func_string, {e.lineno: {f"SyntaxError: {e.msg}"}})

    analyzer = Analyzer(env)

    analyzer.visit(tree)
    return annotate_lines(func_string, analyzer.errors)

