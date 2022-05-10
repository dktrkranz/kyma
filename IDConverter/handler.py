from re import match, sub


def main(event, context):
    user = event['extensions']['request'].query.user.upper()
    name = event['extensions']['request'].query.name.upper()
    surname = event['extensions']['request'].query.surname.upper()
    if user and name and surname:
        if match('^[A-Z]{2}[A-Z_][A-Z]{2}[A-Z_][0-9ASX][0-9]$', user):
            return user
        else:
            if len(surname.split()) > 1:
                surname = ' '.join([x for x in surname.split() if len(x) > 3]
                                   or surname.split()[-1:])
            name, surname = (sub('[^A-Z0-9]', '', n) for n in (name, surname))
            return f'{surname[:3].ljust(3, "_")}{name[:3].ljust(3, "_")}90'
    else:
        return 'ERROR'
