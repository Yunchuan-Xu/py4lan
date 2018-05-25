
# py4lan

## enhanced_print.tree
print out an object as a tree  
all iterable objects (except str) will be expanded into multiple lines by default

### construct an object


```python
from enhanced_print import tree
import collections

lang = ['English', '中文', '日本語', 'русский', 'etc.']

py = {'python2', 'python3'}

types = ('dict', '{set}', '[list]', '(tuple)', '<iterable>')

params = collections.OrderedDict()
params['obj'] = ('the object to be printed',)
params['name'] = ('the name of the object', 
                  "default='root'")
params['symbol_child_birth'] = ('the tree symbol where a sub-item is showing its first line', 
                                "default=' ├─ '")
params['symbol_child_alive'] = ('the tree symbol where a sub-item is showing its rest lines', 
                                "default=' │  '")
params['symbol_last_child_birth'] = ('the tree symbol where the last sub-item is showing its first line', 
                                     "default=' └─ '")
params['symbol_last_child_alive'] = ('the tree symbol where the last sub-item is showing its rest lines', 
                                     "default='    '")
params['expand_types'] = ('if not empty, only expand_types objects will be expanded', 
                          'default={}')
params['no_expand_types'] = ('all iterable objects will be expanded except no_expand_types objects', 
                             'only works when expand_types is empty', 
                             'default={}')
params['expand'] = ('if False, print out the object in one line', 
                    'default=True')
params['return_instead'] = ('if True, no printing, but return a string instead', 
                            'default=False')
params['show_type'] = ('if True, object type info will be added at the end of expanding object name', 
                       'default=False')

example = collections.OrderedDict()  # dict
example['languages'] = lang  # list
example['python versions'] = py  # set
example['types'] = types  # tuple
example['xrange(5)'] = xrange(5)  # iterable
example['params'] = params  # dict
example['author'] = '4lan'  # string
```

### example 1: default


```python
tree(example, 'example')
```

    example
     ├─ languages
     │   ├─ [0]: English
     │   ├─ [1]: 中文
     │   ├─ [2]: 日本語
     │   ├─ [3]: русский
     │   └─ [4]: etc.
     ├─ python versions
     │   ├─ {0}: python3
     │   └─ {1}: python2
     ├─ types
     │   ├─ (0): dict
     │   ├─ (1): {set}
     │   ├─ (2): [list]
     │   ├─ (3): (tuple)
     │   └─ (4): <iterable>
     ├─ xrange(5)
     │   ├─ <0>: 0
     │   ├─ <1>: 1
     │   ├─ <2>: 2
     │   ├─ <3>: 3
     │   └─ <4>: 4
     ├─ params
     │   ├─ obj
     │   │   └─ (0): the object to be printed
     │   ├─ name
     │   │   ├─ (0): the name of the object
     │   │   └─ (1): default='root'
     │   ├─ symbol_child_birth
     │   │   ├─ (0): the tree symbol where a sub-item is showing its first line
     │   │   └─ (1): default=' ├─ '
     │   ├─ symbol_child_alive
     │   │   ├─ (0): the tree symbol where a sub-item is showing its rest lines
     │   │   └─ (1): default=' │  '
     │   ├─ symbol_last_child_birth
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its first line
     │   │   └─ (1): default=' └─ '
     │   ├─ symbol_last_child_alive
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its rest lines
     │   │   └─ (1): default='    '
     │   ├─ expand_types
     │   │   ├─ (0): if not empty, only expand_types objects will be expanded
     │   │   └─ (1): default={}
     │   ├─ no_expand_types
     │   │   ├─ (0): all iterable objects will be expanded except no_expand_types objects
     │   │   ├─ (1): only works when expand_types is empty
     │   │   └─ (2): default={}
     │   ├─ expand
     │   │   ├─ (0): if False, print out the object in one line
     │   │   └─ (1): default=True
     │   ├─ return_instead
     │   │   ├─ (0): if True, no printing, but return a string instead
     │   │   └─ (1): default=False
     │   └─ show_type
     │       ├─ (0): if True, object type info will be added at the end of expanding object name
     │       └─ (1): default=False
     └─ author: 4lan
    

### example 2: show type


```python
tree(example, 'example', show_type=True)
```

    example <class 'collections.OrderedDict'>
     ├─ languages <type 'list'>
     │   ├─ [0]: English
     │   ├─ [1]: 中文
     │   ├─ [2]: 日本語
     │   ├─ [3]: русский
     │   └─ [4]: etc.
     ├─ python versions <type 'set'>
     │   ├─ {0}: python3
     │   └─ {1}: python2
     ├─ types <type 'tuple'>
     │   ├─ (0): dict
     │   ├─ (1): {set}
     │   ├─ (2): [list]
     │   ├─ (3): (tuple)
     │   └─ (4): <iterable>
     ├─ xrange(5) <type 'xrange'>
     │   ├─ <0>: 0
     │   ├─ <1>: 1
     │   ├─ <2>: 2
     │   ├─ <3>: 3
     │   └─ <4>: 4
     ├─ params <class 'collections.OrderedDict'>
     │   ├─ obj <type 'tuple'>
     │   │   └─ (0): the object to be printed
     │   ├─ name <type 'tuple'>
     │   │   ├─ (0): the name of the object
     │   │   └─ (1): default='root'
     │   ├─ symbol_child_birth <type 'tuple'>
     │   │   ├─ (0): the tree symbol where a sub-item is showing its first line
     │   │   └─ (1): default=' ├─ '
     │   ├─ symbol_child_alive <type 'tuple'>
     │   │   ├─ (0): the tree symbol where a sub-item is showing its rest lines
     │   │   └─ (1): default=' │  '
     │   ├─ symbol_last_child_birth <type 'tuple'>
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its first line
     │   │   └─ (1): default=' └─ '
     │   ├─ symbol_last_child_alive <type 'tuple'>
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its rest lines
     │   │   └─ (1): default='    '
     │   ├─ expand_types <type 'tuple'>
     │   │   ├─ (0): if not empty, only expand_types objects will be expanded
     │   │   └─ (1): default={}
     │   ├─ no_expand_types <type 'tuple'>
     │   │   ├─ (0): all iterable objects will be expanded except no_expand_types objects
     │   │   ├─ (1): only works when expand_types is empty
     │   │   └─ (2): default={}
     │   ├─ expand <type 'tuple'>
     │   │   ├─ (0): if False, print out the object in one line
     │   │   └─ (1): default=True
     │   ├─ return_instead <type 'tuple'>
     │   │   ├─ (0): if True, no printing, but return a string instead
     │   │   └─ (1): default=False
     │   └─ show_type <type 'tuple'>
     │       ├─ (0): if True, object type info will be added at the end of expanding object name
     │       └─ (1): default=False
     └─ author: 4lan
    

### example 3: specify symbols


```python
tree(example, 'example', symbol_child_birth=' +- ', symbol_child_alive=' |  ', symbol_last_child_birth=' +- ')
```

    example
     +- languages
     |   +- [0]: English
     |   +- [1]: 中文
     |   +- [2]: 日本語
     |   +- [3]: русский
     |   +- [4]: etc.
     +- python versions
     |   +- {0}: python3
     |   +- {1}: python2
     +- types
     |   +- (0): dict
     |   +- (1): {set}
     |   +- (2): [list]
     |   +- (3): (tuple)
     |   +- (4): <iterable>
     +- xrange(5)
     |   +- <0>: 0
     |   +- <1>: 1
     |   +- <2>: 2
     |   +- <3>: 3
     |   +- <4>: 4
     +- params
     |   +- obj
     |   |   +- (0): the object to be printed
     |   +- name
     |   |   +- (0): the name of the object
     |   |   +- (1): default='root'
     |   +- symbol_child_birth
     |   |   +- (0): the tree symbol where a sub-item is showing its first line
     |   |   +- (1): default=' ├─ '
     |   +- symbol_child_alive
     |   |   +- (0): the tree symbol where a sub-item is showing its rest lines
     |   |   +- (1): default=' │  '
     |   +- symbol_last_child_birth
     |   |   +- (0): the tree symbol where the last sub-item is showing its first line
     |   |   +- (1): default=' └─ '
     |   +- symbol_last_child_alive
     |   |   +- (0): the tree symbol where the last sub-item is showing its rest lines
     |   |   +- (1): default='    '
     |   +- expand_types
     |   |   +- (0): if not empty, only expand_types objects will be expanded
     |   |   +- (1): default={}
     |   +- no_expand_types
     |   |   +- (0): all iterable objects will be expanded except no_expand_types objects
     |   |   +- (1): only works when expand_types is empty
     |   |   +- (2): default={}
     |   +- expand
     |   |   +- (0): if False, print out the object in one line
     |   |   +- (1): default=True
     |   +- return_instead
     |   |   +- (0): if True, no printing, but return a string instead
     |   |   +- (1): default=False
     |   +- show_type
     |       +- (0): if True, object type info will be added at the end of expanding object name
     |       +- (1): default=False
     +- author: 4lan
    

### example 4: only expand objects of particular types


```python
tree(example, 'example', expand_types={dict})
```

    example
     ├─ languages: [English, 中文, 日本語, русский, etc.]
     ├─ python versions: {python3, python2}
     ├─ types: (dict, {set}, [list], (tuple), <iterable>)
     ├─ xrange(5): <0, 1, 2, 3, 4>
     ├─ params
     │   ├─ obj: (the object to be printed)
     │   ├─ name: (the name of the object, default='root')
     │   ├─ symbol_child_birth: (the tree symbol where a sub-item is showing its first line, default=' ├─ ')
     │   ├─ symbol_child_alive: (the tree symbol where a sub-item is showing its rest lines, default=' │  ')
     │   ├─ symbol_last_child_birth: (the tree symbol where the last sub-item is showing its first line, default=' └─ ')
     │   ├─ symbol_last_child_alive: (the tree symbol where the last sub-item is showing its rest lines, default='    ')
     │   ├─ expand_types: (if not empty, only expand_types objects will be expanded, default={})
     │   ├─ no_expand_types: (all iterable objects will be expanded except no_expand_types objects, only works when expand_types is empty, default={})
     │   ├─ expand: (if False, print out the object in one line, default=True)
     │   ├─ return_instead: (if True, no printing, but return a string instead, default=False)
     │   └─ show_type: (if True, object type info will be added at the end of expanding object name, default=False)
     └─ author: 4lan
    

### example 5: expand all iterable objects except particular types


```python
tree(example, 'example', no_expand_types={list, xrange})
```

    example
     ├─ languages: [English, 中文, 日本語, русский, etc.]
     ├─ python versions
     │   ├─ {0}: python3
     │   └─ {1}: python2
     ├─ types
     │   ├─ (0): dict
     │   ├─ (1): {set}
     │   ├─ (2): [list]
     │   ├─ (3): (tuple)
     │   └─ (4): <iterable>
     ├─ xrange(5): <0, 1, 2, 3, 4>
     ├─ params
     │   ├─ obj
     │   │   └─ (0): the object to be printed
     │   ├─ name
     │   │   ├─ (0): the name of the object
     │   │   └─ (1): default='root'
     │   ├─ symbol_child_birth
     │   │   ├─ (0): the tree symbol where a sub-item is showing its first line
     │   │   └─ (1): default=' ├─ '
     │   ├─ symbol_child_alive
     │   │   ├─ (0): the tree symbol where a sub-item is showing its rest lines
     │   │   └─ (1): default=' │  '
     │   ├─ symbol_last_child_birth
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its first line
     │   │   └─ (1): default=' └─ '
     │   ├─ symbol_last_child_alive
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its rest lines
     │   │   └─ (1): default='    '
     │   ├─ expand_types
     │   │   ├─ (0): if not empty, only expand_types objects will be expanded
     │   │   └─ (1): default={}
     │   ├─ no_expand_types
     │   │   ├─ (0): all iterable objects will be expanded except no_expand_types objects
     │   │   ├─ (1): only works when expand_types is empty
     │   │   └─ (2): default={}
     │   ├─ expand
     │   │   ├─ (0): if False, print out the object in one line
     │   │   └─ (1): default=True
     │   ├─ return_instead
     │   │   ├─ (0): if True, no printing, but return a string instead
     │   │   └─ (1): default=False
     │   └─ show_type
     │       ├─ (0): if True, object type info will be added at the end of expanding object name
     │       └─ (1): default=False
     └─ author: 4lan
    

### example 6: print out in one line


```python
tree(example, 'example', expand=False)
```

    example: {languages: [English, 中文, 日本語, русский, etc.], python versions: {python3, python2}, types: (dict, {set}, [list], (tuple), <iterable>), xrange(5): <0, 1, 2, 3, 4>, params: {obj: (the object to be printed), name: (the name of the object, default='root'), symbol_child_birth: (the tree symbol where a sub-item is showing its first line, default=' ├─ '), symbol_child_alive: (the tree symbol where a sub-item is showing its rest lines, default=' │  '), symbol_last_child_birth: (the tree symbol where the last sub-item is showing its first line, default=' └─ '), symbol_last_child_alive: (the tree symbol where the last sub-item is showing its rest lines, default='    '), expand_types: (if not empty, only expand_types objects will be expanded, default={}), no_expand_types: (all iterable objects will be expanded except no_expand_types objects, only works when expand_types is empty, default={}), expand: (if False, print out the object in one line, default=True), return_instead: (if True, no printing, but return a string instead, default=False), show_type: (if True, object type info will be added at the end of expanding object name, default=False)}, author: 4lan}

### example 7: return instead


```python
print(tree(example, 'example', return_instead=True))
```

    example
     ├─ languages
     │   ├─ [0]: English
     │   ├─ [1]: 中文
     │   ├─ [2]: 日本語
     │   ├─ [3]: русский
     │   └─ [4]: etc.
     ├─ python versions
     │   ├─ {0}: python3
     │   └─ {1}: python2
     ├─ types
     │   ├─ (0): dict
     │   ├─ (1): {set}
     │   ├─ (2): [list]
     │   ├─ (3): (tuple)
     │   └─ (4): <iterable>
     ├─ xrange(5)
     │   ├─ <0>: 0
     │   ├─ <1>: 1
     │   ├─ <2>: 2
     │   ├─ <3>: 3
     │   └─ <4>: 4
     ├─ params
     │   ├─ obj
     │   │   └─ (0): the object to be printed
     │   ├─ name
     │   │   ├─ (0): the name of the object
     │   │   └─ (1): default='root'
     │   ├─ symbol_child_birth
     │   │   ├─ (0): the tree symbol where a sub-item is showing its first line
     │   │   └─ (1): default=' ├─ '
     │   ├─ symbol_child_alive
     │   │   ├─ (0): the tree symbol where a sub-item is showing its rest lines
     │   │   └─ (1): default=' │  '
     │   ├─ symbol_last_child_birth
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its first line
     │   │   └─ (1): default=' └─ '
     │   ├─ symbol_last_child_alive
     │   │   ├─ (0): the tree symbol where the last sub-item is showing its rest lines
     │   │   └─ (1): default='    '
     │   ├─ expand_types
     │   │   ├─ (0): if not empty, only expand_types objects will be expanded
     │   │   └─ (1): default={}
     │   ├─ no_expand_types
     │   │   ├─ (0): all iterable objects will be expanded except no_expand_types objects
     │   │   ├─ (1): only works when expand_types is empty
     │   │   └─ (2): default={}
     │   ├─ expand
     │   │   ├─ (0): if False, print out the object in one line
     │   │   └─ (1): default=True
     │   ├─ return_instead
     │   │   ├─ (0): if True, no printing, but return a string instead
     │   │   └─ (1): default=False
     │   └─ show_type
     │       ├─ (0): if True, object type info will be added at the end of expanding object name
     │       └─ (1): default=False
     └─ author: 4lan
    
    
