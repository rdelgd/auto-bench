"""The pure interpreter for the JSON Schema subset used by the checked-in schemas.

Shared by the version 1 interchange decoder and the ledger event-data validator so each
checks the same definitions it renders, without a runtime dependency on ``jsonschema``.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from typing import Any

from .domain import ValidationFinding

JsonSchema = dict[str, Any]

MAX_SAFE_INTEGER = 9007199254740991

_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def finding(code: str, path: str, message: str) -> ValidationFinding:
    return {"code": code, "severity": "error", "path": path, "message": message}


def child(path: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{path}[{key}]"
    return f"{path}.{key}" if _IDENTIFIER.match(key) else f"{path}[{json.dumps(key, ensure_ascii=False)}]"


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_integer_valued(value: int | float) -> bool:
    return isinstance(value, int) or (math.isfinite(value) and value.is_integer())


def json_equal(left: object, right: object) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if _is_number(left) and _is_number(right):
        return left == right
    return type(left) is type(right) and left == right


def _type_matches(expected: str, value: object) -> bool:
    if expected == "object":
        return isinstance(value, Mapping)
    if expected == "array":
        return isinstance(value, (list, tuple))
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "number":
        return _is_number(value)
    if expected == "integer":
        return _is_number(value) and _is_integer_valued(value)  # type: ignore[arg-type]
    raise ValueError(f"unsupported schema type: {expected}")


def describe(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if _is_number(value):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (list, tuple)):
        return "array"
    if isinstance(value, Mapping):
        return "object"
    return type(value).__name__


def numeric_findings(value: object, path: str, findings: list[ValidationFinding]) -> None:
    """Report non-finite numbers and unsafe integer-valued numbers anywhere in a value."""
    if _is_number(value):
        number: int | float = value  # type: ignore[assignment]
        if isinstance(number, float) and not math.isfinite(number):
            findings.append(finding("format.non_finite_number", path, "Numbers must be finite."))
        elif _is_integer_valued(number) and abs(number) > MAX_SAFE_INTEGER:
            findings.append(finding(
                "format.unsafe_integer",
                path,
                f"Integer-valued numbers must be between -{MAX_SAFE_INTEGER} and {MAX_SAFE_INTEGER}.",
            ))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            numeric_findings(item, child(path, index), findings)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            numeric_findings(item, child(path, str(key)), findings)


def _resolve(schema: JsonSchema, definitions: Mapping[str, JsonSchema]) -> JsonSchema:
    while "$ref" in schema:
        schema = definitions[schema["$ref"].removeprefix("#/$defs/")]
    return schema


def _matches(schema: JsonSchema, value: object, definitions: Mapping[str, JsonSchema]) -> bool:
    probe: list[ValidationFinding] = []
    check(schema, value, "$", probe, definitions)
    return not probe


def check(
    schema: JsonSchema,
    value: object,
    path: str,
    findings: list[ValidationFinding],
    definitions: Mapping[str, JsonSchema],
) -> None:
    """Interpret the schema subset, resolving ``#/$defs/`` references against ``definitions``."""
    if "$ref" in schema:
        check(_resolve(schema, definitions), value, path, findings, definitions)
        return
    if "anyOf" in schema:
        options: list[JsonSchema] = [_resolve(option, definitions) for option in schema["anyOf"]]
        if not any(_matches(option, value, definitions) for option in options):
            # Report through the option for this value's JSON type so nested findings stay addressed.
            typed = [option for option in options if "type" in option and _type_matches(option["type"], value)]
            if typed:
                check(typed[0], value, path, findings, definitions)
            else:
                findings.append(finding("format.invalid_value", path, f"Unsupported JSON value of type {describe(value)}."))
        return
    if "const" in schema and not json_equal(value, schema["const"]):
        findings.append(finding("format.invalid_value", path, f"Expected {json.dumps(schema['const'])}."))
        return
    if "enum" in schema and not any(json_equal(value, option) for option in schema["enum"]):
        findings.append(finding("format.invalid_value", path, f"Unsupported value; expected one of: {', '.join(schema['enum'])}."))
        return
    if "type" in schema and not _type_matches(schema["type"], value):
        findings.append(finding("format.invalid_type", path, f"Expected {schema['type']} but found {describe(value)}."))
        return
    if "if" in schema:
        branch = "then" if _matches(schema["if"], value, definitions) else "else"
        if branch in schema:
            check(schema[branch], value, path, findings, definitions)
    if "not" in schema and _matches(schema["not"], value, definitions):
        findings.append(finding("format.invalid_value", path, "Value matches a disallowed shape."))
    if _is_number(value):
        number: int | float = value  # type: ignore[assignment]
        if ("minimum" in schema and number < schema["minimum"]) or ("maximum" in schema and number > schema["maximum"]):
            findings.append(finding("format.invalid_value", path, "Number is outside the supported range."))
    if isinstance(value, (list, tuple)) and "items" in schema:
        for index, item in enumerate(value):
            check(schema["items"], item, child(path, index), findings, definitions)
    if isinstance(value, Mapping):
        properties: dict[str, JsonSchema] = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                findings.append(finding("format.missing_property", child(path, key), f"Missing required property: {key}"))
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if not isinstance(key, str):
                findings.append(finding("format.invalid_type", path, "Object keys must be strings."))
            elif key in properties:
                check(properties[key], item, child(path, key), findings, definitions)
            elif additional is False:
                findings.append(finding("format.unknown_property", child(path, key), f"Unknown property: {key}"))
            elif isinstance(additional, dict):
                check(additional, item, child(path, key), findings, definitions)


def shape_findings(schema: JsonSchema, value: object, path: str, definitions: Mapping[str, JsonSchema]) -> list[ValidationFinding]:
    """Numeric findings first, then shape findings at paths the numeric check did not already address."""
    numeric: list[ValidationFinding] = []
    numeric_findings(value, path, numeric)
    shape: list[ValidationFinding] = []
    check(schema, value, path, shape, definitions)
    numeric_paths = {item["path"] for item in numeric}
    return [*numeric, *(item for item in shape if item["path"] not in numeric_paths)]
