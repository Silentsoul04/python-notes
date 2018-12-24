# round

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

🔨 round(*number*[, *ndigits*])

该函数用于对 *number* 进行舍入，*ndigits* 用于设置精度。

*ndigits* 可以是任意整数值(正数、0、负数均可)。当 *ndigits* 被省略(或值为 `None`)时，将返回距 *number* 最近的整数；当传入 *ndigits* 参数时，将返回与 *number* 同类型的值。

```python
# 注意观察返回值类型的类型
round(1.4), round(1.5) #> (1, 2)
round(1.4,0), round(1.5,0) #> (1.0, 2.0)
```

对于支持 `round()` 的内置类型，舍入结果是距离 *number* 最近的某个 $10^{-ndigits}$ 的倍数。

```python
# 当ndigits=1时，舍入结果应是pow(10,-1)=0.1的倍数，且是最接近number的某个0.1的倍数
round(0.24,1), round(-0.24,1)
#> (0.2, -0.2)

# 如果ndigits<1，便可对整数部分进行舍入
round(1024.61,-1),round(1024.61,-4),round(1024.61,-10)
#> (1020.0, 0.0, 0.0)
round(1024,-1),round(1024,-4),round(1024,-6)
#> (1020, 0, 0)
```

如果存在两个与 *number* 距离相等的 $10^{-ndigits}$ 的倍数，则会向偶数方向进行舍入。

```python
# 当ndigits=0时，舍入结果应是pow(10,0)的倍数，且是最接近number的的某个1的倍数
# 与0.5的距离相等的数有0和1，此时向偶数方向舍入，结果为0
# 与0.5的距离相等的数有0和-1，此时向偶数方向舍入，结果为0
round(0.5,0), round(-0.5,0) #> (0.0, -0.0)
# 与1.5的距离相等的数有1和2，此时向偶数方向舍入，结果为2
# 与-1.5的距离相等的数有-1和-2，此时向偶数方向舍入，结果为-2
round(1.5,0), round(-1.5,0) #> (2.0, -2.0)
# 与2.5的距离相等的数有2和3，此时向偶数方向舍入，结果为2
# 与-2.5的距离相等的数有-2和-3，此时向偶数方向舍入，结果为-2
round(2.5,0), round(-2.5,0) #> (2.0, -2.0)
```

在进行舍入时，还应考虑到浮点运算存在的限制：十进制数的小数部分大多不能使用浮点数精确表示(可阅读 [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3.7/tutorial/floatingpoint.html#tut-fp-issues))。比如在下面这个示例中，实际上浮点数 `2.675` 离 `2.67` 更近，因此舍入结果是 `2.67` 而不是我们预期中的 `2.68`。

```python
# 当ndigits=2时，舍入结果应是pow(10,-2)的倍数，且是最接近number的某个0.01的倍数
# 但浮点数并不能准确表示十进制小数，实际上2.675更接近2.67
format(2.675,'.20'),round(2.675, 2)
#> ('2.6749999999999998224', 2.67)

# 当ndigits=1时，舍入结果应是pow(10,-1)的倍数，且是最接近number的某个0.1的倍数
# 但浮点数并不能准确表示十进制小数，实际上0.15更接近0.1，-0.15更接近-0.1
format(0.15,'.20'),round(0.15,1), round(-0.15,1)
#> ('0.14999999999999999445', 0.1, -0.1)
# 同理，浮点数并不能准确表示十进制小数，实际上0.35更接近0.3，-0.35更接近-0.3
format(0.35,'.20'),round(0.35,1), round(-0.35,1)
#> ('0.3499999999999999778', 0.3, -0.3)

# 0.25可被精确表示，0.25与0.2和0.3距离相等，此时向偶数方向舍入，结果为0.2
# -0.25可被精确表示，-0.25与-0.2和0-.3距离相等，此时向偶数方向舍入，结果为-0.2
format(0.25,'.20'),round(0.25,1), round(-0.25,1)
#> ('0.25', 0.2, -0.2)
```

参考：[python中关于round函数的小坑](https://www.cnblogs.com/anpengapple/p/6507271.html)

## \_\_round\_\_

对于一般的 Python `number` 对象，`round` 函数会委托 `number.__round__` 完成舍入：

```python
class Foo:
    def __round__(self):
        return 61
round(Foo()) #> 61
```

还可阅读 [`object.__round__(self[, ndigits])`](https://docs.python.org/3.7/reference/datamodel.html#object.__round__)

## Py2 vs. Py3

### 返回值的类型

在 Py2 中，如果省略 *ndigits* 参数，则会默认 `ndigits=0`。无论是否传入 *ndigits*，结果始终是浮点数。

```python
# in Py2
round(1.4), round(10,2)
#> (1.0, 10.0)
```

在 Py3 中，如果省略 *ndigits* 参数，则会返回距 *number* 最近的整数；如果传入 *ndigits* 参数，则返回与 *number* 同类型的值。

```python
# in Py3
round(1.4), round(1.4,0), round(10,2)
#> (1, 1.0, 10)
```

### 舍入方向

在 Py2 中，如果存在两个与 *number* 距离相等的 $10^{-ndigits}$ 的倍数，则会向远离 0 的方向进行舍入。

```python
round(0.5,0), round(-0.5,0) #> (1.0, -1.0)
round(1.5,0), round(-1.5,0) #> (2.0, -2.0)
round(2.5,0), round(-2.5,0) #> (3.0, -3.0)
```

在 Py3 中，如果存在两个与 *number* 距离相等的 $10^{-ndigits}$ 的倍数，则会向偶数方向进行舍入。

```python
round(0.5,0), round(-0.5,0) #> (0.0, -0.0)
round(1.5,0), round(-1.5,0) #> (2.0, -2.0)
round(2.5,0), round(-2.5,0) #> (2.0, -2.0)
```

