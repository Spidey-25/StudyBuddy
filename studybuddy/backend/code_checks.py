"""Safe, deterministic checks for the constrained code-edit exercises.

These checks recognize a small set of authored answer patterns and evaluate
them against fixed fixtures. They never compile or execute submitted source.
"""
from __future__ import annotations

import ast
import math
import operator
import re


_SUITES = {
    "cpp-debugger": ("sum-return", "loop-bound", "loop-bound", "pointer-address", "loop-bound", "sum-return"),
    "java-debugger": ("positive-boundary", "accumulate", "string-equality", "floating-division", "positive-boundary", "accumulate"),
    "python-debug": ("contains", "empty-average", "contains", "last-index", "last-index", "contains"),
    "web-playground": ("dom-selector", "flex-center", "prevent-submit", "focus-outline", "dom-selector", "flex-center"),
    "c-debugger": ("max-return", "string-buffer", "array-bound", "static-lifetime", "max-return", "array-bound"),
}

_FIXTURES = {
    "sum-return": ({"a": 2, "b": 3, "expected": 5}, {"a": -1, "b": 1, "expected": 0}, {"a": 0, "b": 0, "expected": 0}),
    "loop-bound": ({"size": 0}, {"size": 1}, {"size": 4}),
    "pointer-address": ({"value": 12, "expected": 12},),
    "positive-boundary": ({"n": 1, "expected": True}, {"n": 0, "expected": False}, {"n": -1, "expected": False}),
    "accumulate": ({"values": [1, 2, 3], "expected": 6}, {"values": [], "expected": 0}),
    "string-equality": ({"left": "study", "right": "study", "same_object": False, "expected": True}, {"left": "study", "right": "buddy", "same_object": False, "expected": False}),
    "floating-division": ({"total": 5, "count": 2, "expected": 2.5}, {"total": 6, "count": 3, "expected": 2.0}),
    "contains": ({"items": [1, 2], "target": 2, "expected": True}, {"items": [], "target": 2, "expected": False}, {"items": [1, 2], "target": 9, "expected": False}),
    "empty-average": ({"values": [], "expected": 0}, {"values": [2, 4], "expected": 3}),
    "last-index": ({"items": [4, 8], "expected": 8}, {"items": [3], "expected": 3}),
    "dom-selector": ({"selector": "#save", "ids": {"save", "cancel"}, "expected": "save"}, {"selector": "#save", "ids": {"save"}, "expected": "save"}),
    "flex-center": ({"display": "flex", "justify_content": "center", "expected": True},),
    "prevent-submit": ({"event": "submit", "prevent_default": True, "expected": True},),
    "focus-outline": ({"width_px": 3, "style": "solid", "color": "currentColor", "expected": True},),
    "max-return": ({"a": 4, "b": 2, "expected": 4}, {"a": -1, "b": 0, "expected": 0}, {"a": 7, "b": 7, "expected": 7}),
    "string-buffer": ({"text": "code", "capacity": 5, "expected": True}, {"text": "code", "capacity": 5, "expected": True}),
    "array-bound": ({"count": 4, "expected_index": 3}, {"count": 1, "expected_index": 0}),
    "static-lifetime": ({"value": 7, "survives_return": True, "expected": 7},),
}


def suite_size(game_id: str, level_index: int) -> int:
    try:
        return len(_FIXTURES[_SUITES[game_id][level_index]])
    except (KeyError, IndexError):
        return 0


def validate_code_edit(game_id: str, level_index: int, candidate: object, reference: str) -> bool:
    """Recognize the submitted line, then check it against private fixtures."""
    if not isinstance(candidate, str):
        return False
    try:
        kind = _SUITES[game_id][level_index]
        fixtures = _FIXTURES[kind]
    except (KeyError, IndexError):
        return False
    # Keep this deliberately constrained: only the authored canonical line (with
    # insignificant whitespace differences) is accepted by these exercises.
    if _normal(candidate) != _normal(reference):
        return False
    return all(_run_fixture(kind, candidate, fixture) for fixture in fixtures)


def _normal(value: str) -> str:
    return re.sub(r"\s+", "", value).rstrip(";")


_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Mod: operator.mod}
_CMPOPS = {ast.Gt: operator.gt, ast.GtE: operator.ge, ast.Lt: operator.lt, ast.LtE: operator.le, ast.Eq: operator.eq, ast.NotEq: operator.ne}


def _eval_expr(expression: str, values: dict) -> object:
    """Evaluate only names, literals, arithmetic, and comparisons from the AST."""
    root = ast.parse(expression.strip().rstrip(";"), mode="eval").body

    def visit(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
            return node.value
        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.IfExp):
            return visit(node.body) if visit(node.test) else visit(node.orelse)
        if isinstance(node, ast.Compare) and len(node.ops) == len(node.comparators) == 1 and type(node.ops[0]) in _CMPOPS:
            return _CMPOPS[type(node.ops[0])](visit(node.left), visit(node.comparators[0]))
        raise ValueError("unsupported expression")

    return visit(root)


def _return_expression(candidate: str) -> str:
    match = re.search(r"\breturn\s+(.+?)\s*;?\s*$", candidate.strip())
    if not match:
        raise ValueError("missing return expression")
    expression = match.group(1).strip()
    # Translate a C-style conditional expression into the safe evaluator's syntax.
    ternary = re.fullmatch(r"(.+?)\?(.+?):(.+)", expression)
    if ternary:
        condition, when_true, when_false = (part.strip() for part in ternary.groups())
        return f"({when_true}) if ({condition}) else ({when_false})"
    return expression


def _run_fixture(kind: str, candidate: str, fixture: dict) -> bool:
    try:
        if kind in {"sum-return", "positive-boundary", "max-return"}:
            result = _eval_expr(_return_expression(candidate), fixture)
            return result == fixture["expected"]
        if kind == "floating-division":
            expression = _return_expression(candidate)
            if "(double)" not in expression.replace(" ", ""):
                return False
            expression = re.sub(r"\(double\)\s*", "", expression)
            result = _eval_expr(expression, {"total": float(fixture["total"]), "count": fixture["count"]})
            return math.isclose(float(result), fixture["expected"])
        if kind == "loop-bound":
            match = re.search(r"\bi\s*(<=|<)\s*(?:[A-Za-z_]\w*\.size\(\)|size)", candidate)
            if not match:
                return False
            size = fixture["size"]
            indexes = list(range(size + (1 if match.group(1) == "<=" else 0)))
            return indexes == list(range(size))
        if kind == "pointer-address":
            match = re.search(r"int\s*\*\s*ptr\s*=\s*&\s*value\s*;?", candidate)
            return bool(match) and fixture["value"] == fixture["expected"]
        if kind == "accumulate":
            code = _normal(candidate)
            if "total+=value" not in code and "total=total+value" not in code:
                return False
            total = 0
            for value in fixture["values"]:
                total += value
            return total == fixture["expected"]
        if kind == "string-equality":
            uses_value_equality = bool(re.search(r"name\.equals\(expected\)", candidate)) or bool(re.search(r"Objects\.equals\(name,\s*expected\)", candidate))
            return uses_value_equality and (fixture["left"] == fixture["right"]) == fixture["expected"]
        if kind == "contains":
            branch_returns_true = _normal(candidate) == "returnTrue"
            found = fixture["target"] in fixture["items"]
            return branch_returns_true and (found if found else False) == fixture["expected"]
        if kind == "empty-average":
            guarded = bool(re.search(r"if\s+not\s+values\s*:\s*return\s+0", candidate))
            values = fixture["values"]
            result = 0 if not values else sum(values) / len(values)
            return guarded and result == fixture["expected"]
        if kind == "last-index":
            uses_last_valid_index = bool(re.search(r"items\s*\[\s*len\(items\)\s*-\s*1\s*\]", candidate))
            result = fixture["items"][-1] if fixture["items"] else None
            return uses_last_valid_index and result == fixture["expected"]
        if kind == "dom-selector":
            match = re.search(r"querySelector\(\s*['\"]#([A-Za-z][\w-]*)['\"]\s*\)", candidate)
            return bool(match) and match.group(0).find("querySelector") >= 0 and match.group(1) in fixture["ids"] and "#" + match.group(1) == fixture["selector"] and match.group(1) == fixture["expected"]
        if kind == "flex-center":
            declarations = {key.strip().lower(): value.strip().lower() for key, value in (part.split(":", 1) for part in candidate.split(";") if ":" in part)}
            return declarations.get("display") == fixture["display"] and declarations.get("justify-content") == fixture["justify_content"] and fixture["expected"] is True
        if kind == "prevent-submit":
            code = re.sub(r"\s+", "", candidate)
            return ("addEventListener('submit'" in code or 'addEventListener("submit"' in code) and "preventDefault()" in code and fixture["event"] == "submit" and fixture["prevent_default"] == fixture["expected"]
        if kind == "focus-outline":
            match = re.search(r"outline\s*:\s*(\d+)px\s+solid\s+currentColor", candidate, re.I)
            return bool(match) and int(match.group(1)) >= 2 and fixture["width_px"] >= 2 and fixture["style"] == "solid" and fixture["color"] == "currentColor" and fixture["expected"]
        if kind == "string-buffer":
            match = re.search(r"char\s+text\s*\[\s*(\d+)\s*\]\s*=\s*\"([^\"]*)\"", candidate)
            capacity = int(match.group(1)) if match else 0
            contents = match.group(2) if match else ""
            return capacity >= len(fixture["text"]) + 1 and contents == fixture["text"] and capacity >= fixture["capacity"] and fixture["expected"]
        if kind == "array-bound":
            match = re.search(r"values\s*\[\s*count\s*-\s*1\s*\]", candidate)
            return bool(match) and fixture["count"] - 1 == fixture["expected_index"] and 0 <= fixture["expected_index"] < fixture["count"]
        if kind == "static-lifetime":
            return bool(re.search(r"static\s+int\s+value\s*=\s*7\s*;", candidate)) and "return&value" in _normal(candidate) and fixture["survives_return"] and fixture["value"] == fixture["expected"]
    except (SyntaxError, TypeError, ValueError, ZeroDivisionError, OverflowError):
        return False
    return False
