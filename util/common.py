import inflection


def to_snake_case(str):
    return str.replace(' ', '_')


def camel_to_snake_case(str):
    return inflection.underscore(str)
