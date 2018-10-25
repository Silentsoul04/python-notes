# 映射类型(dict)

> 本章涵盖了 [Mapping Types — dict](https://docs.python.org/3.7/library/stdtypes.html#dict)，并进行了扩展。

映射([*mapping*](https://docs.python.org/3/glossary.html#term-mapping))对象会将可哈希([*hashable*](https://docs.python.org/3/glossary.html#term-hashable))对象映射到另一个对象。映射属于可变对象。目前只有一种标准的映射类型，即字典(*dictionary*)。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

## 1. hashable

> 本节内容涵盖了 [hashable - 术语表](https://docs.python.org/3.7/glossary.html#term-hashable)，并进行了扩展

"可哈希对象(*hashable*)"需实现 [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) 方法，并且"可哈希对象"的哈希值在其生命周期内永远不会发生变化。"可哈希对象"还需实现 [`__eq__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__eq__) 方法，且满足：当 `x==y` 时，`hash(x) == hash(y)` (x, y 是具备不同id的"可哈希对象")。

即使"可哈希对象"拥有不同的 id，但只要它们的哈希值相同，便可等效使用，例如：

```python
>>> x = (1,2)
>>> y = (1,2)
>>> x is y # id不同，但是hash值相同
False
>>> z = {x:"orca"}
>>> z[y] # y和x可互换使用
'orca'
```

在 Python 中，所有内置不可变对象都属于"可哈希对象"，内置可变容器不属于"可哈希对象"(如，列表和字典等)。默认情况下，自定义类的实例属于可哈希对象，但这些实例的哈希值基于其 id，也就是说不同 id 的实例的哈希值不同，例如：

```python
>>> class Cls:pass

>>> i = Cls()
>>> j = Cls()
>>> hash(i)
156321732037
>>> hash(j)
-9223371880532492263
>>> i == j # 相等性测试也基于id
False
```

可利用 [`collections.abc.Hashable`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Hashable) 来测试目标对象是否属于"可哈希对象"：

```python
>>> # isinstance(obj, collections.abc.Hashable)
>>> import collections
>>> isinstance(1,collections.abc.Hashable)
True
>>> isinstance(set((1,2)),collections.abc.Hashable)
False
>>> isinstance((1,2),collections.abc.Hashable)
True
```

扩展阅读：

- [bject.\_\_hash\_\_(self)](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__)
- [class collections.abc.Hashable](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Hashable)

## 2. 字典

字典的键和集合的成员必须是"可哈希对象"，因为这两种数据结构会在内部使用相关对象的哈希值。

数值类型被用作字典的键时，依旧遵循数值比较规则：如果两个数值相等(如 `1` 和 `1.0` )，字典会认为这两个数值均代表同一个键(可互换)。因此在索引字典时，相等的数值可互换使用。不过由于计算机以近似值存储浮点数，因此最好不要将浮点数用作字典的键。

```python
>>> j = {1:"orca"}
>>> j[1.0] # 1和1.0可互换使用
'orca'
```

扩展：可利用 [`types.MappingProxyType`](https://docs.python.org/3.7/library/types.html#types.MappingProxyType) 为字典创建的只读视图(*view*)。

### 2.1 构建字典

可通过以下几种方式来构建字典：

- 使用一对花括号可构建一个空字典：`{}`

- 使用一对花括号，并在其中填充以逗号分隔的键值对：

  ```python
  >>> i = {'jack': 4098, 'sjoerd': 4127}
  >>> j = {4098: 'jack', 4127: 'sjoerd'}
  >>> k = {**i, **j} # 拆封i和j
  >>> k
  {'jack': 4098, 'sjoerd': 4127, 4098: 'jack', 4127: 'sjoerd'}
  ```

- 使用字典解析式：`{x: x * x for x in [1,2,3,4,5,6]}`

- 使用类型构造器：`dict(**kwarg)` , `dict(mapping, **kwarg)` , `dict(iterable, **kwarg)`

在构造字典对象时，如果某个键多次出现在不同的键值对中，那么该键在新字典中的值是最后出现的那个值。

#### a. 构造器 dict()

```
class dict(object)
 |  dict() -> new empty dictionary
 |  dict(mapping) -> new dictionary initialized from a mapping object's
 |      (key, value) pairs
 |  dict(iterable) -> new dictionary initialized as if via:
 |      d = {}
 |      for k, v in iterable:
 |          d[k] = v
 |  dict(**kwargs) -> new dictionary initialized with the name=value pairs
 |      in the keyword argument list.  For example:  dict(one=1, two=2)
```

构造器 `dict()` 的使用方法如下：

🔨 class dict()

```
 dict() -> new empty dictionary
```

🔨 class dict(\*\**kwarg*)

```
dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list.  
For example:  dict(one=1, two=2)
```

示例 - 展示两种传递关键字实参的方法

```python
>>> d = dict(one=1, two=2) # 直接给出关键字实参
>>> d
{'one': 1, 'two': 2} 
>>> d_ = dict(**d) # 通过拆封传递关键字实参
>>> d_
{'one': 1, 'two': 2}
```

注意，关键字实参的名称必须是有效标识符。

🔨 class dict(*mapping*, \*\**kwarg*)

```
dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs
```

如果将一个映射对象作为实参，则会新建一个该映射对象的浅拷贝副本：

```python
dict_ = {'a':1,'b':(1,2),'c':[3,4]}
d1 = dict(dict_)
```

执行结果：

![构建字典](0x09 映射类型(dict).assets/构建字典.png)

🔨 class dict(*iterable*, \*\**kwarg*)

```
dict(iterable) -> new dictionary initialized as if via:
       d = {}
       for k, v in iterable:
           d[k] = v
```

被用作实参的可迭代对象中的每一项必须是一个包含两个元素的可迭代对象。例如：

```python
>>> dict(zip(['one', 'two', 'three'], [1, 2, 3]))
{'one': 1, 'two': 2, 'three': 3}
>>> dict([('two', 2), ('one', 1), ('three', 3)])
{'two': 2, 'one': 1, 'three': 3}
```

### 2.2 字典支持的操作

以下是字典所支持的操作，自定义映射类型也应支持这些操作。

#### 类方法

classmethod `fromkeys`(*seq*[, *value*])

以 *seq* 中的项作为键创建一个新字典，并将各个键的值设为 *value* (*value* 的默认值是 `None` )。

```python
>>> dict.fromkeys(range(5))
{0: None, 1: None, 2: None, 3: None, 4: None}
>>> dict.fromkeys(range(5),'Orca')
{0: 'Orca', 1: 'Orca', 2: 'Orca', 3: 'Orca', 4: 'Orca'}
```

#### 与项相关的操作

在字典中，项(*item*)或条目(*entry*)被用于表示一个键值对。

- `len(d)` - 返回字典 `d` 中的项的数量

- `d.clear() ` - 移除字典中所有的项

- `d.copy() ` - 返回字典实例的浅拷贝副本

- `d.popitem() ` - 会按照 LIFO 的顺序移除 `d` 中的项，并以元组形式返回被移除的项。当需要对字典进行破坏性迭代时，通常会使用 `popitem` 方法。在空字典上调用 `popitem` 方法时，会抛出 `KeyError` 

  ```python
  >>> d = {'a':1,'b':2,'c':3}
  >>> d.popitem()
  ('c', 3)
  ```

  Changed in version 3.7: LIFO order is now guaranteed. In prior versions, [`popitem()`](https://docs.python.org/3.7/library/stdtypes.html#dict.popitem)would return an arbitrary key/value pair.

- `d.update([other])` - 将 `other` 中的键值对添加到字典中，该操作会覆盖已有的键值对，返回值是 `None` 。`other` 可以是一个字典，也可以是以『 `key,value` 』为单元的可迭代对象。在 `update` 方法中也可使用关键字参数：`d.update(red=1, blue=2)`

  ```python
  >>> d = {'a':1}
  >>> d.update({'b':2})
  >>> d.update([('c',3)])
  >>> d.update(d=4)
  >>> d
  {'a': 1, 'b': 2, 'c': 3, 'd': 4}
  ```

#### 与键相关的操作

- `d[key]` - 返回字典 `d` 中 `key` 键的值，如果字典中没有 `key` 键，则抛出 [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) 异常。

  如果已在 `dict` 类的子类 `dict_sub` 中定义了 [`__missing__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__) 方法。当 `dict_sub` 类的实例 `d_sub` 中没有 `key` 键时，`d_sub[key]` 操作便会调用 `__missing__` 方法并以 `key` 作为实参。字典中的其它操作或方法不会调用 `__missing__` 。如果子类中未定义 `__missing__` 方法，则会抛出 `keyError` 。`__missing__` 必须是一个方法，不可以是实例字段。

  ```python
  >>> class Counter(dict):
      def __missing__(self, key):
          return 0
  
  >>> c = Counter()
  >>> c['red'] # 此处会调用c.__missing__
  0
  >>> c['red'] += 1
  >>> c['red']
  1
  ```

  上面的代码展示了 [`collections.Counter`](https://docs.python.org/3.7/library/collections.html#collections.Counter) 类的部分实现， `__missing__` 方法的另一种用法可参考 [`collections.defaultdict`](https://docs.python.org/3.7/library/collections.html#collections.defaultdict)。

- `d[key] = value` - 设置键 `key` 的值为 `value`

- `del d[key]` - 从 `d` 中删除 `d[key]` ，如果映射中没有 `key` 键，则抛出 [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) 异常。

- `d.get(key[,default])` - 如果字典中包含 `key` 键，则返回其值；否则返回 `default` 。`default` 的默认值是 `None` ，因此 `get` 方法永远不会抛出 [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError)。

- `d.pop(key[, default])` - 如果字典中包含 `key` 键，则移除 `key` 键并返回其值；否则返回 `default` (如果没有给出 `default` 的值，则会抛出 [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) 异常)。

  ```python
  >>> d = {'a':1,'b':2,'c':3}
  >>> d.pop('c')
  3
  >>> d.pop('c')
  Traceback (most recent call last):
    File "<pyshell#3>", line 1, in <module>
      d.pop('c')
  KeyError: 'c'
  ```

- `d.setdefault(key[,default])` - 如果字典中包含 `key` 键，则返回其值；否则在字典中插入 `key:default`，并返回 `default`。`default` 的默认值是 `None`。

  ```python
  >>> d = {'a':1,'b':2,'c':3}
  >>> d.setdefault('a')
  1
  >>> d.setdefault('d')
  >>> d
  {'a': 1, 'b': 2, 'c': 3, 'd': None}
  ```

- `iter(d)` - 等效于 `iter(d.keys())`，返回一个包含 `d` 中所有键的迭代器。

  ```python
  >>> d = {'a':1,'b':2}
  >>> d_iter = iter(d)
  >>> d['c']=3
  >>> list(d_iter) # 改变字典后，d_iter会抛出异常
  Traceback (most recent call last):
    File "<pyshell#72>", line 1, in <module>
      list(d_iter)
  RuntimeError: dictionary changed size during iteration
  ```

- `list(d)` - 等效于 `list(d.keys())`，返回一个包含 `d` 中所有键的列表。

  ```python
  >>> d = {'a':1,'b':2}
  >>> d_list = list(d)
  >>> d_list
  ['a', 'b']
  >>> d['c']=3
  >>> d_list # 改变字典后，不会影响d_list
  ['a', 'b']
  ```

- `key in d` - 测试 `d` 中是否包含 `key` 键，返回 `True` 表示包含，`False` 表示不包含。

- `key not in d` - 等效于 `not key in d`

#### 获取视图对象

- `d.items`() - 返回由字典 `d` 中的项构成的新视图(*view*)。
- `d.keys`() - 返回由字典 `d` 中的键构成的新视图(*view*)。
- `d.values`() - 返回由字典 `d` 中的值构成的新视图(*view*)。

视图对象与字典 `d` 联动，当 `d` 中的项发生变化时，视图对象也将发生变化。另外，视图对象还支持成员测试、迭代等操作。具体细节请看"字典视图对象"小节。

```python
>>> d = {'a':1,'b':2,'c':3}
>>>
>>> d_items = d.items()
>>> d_items
dict_items([('a', 1), ('b', 2), ('c', 3)])
>>>
>>> d_keys = d.keys()
>>> d_keys
dict_keys(['a', 'b', 'c'])
>>>
>>> d_values = d.values()
>>> d_values
dict_values([1, 2, 3])
>>> # 修改字典后，视图对象也将发生变化
>>> d['d']=4
>>> d_items
dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
>>> d_keys
dict_keys(['a', 'b', 'c', 'd'])
>>> d_values
dict_values([1, 2, 3, 4])
```

### 2.3 字典视图对象

我们可以从字典对象中获取三种视图对象(*view objects*)：

```
dict.keys() -> dict_keys object # 键视图对象
dict_values() -> dict_values object # 值视图对象
dict.items() -> dict_items object # 项视图对象
```

视图对象与字典内容动态关联，也就是说当字典发生变化时，视图对象也会发生相应的变化。

视图对象支持的操作如下：(`dictview` 可以是三种视图中的任意一个)

- `len(dictview)` 

  返回字典中的条目的数量

- `iter(dictview)` 

  返回一个迭代器，迭代器生成的内容与视图内容一致。

  由于迭代器会按照插入顺序生成键和值，因此可通过以下两种方式获取 `(value,key)` 列表：

  -  `zip()` 函数 - `pairs = zip(d.values(), d.keys())`
  - 列表解析 - `pairs = [(v, k) for (k, v) in d.items()]`

  ```python
  >>> list(zip(d.values(), d.keys()))
  [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
  >>> [(v, k) for (k, v) in d.items()]
  [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')]
  ```

  在向字典添加或删除条目时迭代视图对象，则可能会抛出 [`RuntimeError`](https://docs.python.org/3.7/library/exceptions.html#RuntimeError) 异常，或不能遍历所有条目。

  Changed in version 3.7: 保证字典保持插入顺序。

- `x in dictview`

  测试视图对象中是否包含 `x`，返回 `True` 表示包含，`False` 表示不包含。当视图对象是 `dict_items`  类型时，`x` 该是一个键值对元组( `(key, value)` )。

  ```python
  >>> d = dict(a=1,b=2,c=3)
  >>> ('d',4) in d.items() # 
  True
  ```

键视图是 set-like 对象，因为  `dict_keys` 中元素唯一且都

由于"键视图"中的元素满足唯一性且均可哈希，所以"键视图"是 set-like 对象。如果字典中所有的值也都可哈希，那么"项视图"也是 set-like 对象，因为此时"项视图"中的元素 `(key, value)` 满足唯一性且均可哈希。由于"值视图"中的元素通常不满足唯一性，所以"值视图"不被视作 set-like 对象。对 set-like 视图来说，抽象基类  [`collections.abc.Set`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Set) 中定义的操作皆可被使用(如：`==`, `<`,  `^`)。

```python
>>> d
{'a': 1, 'b': 2, 'c': 3, 'd': 4}
>>> isinstance(d.keys(),Set)
True
>>> isinstance(d.values(),Set)
False
>>> isinstance(d.items(),Set)
True
>>> d['list_']=[1,2]
>>> isinstance(d.items(),Set)
True
>>> d.items()
dict_items([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('list_', [1, 2])])
>>> 
```



那么键值对元组 `(key, value)` 中的元素也满足唯一性，且均可被哈希，此时项视图也是 set-like 对象。

Keys views are set-like since their entries are unique and hashable. If all values are hashable, so that `(key, value)` pairs are unique and hashable, then the items view is also set-like. (Values views are not treated as set-like since the entries are generally not unique.) For set-like views, all of the operations defined for the abstract base class [`collections.abc.Set`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Set) are available (for example, `==`, `<`, or `^`).

示例 - 字典视图的常见用法：

```python
>>> dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}
>>> keys = dishes.keys()
>>> values = dishes.values()

>>> # iteration
>>> n = 0
>>> for val in values:
...     n += val
>>> print(n)
504

>>> # keys and values are iterated over in the same order (insertion order)
>>> list(keys)
['eggs', 'sausage', 'bacon', 'spam']
>>> list(values)
[2, 1, 1, 500]

>>> # view objects are dynamic and reflect dict changes
>>> del dishes['eggs']
>>> del dishes['sausage']
>>> list(keys)
['bacon', 'spam']

>>> # set operations
>>> keys & {'eggs', 'bacon', 'salad'}
{'bacon'}
>>> keys ^ {'sausage', 'juice'}
{'juice', 'sausage', 'bacon', 'spam'}
```



### 2.3 字典拆封

> 本节内容参考自 [6.2.7. Dictionary displays](https://docs.python.org/3.7/reference/expressions.html#dictionary-displays)

双星号 `**` 用于字典拆封(*unpacking*)，其操作数必须是映射([*mapping*](https://docs.python.org/3.7/glossary.html#term-mapping))。

例如在构建字典时，可使用 `**` 拆封某个字典，从而获取该字典中的键值对。被拆封的字典中的所有键值对都会被添加到新字典中，如果某个键被重复添加，则保留最后一次添加的值。

```python
>>> i = {'jack': 4098, 'sjoerd': 4127}
>>> j = {4098: 'jack', 4127: 'sjoerd'}
>>> k = {**i, **j} # 拆封
>>> k
{'jack': 4098, 'sjoerd': 4127, 4098: 'jack', 4127: 'sjoerd'}
```

在调用函数时，可使用 `**` 对打包到字典中的参数进行拆封：

```python
>>> def func(a,b,c):
	print(a,b,c)

>>> func(**dict(a=1,b=2,c=3))
1 2 3
```

## 提示

### a. 拷贝字典

浅拷贝时，原映射中"值"引用的可变对象**不会产生**新副本，仅会对可变对象的引用进行多次拷贝。若在新副本中修改可变对象，原副本中的可变对象也会发生改变。copy 模块中的 `copy()` 属于浅拷贝(*shallow copy*)

深拷贝时，原映射中"值"引用的可变对象都**会产生**新副本，并会在新映射中引用这些副本。若在新副本中修改可变对象，原副本中的可变对象不受影响。copy 模块中的 `deepcopy()` 属于深拷贝(*deep copy*)

对于不可变对象，由于本身并不能被修改，因此在浅拷贝和深拷贝中都直接拷贝其引用。

示例 - 观察浅拷贝和深拷贝的区别：

```python
import copy
dict_ = {'a':1,'b':(1,2),'c':[3,4]}
# dict(dict_),dict_.copy(),copy.copy(dict_)都执行浅拷贝，相互等效
d3 = dict(dict_)
d4 = copy.deepcopy(dict_)
```

执行结果：

![拷贝字典](0x09 映射类型(dict).assets/拷贝字典.png)

### b. 比较字典

在比较运算符中，仅 `==` 和 `！=` 对字典有效。若在字典上使用其余的比较运算符( `<`, `<=`, `>=`, `>`)，则会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError) 异常。

```python
>>> d = {'a':1,'b':2}
>>> d_ = d.copy()
>>> d is d_
False
>>> d == d_
True
>>> d > d_
Traceback (most recent call last):
  File "<pyshell#77>", line 1, in <module>
    d > d_
TypeError: '>' not supported between instances of 'dict' and 'dict'
```

### c. 项的顺序

字典中项的顺序与插入顺序一致。更新已有的键的值，并不会影响项的顺序。如果在删除某个键后，又将其重新添加到字典中，则会在尾部插入该项。

```python
>>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
>>> d
{'one': 1, 'two': 2, 'three': 3, 'four': 4}
>>> list(d)
['one', 'two', 'three', 'four']
>>> list(d.values())
[1, 2, 3, 4]
>>> d["one"] = 42
>>> d
{'one': 42, 'two': 2, 'three': 3, 'four': 4}
>>> del d["two"]
>>> d["two"] = None
>>> d
{'one': 42, 'three': 3, 'four': 4, 'two': None}
```

Changed in version 3.7: Dictionary order is guaranteed to be insertion order. This behavior was implementation detail of CPython from 3.6.

## 扩展阅读

