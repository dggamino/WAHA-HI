"""YAML utility functions."""
from pathlib import Path
def load_yaml(filepath):
    content = filepath.read_text(encoding="utf-8")
    return _parse_yaml(content)
def dump_yaml(data, filepath):
    yaml_text = _serialize_yaml(data)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(yaml_text, encoding="utf-8")
def _parse_yaml(content):
    lines = content.split("\n")
    result = {}
    current_dict = result
    stack = []
    current_list = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line or line.startswith("#"): continue
        indent = len(raw_line) - len(raw_line.lstrip())
        stripped = line.lstrip()
        if stripped.startswith("- "):
            value_str = stripped[2:].strip()
            value = _parse_value(value_str)
            if current_list is None:
                current_list = []
                if stack:
                    parent_dict, _ = stack[-1]
                    last_key = list(parent_dict.keys())[-1]
                    parent_dict[last_key] = current_list
            current_list.append(value)
            continue
        current_list = None
        while stack and stack[-1][1] >= indent:
            stack.pop()
            current_dict = stack[-1][0] if stack else result
        if ":" not in stripped: continue
        colon_idx = stripped.index(":")
        key = stripped[:colon_idx].strip()
        value_str = stripped[colon_idx+1:].strip()
        if not value_str:
            new_dict = {}
            current_dict[key] = new_dict
            stack.append((current_dict, indent))
n            current_dict = new_dict
        else:
            current_dict[key] = _parse_value(value_str)
    return result
def _parse_value(value_str):
    value_str = value_str.strip()
    if not value_str or value_str.lower() in ("null", "~"): return None
    if value_str.lower() in ("true", "yes", "on"): return True
    if value_str.lower() in ("false", "no", "off"): return False
    try: return int(value_str)
    except ValueError: pass
    try: return float(value_str)
    except ValueError: pass
    if (value_str.startswith('"') and value_str.endswith('"')) or (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str
def _serialize_yaml(data, indent=0):
    spaces = "  " * indent
    if isinstance(data, dict):
        if not data: return "{}"
        lines = []
        for key, value in data.items():
            if isinstance(value, dict) and value:
                lines.append(f"{spaces}{key}:")
                lines.append(_serialize_yaml(value, indent+1))
            elif isinstance(value, list):
                lines.append(f"{spaces}{key}:")
                for item in value: lines.append(f"{spaces}- {_serialize_inline(item)}")
            else:
                lines.append(f"{spaces}{key}: {_serialize_inline(value)}")
        return "\n".join(lines)
    return _serialize_inline(data)
def _serialize_inline(value):
    if value is None: return "null"
    if isinstance(value, bool): return "true" if value else "false"
    if isinstance(value, (int, float)): return str(value)
    if isinstance(value, str):
        if any(c in value for c in [":", "#", "\n", '"', "'"]):
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'
        return value
    return str(value)
