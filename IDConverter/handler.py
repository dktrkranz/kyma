from re import match


def main(event, context):
    user = event['extensions']['request'].query.user.upper()
    name = event['extensions']['request'].query.name.upper()
    surname = event['extensions']['request'].query.surname.upper()
    if user and name and surname:
        if match('^[A-Z]{2}[A-Z_][A-Z]{2}[A-Z_][0-9ASX][0-9]$', user):
            return user
        else:
            return f'{surname[:3].ljust(3, "_")}{name[:3].ljust(3, "_")}90'
    else:
        return 'ERROR'
