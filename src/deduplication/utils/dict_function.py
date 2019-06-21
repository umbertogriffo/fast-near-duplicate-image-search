def find_keys_with_duplicate_values(ini_dict, value_to_key_function):
    """Finding duplicate values from dictionary using flip.

    Parameters
    ----------
    ini_dict: dict
        A dict.
    value_to_key_function : function
        A function that transforms the value into a hashable type.
        For example if I have a list of int as value, I can transform the value in a int as follow:
            lambda x: int("".join([str(i) for i in x])

    Returns
    -------
    dict
        a flipped dictionary with values as key.
    """

    #
    flipped = {}

    for key, value in ini_dict.items():
        value = value_to_key_function(value)
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)

    return flipped
