from dataclasses import fields


def dataclass_from_dict(klass, dikt):
    try:
        field_types = {f.name: f.type for f in fields(klass)}
        return klass(**{f: dataclass_from_dict(field_types[f], dikt[f]) for f in dikt})
    except (AttributeError, TypeError):
        if isinstance(dikt, (tuple, list)):
            return [dataclass_from_dict(klass.__args__[0], f) for f in dikt]
        return dikt
