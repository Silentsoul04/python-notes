# 集合类型(set, frozenset)

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库。
>
> 本笔记涵盖了 [Set Types — set, frozenset](https://docs.python.org/3.7/library/stdtypes.html#set-types-set-frozenset)，并进行了扩展。

集合(*set*)对象是由不同的可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象组成的无序集合。set 对象常用于成员测试；从序列中删除重复项；进行数学运算，如交集(*intersection*), 并集(*union*), 差集(*difference*), 对称差集(*symmetric* difference)。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

关于可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象，详见笔记「映射类型(dict).md」-> 1. hashable

与其它集合(*collection*)一样，set 同样支持 `x in set`、`len(set)` 和 `for x in set` (还可参考 [collections.abc.Set](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Set))。set 作为无需集合，不会记录元素的位置或插入顺序。因此，set 不支持索引、切片或其它类序列(*sequence*-*like*)行为。

目前有两种内置 set 类型：[set](https://docs.python.org/3.7/library/stdtypes.html#set) 和 [frozenset](https://docs.python.org/3.7/library/stdtypes.html#frozenset) 。set 类型是可变类型——可使用 `add()` 和 `remove()` 等方法来更改其内容。由于 set 是可变类型，因此 set 对象没有哈希值，且不能用作字典的键，也不能用作其它 set 对象的元素。frozenset 类型是不可变类型，并且可哈希——frozenset 对象在创建后不能被改变；因此 frozenset 对象可用作字典的键值或是其它 set 对象的元素。

## 1. 构建集合(set, frozenset)

可通过以下几种方式来构建集合(set, frozenset)：

- 使用一对花括号，并在其中填充以逗号分割的项 - 可构建非空 set，但不能构建 frozenset，例如 `{'jack', 'sjoerd'}` , `{*[1,2,3]}`

- 使用集合解析(*comprehension*) - 可构建非空 set，但不能构建 frozenset，例如

  ```python
  {x for x in 'abracadabra' if x not in 'abc'}
  #> {'d', 'r'}
  ```

- 使用类型构造器(*constructor*) - 可构建 set 或 frozenset，例如 `set()` , `set(iterable)` ,  `frozenset()` , `frozenset(iterable)`

注意：`{}` 将构造一个空字典，并不会构建空集合。

🔨 *class* set([*iterable*])

🔨 *class* frozenset([*iterable*])

构造器 `set()` 和 `frozenset()` 拥有相同的工作方式，可分为以下两种情况：

- 如果未指定 *iterable*，将构建一个空 set (或 frozenset)对象：

  ```python
  set(),frozenset()
  #> (set(), frozenset())
  ```

- 如果给定了 *iterable* 参数，则会用 *iterable* 中的元素构建一个 set (或 frozenset)对象。*iterable* 中的元素必须都是可哈希对象，`set()` (或 `frozenset()`) 会自动剔除 *iterable* 中的重复项。如果想构建一个内含集合(*set*)对象的 set，内层的集合必须是 frozenset 对象。

  ```python
  set([1,2,2,3]) #> {1, 2, 3}
  set('abracadabra') #> {'a', 'b', 'c', 'd', 'r'}
  frozenset([1,2,2,3]) #> frozenset({1, 2, 3})
  ```

## 2. 支持的操作

set 和 frozenset 实例支持以下操作：

- `len(s)` - 返回集合 *s* 中元素的个数，也称集合 *s* 的势(*cardinality*)

- `x in s` - Test *x* for membership in *s*.

- `x not in s` - Test *x* for non-membership in *s*.

- `isdisjoint`(*other*) - 如果集合与 *other* 互斥(*disjoint*)，即集合与 *other* 的交集(intersection)为空，则返回 `True` 

  ```python
  a = {1,2,3}
  assert a.isdisjoint([4,5,6]) is True
  assert a.isdisjoint({4,5}) is True
  ```

- `issubset`(*other*) 或 `set <= other` - 测试集合是否是 *other* 的子集。

  Test whether every element in the set is in *other*.

- `set < other` - 测试集合是否是 *other* 的真子集。

  Test whether the set is a proper subset of *other*, that is, `set <= other and set !=other`.

- `issuperset`(*other*) 或 `set >= other` - 测试 *other* 是否是集合的子集。

  Test whether every element in *other* is in the set.

- `set > other`  - 测试 *other* 是否是集合的真子集。

  Test whether the set is a proper superset of *other*, that is, `set >= other and set !=other`.

- `union`(**others*) 或 `set | other | ...` - 并集

  Return a new set with elements from the set and all others.

- `intersection`(**others*) 或 `set & other & ...` - 交集

  Return a new set with elements common to the set and all others.

- `difference`(**others*) 或 `set - other - ...` - 差集

  Return a new set with elements in the set that are not in the others.

- `symmetric_difference`(*other*) 或 `set ^ other` - 对称差集

  Return a new set with elements in either the set or *other* but not both.

- `copy`()

  Return a new set with a shallow copy of *s*.

任何可迭代对象均可用作以下方法的参数，但这些方法对应的运算符版本只能使用集合作为操作数：

- `union()`, `intersection()`, `difference()`, `symmetric_difference()`
- `issubset()`, `issuperset()` 

使用以上方法可以避免像 `set('abc') & 'cbs'` 这样的错误，并且 `set('abc').intersection('cbs')` 也更加易读。

set 和 frozenset 均支持集合间的比较操作： Two sets are equal if and only if every element of each set is contained in the other (each is a subset of the other). A set is less than another set if and only if the first set is a proper subset of the second set (is a subset, but is not equal). A set is greater than another set if and only if the first set is a proper superset of the second set (is a superset, but is not equal).

set 实例和 frozenset 实例间的比较操作是基于所含成员进行的，例如：

```python
set('abc') == frozenset('abc') #> True
set('abc') in set([frozenset('abc')]) #> Ture
```

子集(*subset*)和相等比较不能被推广到排序函数









