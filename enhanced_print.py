# -*- coding: utf-8 -*-
import sys
import six


if six.PY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    STRING_TYPE = (str, unicode)
else:
    STRING_TYPE = str


def tree(obj, name='root', **kwargs):
    """
    print out an object as a tree

    :param obj: the object
    :param name: the name of the object
    :param kwargs:
        symbol_child_birth=" ├─ ",
        symbol_child_alive=" │  " ,
        symbol_last_child_birth=" └─ ",
        symbol_last_child_alive="    ",
        expand_types={},
        no_expand_types={},
        expand=True,
        return_instead=False
    :return:
        unicode (in PY2) or str (in PY3) or None (return_instead=False)
    """
    _kwargs = {'symbol_child_birth': " ├─ ",
               'symbol_child_alive': " │  ",
               'symbol_last_child_birth': " └─ ",
               'symbol_last_child_alive': "    ",
               'expand_types': {},
               'no_expand_types': {},
               'expand': True,
               'return_instead': False,
               'padding_base': '',
               'padding_extra': '',
               'padding_increment': '',
               'padding_end': "\n"}
    _kwargs.update(kwargs)
    at_top_level_of_non_expand_line = False
    if _kwargs['expand']:
        _kwargs['expand'] = hasattr(obj, '__iter__') and not isinstance(obj, STRING_TYPE)
        if _kwargs['expand_types']:
            _kwargs['expand'] = _kwargs['expand'] and isinstance(obj, tuple(_kwargs['expand_types']))
        elif _kwargs['no_expand_types']:
            _kwargs['expand'] = _kwargs['expand'] and not isinstance(obj, tuple(_kwargs['no_expand_types']))
        if not _kwargs['expand']:
            at_top_level_of_non_expand_line = True
    result = u''
    head = u'{}{}{}'.format(_kwargs['padding_base'], _kwargs['padding_extra'], name)
    if _kwargs['return_instead']:
        result += head
    else:
        six.print_(head, end='')
    if _kwargs['expand']:
        neck = u'\n'
        if _kwargs['return_instead']:
            result += neck
        else:
            six.print_(neck, end='')
        _kwargs['padding_base'] = _kwargs['padding_base'] + _kwargs['padding_increment']
        for i, item in enumerate(obj):
            if isinstance(obj, dict):
                item, item_name = obj[item], item
            else:
                item_name = "[{}]".format(i) if isinstance(obj, list) \
                    else "({})".format(i) if isinstance(obj, tuple) \
                    else "<{}>".format(i)
            if i < len(obj) - 1:
                _kwargs['padding_extra'] = _kwargs['symbol_child_birth']
                _kwargs['padding_increment'] = _kwargs['symbol_child_alive']
            else:
                _kwargs['padding_extra'] = _kwargs['symbol_last_child_birth']
                _kwargs['padding_increment'] = _kwargs['symbol_last_child_alive']
            if _kwargs['return_instead']:
                result += show_content(item, item_name, **_kwargs)
            else:
                show_content(item, item_name, **_kwargs)
    else:
        neck = u': ' if name else u''
        if _kwargs['return_instead']:
            result += neck
        else:
            six.print_(neck, end='')
        if hasattr(obj, '__iter__') and not isinstance(obj, STRING_TYPE):
            body_start = u'{' if isinstance(obj, (dict, set)) \
                else u'[' if isinstance(obj, list) \
                else u'(' if isinstance(obj, tuple) \
                else u'<'
            if _kwargs['return_instead']:
                result += body_start
            else:
                six.print_(body_start, end='')
            _kwargs['padding_base'] = ""
            _kwargs['padding_extra'] = ""
            _kwargs['padding_increment'] = ""
            _kwargs['padding_end'] = ""
            for i, item in enumerate(obj):
                if isinstance(obj, dict):
                    item, item_name = obj[item], item
                else:
                    item_name = ""
                if _kwargs['return_instead']:
                    result += show_content(item, item_name, **_kwargs)
                else:
                    show_content(item, item_name, **_kwargs)
                if i < len(obj) - 1:
                    sep = ', '
                else:
                    sep = ''
                if _kwargs['return_instead']:
                    result += sep
                else:
                    six.print_(sep, end='')
            body_end = u'}' if isinstance(obj, (dict, set)) \
                else u']' if isinstance(obj, list) \
                else u')' if isinstance(obj, tuple) \
                else u'>'
            body_end += "\n" if at_top_level_of_non_expand_line else ""
            if _kwargs['return_instead']:
                result += body_end
            else:
                six.print_(body_end, end='')
        else:
            body = (obj if isinstance(obj, STRING_TYPE) else repr(obj)) + _kwargs['padding_end']
            if _kwargs['return_instead']:
                result += body
            else:
                six.print_(body, end='')
    if _kwargs['return_instead']:
        return result
