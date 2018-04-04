def show_content(obj, name='root', **kwargs):
    """
    print out a json as a tree

    :param obj: the json object
    :param name: the name of the json object
    :param kwargs:
        padding_child_birth=" ├─ ", 
        padding_child_alive=" │  " ,
        padding_last_child_birth=" └─ ",
        padding_last_child_alive="    "
    :return:
    """
    _kwargs = {'padding': '',
               'padding_tail': '',
               'padding_following': '',
               'padding_child_birth': " ├─ ",
               'padding_child_alive': " │  ",
               'padding_last_child_birth': " └─ ",
               'padding_last_child_alive': "    "}
    _kwargs.update(kwargs)
    if isinstance(obj, (list, dict)):
        print("{}{}{}".format(_kwargs['padding'], _kwargs['padding_tail'], name))
        _kwargs['padding'] = _kwargs['padding'] + _kwargs['padding_following']
        for i, item in enumerate(obj):
            item, item_name = (item, "[{}]".format(i)) if isinstance(obj, list) else (obj[item], item)
            if i < len(obj) - 1:
                _kwargs['padding_tail'] = _kwargs['padding_child_birth']
                _kwargs['padding_following'] = _kwargs['padding_child_alive']
            else:
                _kwargs['padding_tail'] = _kwargs['padding_last_child_birth']
                _kwargs['padding_following'] = _kwargs['padding_last_child_alive']
            show_content(item, item_name, **_kwargs)
    else:
        print("{}{}{}: {}".format(_kwargs['padding'], _kwargs['padding_tail'], name, obj))
