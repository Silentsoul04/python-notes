# sorted

🔨sorted(*iterable*, \*, *key=None*, *reverse=False*)

sorted 函数会对 *iterable* 对象执行排序操作，并返回一个内含排序结果的新列表。

各参数含义如下：

- *iterable* : 一个可迭代对象
- *key* : 用于引入一个**单参数**的**可调用对象**(如 `key=str.lower`)，该对象被用于提取 *iterable* 中各个元素的比较键(*comparison key*)，并以比较键的顺序作为排序依据。如果保持默认值 `None`，则会直接比较 *iterable* 中的各个元素。
- *reverse* : 一个布尔值，用于控制排列顺序。默认值 `False` 表示以升序排列 *iterable* 中的元素；`True` 则表示以降序排列 *iterable* 中的元素。

一些简单的列子：

```python
# 直接比较iterable中的各个元素，升序排列
>>> sorted([36, 5, -12, 9, -21])
[-21, -12, 5, 9, 36]

# 使用iterable中各元素的绝对值进行排序
>>> sorted([36, 5, -12, 9, -21], key=abs)
[5, 9, -12, -21, 36]

# 降序排列
>>> sorted([36, 5, -12, 9, -21], reverse=True)
[36, 9, 5, -12, -21]

# 字符串默认按ASCII排序，因此大小写会影响排序结果
>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
['Credit', 'Zoo', 'about', 'bob']

# 排序时忽略大小写
>>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
['about', 'bob', 'Credit', 'Zoo']
```

**扩展阅读**：["Sorting HOW TO"](https://docs.python.org/3.7/howto/sorting.html#sortinghowto) 作为一个排序教程提供了更多参考示例。

## 稳定性

稳定性排序(stable-sort)算法在对相同元素进行排序时，不会改变这些元素在排序之前的相对位置。比如当我们按照牌面值进行排序时：在稳定性排序中，红心 5 和黑桃 5 的前后顺序保持不变；而在非稳定性算法中，两者的顺序则可能会发生改变。

![Stable sort ](sorted.assets/Stable sort .png)

sorted 函数采用稳定性排序算法，可以看到花色顺序不会改变：

```python
>>> cards = [(7,"黑桃"), (5,"红桃"), (2,"红桃"), (5,"黑桃")]
>>> sorted(cards, key=lambda item:item[0])
[(2, '红桃'), (5, '红桃'), (5, '黑桃'), (7, '黑桃')]
```

当数据需要连续经历多个排序步骤时(比如先按部门排序，再按工资等级排序)，稳定性排序算法会非常实用，因为它不会改变上一步已排列好的顺序。

```python
>>> # 先按牌面值排序，再按照花色排序
>>> cards = [(6, "黑桃"), (5, "红桃"), (4, "方片"), (2, "梅花"),
         (7, "黑桃"), (8, "红桃"), (3, "方片"), (1, "梅花")]
>>> first = sorted(cards, key=lambda item: item[0])
>>> first
[(1, '梅花'), (2, '梅花'), (3, '方片'), (4, '方片'), (5, '红桃'), (6, '黑桃'), (7, '黑桃'), (8, '红桃')]
>>> second = sorted(first, key=lambda item: item[1])
>>> second
[(3, '方片'), (4, '方片'), (1, '梅花'), (2, '梅花'), (5, '红桃'), (8, '红桃'), (6, '黑桃'), (7, '黑桃')]
```

## functools.cmp_to_key

在 Py2.x 版本中 sorted 函数的语法如下：

```python
sorted (iterable[, cmp[, key[, reverse]]])
```

可以看到，Py2.x 中的 sorted 函数比 Py3.0 多了一个 *cmp* 参数。*cmp* 是一个可选参数，用于引入自定义比较函数。比较函数需要接受两个参数，并以正数、零和负数来表示两个参数的比较结果。例如：

```python
def numeric_compare(x, y):
    """
    返回正数，表示x大于y；
    返回0，表示x等于y；
    返回负数，表示x小于y。
    """
    return x - y
```

在 Py2.x 中，我们可以通过 *cmp* 参数自定义排序函数：

```python
>>> def numeric_compare(x, y):
...     return x - y
>>> sorted([5, 2, 4, 1, 3], cmp=numeric_compare) 
[1, 2, 3, 4, 5]
```

如果需要翻转上述排序顺序的话，只需稍作修改即可：

```python
>>> def reverse_numeric(x, y):
...     return y - x
>>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric) 
[5, 4, 3, 2, 1]
```

但是，sorted 函数在 Py3.0 中该参数已移除了 *cmp* 参数。当我们将代码从 Py2.x 移植到 Py3.x 时，便需要将旧式比较函数(comparison function)转换为键函数([key function](https://docs.python.org/3.7/glossary.html#term-key-function))。为了满足该需求，我们可以使用 `functools.cmp_to_key()` 函数。

[cmp_to_key](https://docs.python.org/3.7/library/functools.html#functools.cmp_to_key) 函数用于将旧式比较函数(comparison function)转换为键函数([key function](https://docs.python.org/3.7/glossary.html#term-key-function))，在 Py3.2 中被引入。使用方式如下：

```python
>>> # in Python 3
>>> def reverse_numeric(x, y):
...     return y - x
>>> sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
[5, 4, 3, 2, 1]
```

cmp_to_key 函数的源代码如下：

```python
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
```

