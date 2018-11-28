# open

🔨 open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

该函数用于打开 *file* 并返回相应的 I/O 对象「也称文件对象([*file object*](https://docs.python.org/3.7/glossary.html#term-file-object))」，如果打开失败则会抛出 [`OSError`](https://docs.python.org/3.7/library/exceptions.html#OSError)。

[`io.open()`](https://docs.python.org/3.7/library/io.html#io.open) 其实是 `open()` 函数的别名，而 [`os.open`](https://docs.python.org/3.7/library/os.html#os.open) 被用于创建文件描述符。新创建的文件和文件描述符都是不可继承的([non-inheritable](https://docs.python.org/3.7/library/os.html#fd-inheritance))——文件描述符具有"inheritable"标志，该标志指示子进程是否可以继承该文件描述符(可阅读 [Inheritance of File Descriptors](https://docs.python.org/3.7/library/os.html#fd-inheritance) 和 [`os.open`](https://docs.python.org/3.7/library/os.html#os.open)，以了解更多信息)

## I/O 对象

`open()` 函数返回的 I/O 对象的类型取决于 *mode* 参数：

- 当以 text 模式(`'w'`, `'r'`, `'wt'`, `'rt'`, etc.)打开某个文件时，将返回 [`io.TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 的子类( [`io.TextIOWrapper`](https://docs.python.org/3.7/library/io.html#io.TextIOWrapper))的实例

  ```python
  with open('a_file.txt', 'r') as fin:
      print(type(fin)) # Out:<class '_io.TextIOWrapper'>
  with open('a_file.txt', 'w') as fin:
      print(type(fin)) # Out:<class '_io.TextIOWrapper'>
  with open('a_file.txt', 'r+') as fin:
      print(type(fin)) # Out:<class '_io.TextIOWrapper'>
  ```

- 当以 binary 模式打开某个启用 *buffering* 的文件时，将返回 [`io.BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) 的子类的实例，具体的子类如下：

  - 在 read binary 模式下，将返回 [`io.BufferedReader`](https://docs.python.org/3.7/library/io.html#io.BufferedReader) 类的实例
  - 在 write(or append) binary 模式下，将返回 [`io.BufferedWriter`](https://docs.python.org/3.7/library/io.html#io.BufferedWriter) 类的实例
  - 在 read/write binary 模式下，将返回 [`io.BufferedRandom`](https://docs.python.org/3.7/library/io.html#io.BufferedRandom) 类的实例

  ```python
  # 注意,已启用buffering,详见之后的buffering小节
  with open('a_file.txt', 'rb') as fin:
      print(type(fin)) # Out:<class '_io.BufferedReader'>
  with open('a_file.txt', 'wb') as fin:
      print(type(fin)) # Out:<class '_io.BufferedWriter'>
  with open('a_file.txt', 'r+b') as fin:
      print(type(fin)) # Out:<class '_io.BufferedRandom'>
  ```

- 当禁用 *buffering* 时，将返回原始流(*raw stream*)，即 [`io.RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase) 的子类([`io.FileIO`](https://docs.python.org/3.7/library/io.html#io.FileIO))的实例

  ```python
  # 注意,buffering=0便会禁用缓冲器,详见之后的buffering小节
  with open('a_file.txt', 'rb', 0) as fin:
      print(type(fin)) # Out:<class '_io.FileIO'>
  with open('a_file.txt', 'wb', 0) as fin:
      print(type(fin)) # Out:<class '_io.FileIO'>
  with open('a_file.txt', 'r+b', 0) as fin:
      print(type(fin)) # Out:<class '_io.FileIO'>
  ```

我们可以在上述类的文档中查看这些 I/O 对象中包含的属性。

### I/O 类的继承链

[`io`](https://docs.python.org/3.7/library/io.html#module-io) 模块中，各个 I/O 类间的继承关系如下：

```
IOBase
|--RawIOBase
	|--FileIO
|--BufferedIOBase
	|--BytesIO
	|--BufferedReader
	|--BufferedWriter
	|--BufferedRandom
	|--BufferedRWPair
|--TextIOBase
	|--TextIOWrapper
	|--StringIO
```

### StringIO

🔨 *class* io.StringIO(*initial_value=''*, *newline='\n'*)

该构造器会在内存中创建一个 text I/O 流。在 [`StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO) 类的实例上调用 `close()` 方法时，将丢弃文本缓冲区中的数据。

参数说明：

- *initial_value* 用于设置缓冲区的初始值，但即便置了初始值，在流中仍会以 0 偏移量为起点

- *newline* 用于设置是否启用换行符转换，其工作方式与 [`TextIOWrapper`](https://docs.python.org/3.7/library/io.html#io.TextIOWrapper) 的同名参数一致，具体行为可参考本笔记的「参数说明.*newline*」小节

在 `StringIO` 中，除包含 [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 及其父类中的方法之外，还提供下述方法：

- getvalue() - 返回一个包含缓冲区中全部内容的 str 对象。换行符的处理方式依赖于 *newline* 参数，具体行为可参考本笔记的「参数说明.*newline*」小节

示例：

```python
import io

output = io.StringIO()
output.write('First line.\n')
print('Second line.', file=output)

# Retrieve file contents -- this will be
# 'First line.\nSecond line.\n'
contents = output.getvalue()

# Close object and discard memory buffer --
# .getvalue() will now raise an exception.
output.close() # 使用完毕后，同样需要关闭
```

### BytesIO

🔨 *class* io.BytesIO([*initial_bytes*])

该构造器会在内存中创建一个 bytes I/O 流。[`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) 

该类继承自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase)，其构造器会在内存中创建一个 bytes I/O 流。在 [`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) 类的实例上调用 `close()` 方法时，将丢弃缓冲区中的数据。

*initial_bytes* 用于设置缓冲区的初始值，但即便置了初始值，在流中仍会以 0 偏移量为起点

A stream implementation using an in-memory bytes buffer. It inherits [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase). The buffer is discarded when the [`close()`](https://docs.python.org/3.7/library/io.html#io.IOBase.close) method is called.

The optional argument *initial_bytes* is a [bytes-like object](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) that contains initial data.

[`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) provides or overrides these methods in addition to those from [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase)and [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase):





```
>>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())
b'\xe4\xb8\xad\xe6\x96\x87'

>>> f.write('中文')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-25-37d03170c78b> in <module>()
----> 1 f.write('中文')

TypeError: a bytes-like object is required, not 'str'
```

注意，写入的对象是进过 UTF-8 编码的 bytes。
如果直接写入 `str` 会抛出 TypeError 。

读取方式和文件相同：

```
>>> from io import BytesIO
>>> f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
>>> f.read()
b'\xe4\xb8\xad\xe6\x96\x87'
```



## 参数说明

### *file*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*file* 用于设置需要打开的文件，有以下两种形式：

- 可以是一个表示**文件系统路径**(绝对路径或相对路径均可)的对象，即 [path-like](https://docs.python.org/3.7/glossary.html#term-path-like-object) 对象。该对象可以是文本字符串或 byte 字符串，也可是实现了 [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) 协议的对象。

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  fin = open(b'somefile.txt')
  print(fin.read())
  print(fin.fileno())  # fileno()会返回文件描述符
  fin.close()
  """Out:
  first line
  second line
  3
  """
  ```

- 还可以是一个**整型文件描述符**(*integer file descriptor*)，该描述符代表一个被打包(*wrapped*)的文件，可通过 [`os.open`](https://docs.python.org/3.7/library/os.html#os.open) 创建。如果给出了文件描述符，那么当我们关闭 `open()` 返回的 I/O 对象时，该文件描述符也将被关闭，除非将 *closefd* 设置为 `False`。

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  import os
  # 使用底层IO打开一个文件，并返回其文件描述符(integer)
  fd = os.open('somefile.txt', os.O_RDONLY)
  print("文件描述符的值是 {0}，类型是 {1}".format(fd, type(fd)))
  f = open(fd, 'r')
  print(f.read())
  f.close()
  # f被关闭后，对应的文件描述符也将被关闭，
  # 但文件描述符被关闭后不能再次被打开
  f = open(fd, 'r')
  """Out:
  文件描述符的值是 3，类型是 <class 'int'>
  first line
  second line
  Traceback (most recent call last):
    File "c:/Users/iwhal/Desktop/内置函数/BI_open.py", line 13, in <module>
      f = open(fd, 'r')
  OSError: [WinError 6] 句柄无效。
  """
  ```

  如果需要再次打开文件描述，则需将 *closefd* 参数设置为 `False`：

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  import os
  fd = os.open('somefile.txt', os.O_RDONLY)
  # 将closefd设置为False
  f = open(fd, 'r', closefd=False)
  f.close()
  f = open(fd, 'r')
  print(f.read())
  """Out:
  first line
  second line
  """
  ```

  **扩展阅读**: 5.18 将文件描述符包装成文件对象 - Python Cookbook

### *mode*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*mode* 用于设定文件的打开模式，默认值是 `'rt'`，有如下可用模式：

| Character | Meaning                                                      |
| --------- | ------------------------------------------------------------ |
| `'r'`     | open for reading (default)                                   |
| `'w'`     | open for writing , truncating the file first <br />如果文件已存在，则会清空现有内容；如果文件不存在，则会创建该文件 |
| `'x'`     | open for exclusive creation, failing if the file already exists<br />如果文件不存在，则会创建该文件，并默认以 `'wt'` 打开；如果文件已存在，则会抛出 `FileExistsError` |
| `'a'`     | open for writing, appending to the end of the file if it exists<br />在某些 Unix 系统中，这意味着所有写入都会被附加到文件的末尾，并且无视 seek 位置 |
| `'b'`     | binary mode (以字节形式读写数据，用于不包含文本的所有文件)<br />在读写 raw bytes 时，需使用 binary 模式，并且不需要指定编码方式 |
| `'t'`     | text mode (default)<br />在文本模式下，如果未指定 *encoding*，则依赖平台的编码方式，即调用`locale.getpreferredencoding(False)` 来获取当前本地编码方式。 |
| `'+'`     | open a disk file for updating (reading and writing)          |
| `'U'`     | [universal newlines](https://docs.python.org/3.7/glossary.html#term-universal-newlines) mode (deprecated), Use newline to control universal newlines mode.<br />`'U'` 模式已被弃用，在未来的 Python 版本中将会引发异常。该模式在 Python 3 中无效。 |

对于二进制(*binary*)读写访问，`'w+b'` 会截断文件至 0 字节，但 `'r+b'` 不会截断文件，这两种模式在流中都以 0 偏移量为起点。

如 `io` 模块中[概述](https://docs.python.org/3.7/library/io.html#overview)部分所言，Python 会区分 binary I/O 和 text I/O： (即使底层操作系统并不会区分这两者，Python 仍然会进行区别)

- 以 binary 模式( `'b'` )打开文件后：在读取文件时，会将文件中的内容以 `bytes` 对象返回，不会进行任何解码操作；在写入文件时，会将 `bytes` 对象直接写入文件，不会进行任何编码操作。在使用 binary 模式时，需保持 `encoding=None`。

- 以 text 模式( `'t'` )打开文件后：在读取文件时，会先对读取到的字节进行解码，再以 `str` 对象返回解码后的内容；在写入文件时，会先对被写入的 `str` 对象进行编码，再将编码得到的字节写入文件。在 text 模式下，如果未指定 *encoding*，则依赖平台的编码方案，即调用`locale.getpreferredencoding(False)` 来获取当前本地编码方案。

  在 Windows 下，默认的编码方式是 cp936：

  ```python
  >>> import locale
  >>> locale.getpreferredencoding(False)
  'cp936'
  ```

注意：Python 不依赖于底层操作系统定义的文本文件的概念；所有处理都由 Python 本身完成，因此与平台无关。

示例 - 展示 binary 模式和 text 模式的区别

```python
with open('a_file.txt', 'r+b') as fin:
    # 在binary模式下会直接向文件写入字节
    fin.write(b'orca_j35 ' + bytes('鲸', 'utf8'))
    fin.seek(0)
    # 读取之前写入的字节
    print(fin.read())

with open('a_file.txt', 'r+', encoding='utf8') as fin:
    # 在text模式下，会先对读取到的字节进行解码，再以字符串对象返回解码后的内容
    print(fin.read())
"""Out:
b'orca_j35 \xe9\xb2\xb8'
orca_j35 鲸
"""
```

### *buffering*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*buffering* 用于设置缓冲策略(*buffering policy*)，可以是以下整数值：

- 0 to switch buffering off (only allowed in binary mode, raise ValueError in text mode) - 会立即把内容输出至流文件，不会进行缓存

  ```python
  >>> f=open('test.txt', 'w+b')
  # 此时test.txt中没有何内容
  >>> f.write(b'a')
  1
  # 此时test.txt中仍然没有何内容，会先将输出至文件对象的数据进行缓存
  # 待文件对象关闭时，才会将缓存的数据写入文件对象
  >>> f.close()
  # 此时test.txt中出现'a'
  
  >>> f=open('test.txt', 'w+b', 0)
  # 此时test.txt中没有何内容
  >>> f.write(b'a')
  1
  # 此时test.txt中出现'a'
  # buffering=0时不会缓存数据，会立即把内容输出到流文件,不用等文件对象关闭后再写入
  >>> f.close()
  
  # buffering=0不能用于text模式，否则会抛出异常
  >>> f=open('test.txt', 'wt', 0)
  Traceback (most recent call last):
    File "<pyshell#15>", line 1, in <module>
      f=open('test.txt', 'wt', 0)
  ValueError: can't have unbuffered text I/O
  ```

- 1 to select line buffering (only usable in text mode) - 每次缓存一行数据，行分隔符由 *newline* 参数决定。

  ```python
  >>> f=open('test.txt', 'w+t', 1)
  # 此时test.txt中没有何内容
  >>> f.write('abc')
  3
  # 此时test.txt中仍没有何内容
  >>> f.write('cde\n')
  4
  # 此时test.txt中出现'abccde'
  >>> f.write('efg\r')
  4
  # 此时test.txt中出现'efg'
  
  # buffering=1对binary模式无效
  >>> f=open('test.txt', 'w+b', 1)
  # 此时test.txt中没有何内容
  >>> f=open('test.txt', 'w+b', 1)
  >>> f.write(b'abc\n')
  4
  >>> f.write(b'def\r')
  4
  # 此时test.txt中仍没有何内容
  >>> f.close()
  # 此时test.txt中出现'abc'和'def'
  ```

- an integer > 1 to indicate the size in bytes of a fixed-size chunk buffer - 将缓冲器设置为给定的尺寸，当缓冲器中数据的尺寸大于该长度时，便会向文件对象写入一次数据。似乎只对 binary 模式有效，对 text 模式无效。

  ```python
  >>> f=open('test.txt', 'w+b', 2)
  >>> f.write(b'ab')
  2
  # 此时test.txt中没有何内容
  >>> f.write(b'c')
  1
  # 此时test.txt中出现 'ab'，但没有'c'
  >>> f.close()
  # 此时test.txt中出现 'ab'和'c'
  ```

如果没有给出 *buffering* 参数，默认缓冲策略的工作方式如下：

- Binary files are buffered in fixed-size chunks; the size of the buffer is chosen using a heuristic trying to determine the underlying device’s “block size” and falling back on [`io.DEFAULT_BUFFER_SIZE`](https://docs.python.org/3.7/library/io.html#io.DEFAULT_BUFFER_SIZE). On many systems, the buffer will typically be 4096 or 8192 bytes long. 

  即，二进制文件会以固定尺寸的缓冲器块进行缓存

- “Interactive” text files (files for which [`isatty()`](https://docs.python.org/3.7/library/io.html#io.IOBase.isatty) returns `True`) use line buffering. Other text files use the policy described above for binary files.

### *encoding*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*encoding* 用于设置字符编码方案，在编码(或解码)文件内容时便会使用该编码方案，该参数只能用于 text 模式。在 [`codecs`](https://docs.python.org/3.7/library/codecs.html#module-codecs) 模块中列举了 Python 支持的编码方案。 

当 `encoding=None` 时，编码方案取决于当前平台，会通过 `locale.getpreferredencoding(False)` 来获取当前本地编码方案。在 Windows 下，默认的编码方式是 cp936：

```python
>>> import locale
>>> locale.getpreferredencoding(False)
'cp936'
```

### *errors*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*errors* 用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，当出现编码(或解码)错误时，便会使用此错误处理方案，该参数不能用于 binary 模式。

*errors* 的实参值可以是 [Error Handlers](https://docs.python.org/3.7/library/codecs.html#error-handlers) 中列出的标准错误处理方案；也可以是已在 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册过的任何错误处理方案的名称。

标准错误处理方案包括：

- `'strict'` to raise a [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) exception if there is an encoding error. The default value of `None` has the same effect.
- `'ignore'` ignores errors. Note that ignoring encoding errors can lead to data loss.
- `'replace'` causes a replacement marker (such as `'?'`) to be inserted where there is malformed data.
- `'surrogateescape'` will represent any incorrect bytes as code points in the Unicode Private Use Area ranging from U+DC80 to U+DCFF. These private code points will then be turned back into the same bytes when the `surrogateescape` error handler is used when writing data. This is useful for processing files in an unknown encoding.
- `'xmlcharrefreplace'` is only supported when writing to a file. Characters not supported by the encoding are replaced with the appropriate XML character reference `&#nnn;`.
- `'backslashreplace'` replaces malformed data by Python’s backslashed escape sequences.
- `'namereplace'` (also only supported when writing) replaces unsupported characters with `\N{...}` escape sequences.

还可阅读 `codecs.register` 的文档或是运行 `'help(codecs.Codec)'` ，来了解各种错误处理方案。

### *newline*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*newline* 用于控制通用换行符模式( `'U'` )的工作方式，只能用于 text 模式，其值可以是`None`、`''`、`'\n'`、`'\r'`、`'\r\n'`，具体工作方式如下：

- 从流中读取输入数据时：
  - 如果 `newline=None`，则会启用通用换行符模式。输入数据中的行分隔符可以是 `'\n'`、`'\r'` 或 `'\r\n'`，但在将数据返回给调用者之前，这三种换行符均会被转换为 `'\n'`。
  - 如果 `newline=''`，同样会启用通用换行符模式，但会将换行符原样返回给调用者，不会对换行符进行转换。
  - 如果 *newline* 是 `'\n'`、`'\r'`、`'\r\n'` 三者之一，则在读取数据时仅会将 *newline* 视作行分隔符，并且会将换行符原样返回给调用者，不会对换行符进行转换。
- 向流中写入输出数据时：
  - 如果 `newline=None`，则会将输出数据中所有的 `'\n'` 字符转换为系统默认的行分隔符(即，[`os.linesep`](https://docs.python.org/3.7/library/os.html#os.linesep))。

    ```python
    with open('a_file.txt', 'w+t', newline=None) as fin:
        fin.write('a_\r')
        fin.write('b_\n')
        fin.write('c_\r\n')
    '''a_file.txt中的内容如下：
    a_␍
    b_␍␊
    c_␍
    ␍␊
    '''
    ```

  - 如果 *newline* 是 `''` 或 `'\n'`，则会将输出数据中的行分隔符原样保留。

    ```python
    with open('a_file.txt', 'w+t', newline='') as fin:
        fin.write('a_\r')
        fin.write('b_\n')
        fin.write('c_\r\n')
    '''a_file.txt中的内容如下：
    a_␍
    b_␊
    c_␍␊
    '''
    ```

  - 如果 *newline* 是 `'\r'` 或 `'\r\n'`，则会将输出数据中所有的 `'\n'` 字符装换为 *newline*。

    ```python
    with open('a_file.txt', 'w+t', newline='\r') as fin:
        fin.write('a_\r')
        fin.write('b_\n')
        fin.write('c_\r\n')
    '''a_file.txt中的内容如下：
    a_␍
    b_␍
    c_␍
    ␍
    '''
    with open('a_file.txt', 'w+t', newline='\r\n') as fin:
        fin.write('a_\r')
        fin.write('b_\n')
        fin.write('c_\r\n')
    '''a_file.txt中的内容如下：
    a_␍
    b_␍␊
    c_␍
    ␍␊
    '''
    ```

### *closefd*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

如果 `closefd=False` 并且 *file* 的值是文件描述符，当我们关闭 `open()` 返回的文件对象时，底层文件描述符依旧会保持打开状态。

如果 `closefd=True` 并且 *file* 的值是文件描述符，当我们关闭 `open()` 返回的文件对象时，底层文件描述符也将被关闭。

如果 *file* 的值是某个路径，那么 *closefd* 必须保持默认状态(`True`)，否则会抛出异常。

### *opener*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*opener* 用于设置自定义开启器(opener)。调用开启器( 即 `opener(file, flags)` )后，可获得文件对象的底层文件描述符。开启器的返回值必须是一个打开的文件描述符。`opener=os.open` 与 `opener=None` 的等效。

The following example uses the [dir_fd](https://docs.python.org/3.7/library/os.html#dir-fd) parameter of the [`os.open()`](https://docs.python.org/3.7/library/os.html#os.open) function to open a file relative to a given directory:

在下面这个示例中，将使用 [`os.open()`](https://docs.python.org/3.7/library/os.html#os.open) 函数的 [dir_fd](https://docs.python.org/3.7/library/os.html#dir-fd) 参数来打开相对于给定目录的文件：

```python
>>> import os
>>> dir_fd = os.open('somedir', os.O_RDONLY)
>>> def opener(path, flags):
...     return os.open(path, flags, dir_fd=dir_fd)
...
>>> with open('spamspam.txt', 'w', opener=opener) as f:
...     print('This will be written to somedir/spamspam.txt', file=f)
...
>>> os.close(dir_fd)  # don't leak a file descriptor
```



## 术语

### file object

An object exposing a file-oriented API (with methods such as `read()` or `write()`) to an underlying resource. Depending on the way it was created, a file object can mediate access to a real on-disk file or to another type of storage or communication device (for example standard input/output, in-memory buffers, sockets, pipes, etc.). File objects are also called *file-like objects* or *streams*.

There are actually three categories of file objects: raw [binary files](https://docs.python.org/3.7/glossary.html#term-binary-file), buffered [binary files](https://docs.python.org/3.7/glossary.html#term-binary-file)and [text files](https://docs.python.org/3.7/glossary.html#term-text-file). Their interfaces are defined in the [`io`](https://docs.python.org/3.7/library/io.html#module-io) module. The canonical way to create a file object is by using the [`open()`](https://docs.python.org/3.7/library/functions.html#open) function.

### file-like object

A synonym for [file object](https://docs.python.org/3.7/glossary.html#term-file-object).

### path-like object

An object representing a file system path. A path-like object is either a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes)object representing a path, or an object implementing the [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) protocol. An object that supports the [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) protocol can be converted to a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) file system path by calling the [`os.fspath()`](https://docs.python.org/3.7/library/os.html#os.fspath) function; [`os.fsdecode()`](https://docs.python.org/3.7/library/os.html#os.fsdecode) and [`os.fsencode()`](https://docs.python.org/3.7/library/os.html#os.fsencode) can be used to guarantee a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) result instead, respectively. Introduced by [**PEP 519**](https://www.python.org/dev/peps/pep-0519).

### text file

A [file object](https://docs.python.org/3.7/glossary.html#term-file-object) able to read and write [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) objects. Often, a text file actually accesses a byte-oriented datastream and handles the [text encoding](https://docs.python.org/3.7/glossary.html#term-text-encoding) automatically. Examples of text files are files opened in text mode (`'r'` or `'w'`), [`sys.stdin`](https://docs.python.org/3.7/library/sys.html#sys.stdin), [`sys.stdout`](https://docs.python.org/3.7/library/sys.html#sys.stdout), and instances of[`io.StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO).

See also [binary file](https://docs.python.org/3.7/glossary.html#term-binary-file) for a file object able to read and write [bytes-like objects](https://docs.python.org/3.7/glossary.html#term-bytes-like-object).

### text encoding

A codec which encodes Unicode strings to bytes.

### universal newlines

A manner of interpreting text streams in which all of the following are recognized as ending a line: the Unix end-of-line convention `'\n'`, the Windows convention `'\r\n'`, and the old Macintosh convention `'\r'`. See [**PEP 278**](https://www.python.org/dev/peps/pep-0278) and [**PEP 3116**](https://www.python.org/dev/peps/pep-3116), as well as[`bytes.splitlines()`](https://docs.python.org/3.7/library/stdtypes.html#bytes.splitlines) for an additional use.

