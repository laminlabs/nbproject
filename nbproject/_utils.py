def public_fields(obj):
    vars_props_dict = {}
    for key in dir(obj):
        if key[0] != "_":
            value = getattr(obj, key)
            if not callable(value):
                vars_props_dict[key] = value
    return vars_props_dict
