def has_all_required_fields(data, fields):
    for field in fields:
        if not data.get(field):
            return False, field

    return True, None
