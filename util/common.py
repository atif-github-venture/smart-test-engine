import inflection


def to_snake_case(str):
    return str.replace(' ', '_')

def to_hypen_lowercase(str):
    return str.lower().replace(' ', '-')

def camel_to_snake_case(str):
    return inflection.underscore(str)
