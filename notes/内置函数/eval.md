# eval

🔨 eval(*expression*, *globals=None*, *locals=None*)

**Eval**uate the given *expression* in the context of *globals* and *locals*.

各参数含义如下：

- *expression* - 必选参数，有以下两种情况：

  - 可以是一个字符串，其内容是 Python 表达式，但不能是 Python 语句——关于表达式和语句的区别，详见笔记『表达式和运算符.md』。`eval()` 会将 *expression* 当作 Python 表达式进行解析和计算，并会使用 *globals* 和 *locals* 作为全局和本地命名空间。当 *expression* 中存在语法错误时，`eval()` 会抛出异常。

    ```python
    >>> eval('1+2+3+4')
    10
    >>> eval("{1: 'a', 2: 'b'}")
    {1: 'a', 2: 'b'}
    >>> eval("[x for x in range(10)]")
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # 在导入相应模块后，eval一样可以执行模块中的对象
    >>> import sys
    >>> eval("sys.path")
    ['', 'C:\\Python37\\Lib\\idlelib', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
    ```

  - 还可以是由 `compile()` 函数创建的 code 对象。在创建 code 对象时，如果将 *mode* 设为  `'exec'`，那么 `eval()` 的返回值将是 `None`。

- *globals* - 可选参数，表示全局变量表，必须是一个字典对象，默认值是调用 `eval()` 时的全局变量表。如果仅提供 *globals*，但不提供 *locals*，则默认 *locals* 与 *globals* 相同。

  如果提供的 *globals* 字典中不包含 `__builtins__` 键，则会在解析 *expression* 之前将 `'__builtins__': <module 'builtins' (built-in)>` 插入到 *globals* 中。这意味着 *expression* 通常具有对标准模块 [`builtins`](https://docs.python.org/3.7/library/builtins.html#module-builtins) 的全部访问权限，并且在受限制的环境中被传播。

  ```python
  >>> g = {}
  >>> g.keys()
  dict_keys([])
  # 由于会在解析expression之前向d中插入'__builtins__': 'builtins'
  # 所以可以在expression中直接使用内置函数
  >>> eval('print(1024)',g)
  1024
  # g中被添加了__builtins__键
  >>> g.keys()
  dict_keys(['__builtins__'])
  ```

  还可以通过 `__builtins__` 属性控制内置函数的可用性：

  ```python
  import builtins
  g = dict(__builtins__={'print': builtins.print})
  # 此时，只能使用print函数
  eval('print(999)', g)
  ```

- *locals* - 可选参数，表示局部变量表，可以是任何映射对象，默认值是调用 `eval()` 时的局部变量表。如果仅提供 *globals*，但不提供 *locals*，则默认 *locals* 与 *globals* 相同。

示例 - 演示 *globals* 和 *locals*：

```python
def func():
    y = 200
    print(eval('x + y'))
    print(eval('x + y', {'x': 10, 'y': 20}))
    print(eval('x + y', {
        'x': 10,
        'y': 20
    }, {
        'y': 2,
    }))
func()
'''Out:
300
30
12
'''
```

内置函数 `globals() ` 会返回当前全局字典，`locals()` 会返回当前本地字典，在向 `eval()` 或 `exec()` 传递参数时，可能会用到 `globals()` 和 `locals()`。在模块级别， `globals() ` 和 `locals()` 都会返回全局字典。

提示：`eval()` 仅支持执行表达式，但 `exec()` 函数支持动态执行语句。 

See [`ast.literal_eval()`](https://docs.python.org/3.7/library/ast.html#ast.literal_eval) for a function that can safely evaluate strings with expressions containing only literals.