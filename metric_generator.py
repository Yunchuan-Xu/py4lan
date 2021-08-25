from abc import ABC, abstractmethod
from copy import deepcopy
import re

import numpy as np

_abs = abs
_min = min
_max = max
_valid_names = {
    '_x2m',
    'abs',
    'acc',
    'amplitude',
    'at',
    'autoregress',
    'avg',
    'bottom',
    'choices',
    'concat',
    'const',
    'cos',
    'cycle',
    'diff',
    'downsample',
    'end',
    'factors',
    'frag',
    'initial_phase',
    'left',
    'lines',
    'loc',
    'max',
    'median',
    'method',
    'metric1',
    'metric2',
    'min',
    'n',
    'normal',
    'padding',
    'paddings',
    'period',
    'points',
    'pos',
    'pulse',
    'rand',
    'rand_choice',
    'rand_int',
    'rect',
    'regress',
    'repeat',
    'right',
    'sample_size',
    'scale',
    'shift',
    'sin',
    'smooth',
    'start',
    'up',
    'val',
    'value',
    'values',
    'weights',
    'window_size',
    'x'
}


def _show_iterable_with_length_limit(obj, n):
     return f'[{", ".join(map(str, obj[:n]))}{f", ..." if len(obj) > n else ""}]'


def _x2m(x):
    if isinstance(x, Metric):
        return x
    elif isinstance(x, (int, float)):
        return Const(x)
    elif isinstance(x, (list, tuple)):
        return Fragment(x)
    elif isinstance(x, dict):
        pos = sorted(x.keys())
        val = [x[k] for k in pos]
        return Pulse(pos, val)


def abs(x):
    if isinstance(x, Metric):
        return Abs(x)
    else:
        return _abs(x)


def min(*xs):
    for x in xs:
        if isinstance(x, Metric):
            return Min(*xs)
    return _min(*xs)


def max(*xs):
    for x in xs:
        if isinstance(x, Metric):
            return Max(*xs)
    return _max(*xs)


class Metric(ABC):
    def __init__(self):
        self._i = -1
        self._v = None

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        self._v = self._calc(self._i)
        return self._v

    def __getitem__(self, item):
        if item < 0:
            raise ValueError('does not support negative indexing')
        if item < self._i:
            raise ValueError('cannot go backward')
        for i in range(item - self._i):
            self.__next__()
        return self._v

    def __pos__(self):
        return Add(0, self)

    def __neg__(self):
        return Sub(0, self)

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __floordiv__(self, other):
        return Div(self, other, floor=True)

    def __rfloordiv__(self, other):
        return Div(other, self, floor=True)

    def __mod__(self, other):
        return Mod(self, other)

    def __rmod__(self, other):
        return Mod(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    def __lshift__(self, other):
        return Shift(self, -other)

    def __rshift__(self, other):
        return Shift(self, other)

    def __matmul__(self, other):
        return Pulse(other, self)

    def __rmatmul__(self, other):
        return Pulse(self, other)

    @property
    def last(self):
        return self._v
    
    def next(self, n=1):
        return [self.__next__() for _ in range(n)]

    def reset(self):
        self._reset()
        self._i = -1
        self._v = None

    def restore(self, from_obj):
        for k, v in from_obj.__dict__.items():
            if isinstance(v, Metric):
                self.__dict__[k].restore(v)
            elif isinstance(v, list):
                for i, vi in enumerate(v):
                    if isinstance(vi, Metric):
                        self.__dict__[k][i].restore(vi)
                    else:
                        self.__dict__[k][i] = vi
            else:
                self.__dict__[k] = v
    
    def acc(self):
        return Acc(self)

    def diff(self):
        return Diff(self)

    def shift(self, n, padding=0):
        return Shift(self, n, padding=padding)

    def smooth(self, window_size):
        return Smooth(self, window_size)

    def regress(self, factors, paddings=None):
        return Regress(self, factors, paddings=paddings)

    def autoregress(self, factors):
        return AutoRegress(self, factors)

    def downsample(self, sample_size, method='avg'):
        return Downsample(self, sample_size, method=method)

    def repeat(self, start, end, n=None):
        return Repeat(self, start, end, n=n)

    def cycle(self, start, end, n=None):
        return Cycle(self, start, end, n=n)

    def concat(self, at, other):
        return Concat(self, other, at=at)

    def val(self, val):
        return Pulse(self, val)

    def as_pos(self, val):
        return Pulse(self, val)

    def at(self, pos):
        return Pulse(pos, self)

    def as_val(self, pos):
        return Pulse(pos, self)

    @abstractmethod
    def _calc(self, item):
        pass

    @abstractmethod
    def _reset(self):
        pass


class Const(Metric):
    def __init__(self, value):
        self.value = value
        super().__init__()
    
    def __repr__(self):
        return f'<Const({self.value})>'
    
    def _calc(self, item):
        return self.value
    
    def _reset(self):
        pass


class Fragment(Metric):
    def __init__(self, values):
        self.values = values
        self.len = len(values)
        super().__init__()
    
    def __repr__(self):
        return f'<Fragment({_show_iterable_with_length_limit(self.values, 4)}, len={self.len})>'
    
    def _calc(self, item):
        return self.values[item] if item < self.len else 0
    
    def _reset(self):
        pass


class Normal(Metric):
    def __init__(self, scale=1, loc=0):
        self.scale = scale
        self.loc = loc
        super().__init__()

    def __repr__(self):
        return f'<Normal({self.scale}, loc={self.loc})>'
    
    def _calc(self, item):
        return np.random.normal(loc=self.loc, scale=self.scale)
    
    def _reset(self):
        pass


class Rand(Metric):
    def __init__(self, *args):
        if len(args) == 0:
            args = [0, 1]
        elif len(args) == 1:
            args = [0, args[0]]
        self.low = _min(args)
        self.high = _max(args)
        self.range = high - low
        super().__init__()
    
    def __repr__(self):
        return f'<Rand({self.low}, {self.high})>'
    
    def _calc(self, item):
        return self.low + np.random.random() * self.range
    
    def _reset(self):
        pass


class RandInt(Metric):
    def __init__(self, *args):
        if len(args) == 0:
            args = [0, 1]
        elif len(args) == 1:
            args = [0, args[0]]
        self.low = _min(args)
        self.high = _max(args)
        super().__init__()

    def __repr__(self):
        return f'<RandInt({self.low}, {self.high})>'
    
    def _calc(self, item):
        return np.random.randint(self.low, self.high + 1)
    
    def _reset(self):
        pass


class RandChoice(Metric):
    def __init__(self, choices, weights=None):
        self.choices = choices
        self.len = len(choices)
        if weights is None:
            self.weights = [1 / self.len] * self.len
        elif len(weights) != self.len:
            raise ValueError('weights should be of same length as choices')
        else:
            weight_sum = sum(weights)
            self.weights = [w / weight_sum for w in weights]
        super().__init__()
    
    def __repr__(self):
        return (f'<RandChoice({_show_iterable_with_length_limit(self.choices, 4)}, '
                f'len={self.len}, '
                f'weights={_show_iterable_with_length_limit(self.weights, 4)}'
                ')>')
    
    def _calc(self, item):
        return np.random.choice(self.choices, p=self.weights)
    
    def _reset(self):
        pass


class Sin(Metric):
    def __init__(self, period, amplitude=1, initial_phase=0):
        self.period = period
        self.amplitude = amplitude
        self.initial_phase = initial_phase
        self.phase = initial_phase
        super().__init__()
    
    def __repr__(self):
        return f'<Sin(period={self.period}, amplitude={self.amplitude}, initial_phase={self.initial_phase})>'
    
    def _calc(self, item):
        return self.amplitude * np.sin(item * (2 * np.pi) / self.period + self.initial_phase)
    
    def _reset(self):
        self.phase = self.initial_phase


class Cos(Metric):
    def __init__(self, period, amplitude=1, initial_phase=0):
        self.period = period
        self.amplitude = amplitude
        self.initial_phase = initial_phase
        self.phase = initial_phase
        super().__init__()
    
    def __repr__(self):
        return f'<Cos(period={self.period}, amplitude={self.amplitude}, initial_phase={self.initial_phase})>'
    
    def _calc(self, item):
        return self.amplitude * np.cos(item * (2 * np.pi) / self.period + self.initial_phase)
    
    def _reset(self):
        self.phase = self.initial_phase


class Abs(Metric):
    def __init__(self, metric):
        self.metric = _x2m(metric)
        super().__init__()
    
    def __repr__(self):
        return f'Abs({self.metric})'
    
    def _calc(self, item):
        return _max(self.metric.__next__(), 0)
    
    def _reset(self):
        self.metric.reset()


class Acc(Metric):
    def __init__(self, metric):
        self.metric = _x2m(metric)
        self.value = 0
        super().__init__()
    
    def __repr__(self):
        return f'<Acc({self.metric})>'
    
    def _calc(self, item):
        self.value += self.metric.__next__()
        return self.value
    
    def _reset(self):
        self.metric.reset()
        self.value = 0


class Diff(Metric):
    def __init__(self, metric):
        self.metric = _x2m(metric)
        self.value = np.nan
        super().__init__()
    
    def __repr__(self):
        return f'<Diff({self.metric})>'
    
    def _calc(self, item):
        old_value = self.value
        self.value = self.metric.__next__()
        return self.value - old_value
    
    def _reset(self):
        self.metric.reset()
        self.value = np.nan


class Shift(Metric):
    def __init__(self, metric, n, padding=0):
        self.metric = _x2m(metric)
        self.n = n
        self.n_left = _max(0, n)
        self.padding = padding
        for i in range(-n):
            self.metric.__next__()
        super().__init__()
    
    def __repr__(self):
        return f'<Shift({self.metric}, n={self.n}, padding={self.padding})>'
    
    def _calc(self, item):
        if self.n_left > 0:
            self.n_left -= 1
            return self.padding
        else:
            return self.metric.__next__()
    
    def _reset(self):
        self.metric.reset()
        self.n_left = self.n


class Smooth(Metric):
    def __init__(self, metric, window_size):
        self.metric = _x2m(metric)
        self.window_size = window_size
        self.window_values = [np.nan] * window_size
        super().__init__()
    
    def __repr__(self):
        return f'<Smooth({self.metric}, window_size={self.window_size})'
    
    def _calc(self, item):
        self.window_values.pop(0)
        self.window_values.append(self.metric.__next__())
        return np.nanmean(self.window_values)
    
    def _reset(self):
        self.window_values = [np.nan] * self.window_size
        self.metric.reset()


class Regress(Metric):
    def __init__(self, metric, factors, paddings=None):
        self.metric = _x2m(metric)
        self.factors = factors
        self.window_size = len(factors)
        self.paddings = Const(0) if paddings is None else _x2m(paddings)
        self.window_values = self.paddings.next(self.window_size)
        super().__init__()
    
    def __repr__(self):
        return (f'<Regress({self.metric}, '
                f'factors={_show_iterable_with_length_limit(self.factors, 4)}, '
                f'window_size={self.window_size}, '
                f'paddings={self.paddings}'
                ')>')
    
    def _calc(self, item):
        self.window_values.pop(0)
        self.window_values.append(self.metric.__next__())
        return sum(self.window_values[i] * self.factors[i] for i in range(self.window_size))
    
    def _reset(self):
        self.metric.reset()
        self.paddings.reset()
        self.window_values = self.paddings.next(self.window_size)


class AutoRegress(Metric):
    def __init__(self, metric, factors):
        self.metric = _x2m(metric)
        self.factors = factors
        self.window_size = len(factors)
        self.initials = self.metric.next(self.window_size)
        self.window_values = []
        super().__init__()
    
    def __repr__(self):
        return (f'<AutoRegress({self.metric}, '
                f'factors={_show_iterable_with_length_limit(self.factors, 4)}, '
                f'window_size={self.window_size}'
                ')>')
    
    def _calc(self, item):
        if len(self.window_values) < self.window_size:
            value = self.initials[len(self.window_values)]
        else:
            value = sum(self.window_values[i] * self.factors[i] for i in range(self.window_size))
            self.window_values.pop(0)
        self.window_values.append(value)
        return value
    
    def _reset(self):
        self.metric.reset()
        self.initials = self.metric.next(self.window_size)
        self.window_values = []


class Downsample(Metric):
    def __init__(self, metric, sample_size, method='avg'):
        if method not in ('avg', 'max', 'min'):
            raise ValueError(f'invalid method "{method}"')
        self.metric = _x2m(metric)
        self.sample_size = sample_size
        self.method = method
        super().__init__()
    
    def __repr__(self):
        return f'<Downsample({self.metric}, sample_size={self.sample_size}, method={self.method})>'
    
    def _calc(self, item):
        samples = self.metric.next(self.sample_size)
        if self.method == 'avg':
            value = np.nanmean(samples)
        elif self.method == 'max':
            value = np.nanmax(samples)
        elif self.method == 'min':
            value = np.nanmin(samples)
        return value
    
    def _reset(self):
        self.metric.reset()


class Repeat(Metric):
    def __init__(self, metric, start, end, n=None):
        self.metric = _x2m(metric)
        self.start = start
        self.end = end
        self.n = n
        self.period = end - start
        self.exit = None if n is None else start + self.period * n
        self.v = []
        super().__init__()
    
    def __repr__(self):
        return (f'<Repeat({self.metric}, '
                f'start={self.start}, '
                f'end={self.end}, '
                f'n={self.n}'
                ')>')
    
    def _calc(self, item):        
        if item < self.start or (self.exit is not None and item >= self.exit):
            value = self.metric.__next__()
        elif len(self.v) < self.period:
            value = self.metric.__next__()
            self.v.append(value)
        else:
            value = self.v[(item - self.start) % self.period]
        return value
    
    def _reset(self):
        self.v = []
        self.metric.reset()


class Cycle(Metric):
    def __init__(self, metric, start, end, n=None):
        self.metric = _x2m(metric)
        self.start = start
        self.end = end
        self.n = n
        self.period = end - start
        self.exit = None if n is None else start + self.period * n
        self.checkpoint = None
        super().__init__()
    
    def __repr__(self):
        return (f'<Cycle({self.metric}, '
                f'start={self.start}, '
                f'end={self.end}, '
                f'n={self.n}'
                ')>')
    
    def _calc(self, item):
        if item < self.start or (self.exit is not None and item >= self.exit):
            value = self.metric.__next__()
        elif self.checkpoint is None:
            self.checkpoint = deepcopy(self.metric)
            value = self.metric.__next__()
        elif (item - self.start) % self.period == 0:
            self.metric.restore(self.checkpoint)
            value = self.metric.__next__()
        else:
            value = self.metric.__next__()
        return value
    
    def _reset(self):
        self.metric.reset()


class Concat(Metric):
    def __init__(self, metric1, metric2, at=0):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        self.at = at
        super().__init__()

    def __repr__(self):
        return (f'<Concat({self.metric1}, {self.metric2}, at={self.at})>')
    
    def _calc(self, item):
        if item < self.at:
            return self.metric1.__next__()
        else:
            return self.metric2.__next__()
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Add(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        super().__init__()
    
    def __repr__(self):
        return f'<Add({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        return self.metric1.__next__() + self.metric2.__next__()
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Sub(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        super().__init__()
    
    def __repr__(self):
        return f'<Sub({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        return self.metric1.__next__() - self.metric2.__next__()
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Mul(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        super().__init__()
    
    def __repr__(self):
        return f'<Mul({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        return self.metric1.__next__() * self.metric2.__next__()
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Div(Metric):
    def __init__(self, metric1, metric2, floor=False):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        self.floor = floor
        super().__init__()
    
    def __repr__(self):
        return f'<{"Floor" if self.floor else ""}Div({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        v1 = self.metric1.__next__()
        v2 = self.metric2.__next__()
        if np.isnan(v2):
            return np.nan
        elif v2 == 0:
            return np.inf
        else:
            return v1 // v2 if self.floor else v1 / v2
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Mod(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        super().__init__()
    
    def __repr__(self):
        return f'<Mod({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        v1 = self.metric1.__next__()
        v2 = self.metric2.__next__()
        if np.isnan(v2):
            return np.nan
        elif v2 == 0:
            return v1
        else:
            return v1 % v2
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Pow(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = _x2m(metric1)
        self.metric2 = _x2m(metric2)
        super().__init__()
    
    def __repr__(self):
        return f'<Pow({self.metric1}, {self.metric2})>'
    
    def _calc(self, item):
        return self.metric1.__next__() ** self.metric2.__next__()
    
    def _reset(self):
        self.metric1.reset()
        self.metric2.reset()


class Pulse(Metric):
    def __init__(self, pos, val):
        self.pos = _x2m(pos)
        self.val = _x2m(val)
        self.p = self.pos.__next__()
        self.v = self.val.__next__()
        super().__init__()
    
    def __repr__(self):
        return (f'<Pulse(pos={self.pos}, val={self.val})>')
    
    def _calc(self, item):
        if item == self.p:
            value = self.v
            self.p = self.pos.__next__()
            self.v = self.val.__next__()
        else:
            value = 0
        return value
    
    def _reset(self):
        self.pos.reset()
        self.val.reset()
        self.p = self.pos.__next__()
        self.v = self.val.__next__()


class Min(Metric):
    def __init__(self, *args):
        self.metrics = [_x2m(x) for x in args]
        super().__init__()
    
    def __repr__(self):
        return f'Min({", ".join(str(metric) for metric in self.metrics)})'
    
    def _calc(self, item):
        return _min(metric.__next__() for metric in self.metrics)
    
    def _reset(self):
        [metric.reset() for metric in self.metrics]


class Max(Metric):
    def __init__(self, *args):
        self.metrics = [_x2m(x) for x in args]
        super().__init__()
    
    def __repr__(self):
        return f'Max({", ".join(str(metric) for metric in self.metrics)})'
    
    def _calc(self, item):
        return _max(metric.__next__() for metric in self.metrics)
    
    def _reset(self):
        [metric.reset() for metric in self.metrics]


def const(value):
    return Const(value)


def frag(values):
    return Fragment(values)


def normal(scale=1, loc=0):
    return Normal(scale, loc)


def rand(*args):
    return Rand(*args)


def rand_int(*args):
    return RandInt(*args)


def rand_choice(choices, weights=None):
    return RandChoice(choices, weights)


def sin(period, amplitude=1, initial_phase=0):
    return Sin(period, amplitude=amplitude, initial_phase=initial_phase)


def cos(period, amplitude=1, initial_phase=0):
    return Cos(period, amplitude=amplitude, initial_phase=initial_phase)


def acc(x):
    return Acc(x)


def diff(x):
    return Diff(x)


def shift(x, n, padding=0):
    return Shift(x, n, padding=padding)


def smooth(x, window_size):
    return Smooth(x, window_size)


def regress(x, factors, paddings=None):
    return Regress(x, factors, paddings=paddings)


def autoregress(x, factors):
    return AutoRegress(x, factors)


def downsample(metric, sample_size, method='avg'):
    return Downsample(metric, sample_size, method=method)


def repeat(metric, period, start, end, n=None):
    return Repeat(metric, period, start, end, n=n)


def cycle(metric, period, start, end, n=None):
    return Cycle(metric, period, start, end, n=n)


def concat(metric1, metric2, at=0):
    return Concat(metric1, metric2, at=at)


def pulse(pos, val):
    return Pulse(pos, val)


def rect(left, right, bottom, up):
    return const(bottom).concat(left, const(up)).concat(right, const(bottom))


def lines(points):
    x, y = zip(*points)
    m = const(y[0])
    for i in range(len(x) - 1):
        delta = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        m = m.concat(x[i], y[i] + const(delta).acc() - delta)
    return m.concat(x[-1], const(y[-1]))


def parse(expr, **metrics):
    expr = re.sub(r'#([0-9.]+(?![a-zA-Z])|\[[^\]]*\]|{[^}]*})', lambda x: f'_x2m({x.group(1)})', expr.strip())
    for name in re.findall(r'(?<![\$a-zA-Z_])[a-zA-Z_]+[a-zA-Z0-9]*', expr):
        if name not in _valid_names:
            raise SyntaxError(f'invalid name: {name}')
    available_metrics = {k: v for k, v in metrics.items() if isinstance(v, Metric)}
    for name in re.findall(r'(?<=\$)[a-zA-Z_]+[a-zA-Z0-9]*', expr):
        if name not in available_metrics:
            raise ValueError(f'metric {name} not found')
    expr = expr.replace('$', '')
    return eval(expr, globals(), available_metrics)
