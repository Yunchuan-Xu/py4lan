from collections import Iterable


def list2dict(l, key='id', *, func=None, value=None):
    if l is None:
        return None
    elif callable(func):
        return {o[key]: func(o) for o in l}
    elif value is None:
        return {o[key]: o for o in l}
    elif isinstance(value, dict):
        return {o[key]: {new_v: o[old_v] for old_v, new_v in value.items()} for o in l}
    elif isinstance(value, Iterable) and not isinstance(value, str):
        return {o[key]: {v: o[v] for v in value} for o in l}
    else:
        return {o[key]: o[value] for o in l}
