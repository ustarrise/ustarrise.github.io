---
title: python
typora-root-url: ..
date: 2023-09-06 19:30:10
tags:
---



## 命名规定：

以下是 Python 标识符的命名约定

- 类名以大写字母开头。所有其他标识符都以小写字母开头。
- 以单个前导下划线开头的标识符表示该标识符是私有的。
- 以两个前导下划线开头的标识符表示强私有标识符。
- 如果标识符也以两个尾随下划线结尾，则标识符是语言定义的特殊名称。

### **保留字**

以下列表显示了 Python 关键字。这些是保留字，您不能将它们用作常量或变量或任何其他标识符名称。所有 Python 关键字仅包含小写字母。

| 关键字   |         |        |
| :------- | :------ | :----- |
| and      | exec    | not    |
| assert   | finally | or     |
| break    | for     | pass   |
| class    | from    | print  |
| continue | global  | raise  |
| def      | if      | return |
| del      | import  | try    |
| elif     | in      | while  |
| else     | is      | with   |
| except   | lambda  | yield  |

### **行和缩进**

Python 不提供大括号来指示类和函数定义或流控制的代码块。代码块由行缩进表示，这是严格执行的。

缩进中的空格数是可变的，但块中的``所有语句``必须缩进相同的数量。例如

```python
if True:
   print "True"
else:
   print "False"
```

但是，以下块会产生错误

```
if True:
print "Answer"
print "True"
else:
print "Answer"
print "False"
```

因此，在 Python 中，所有以相同数量的空格缩进的连续行将形成一个块。

### **多行语句**

Python 中的语句通常以新行结束。但是，Python 确实允许使用行继续符 (\\) 来表示该行应该继续。例如

```
total = item_one + \
        item_two + \
        item_three
```

[]、{} 或 () 括号内包含的语句不需要使用行继续符。例如

```
days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday']\
```

## Python 有五种标准数据类型:

- Numbers
- String
- List
- Tuple
- Dictionary

#### **Python Numbers**

数字数据类型存储数值。当您为它们分配一个值时，就会创建数字对象。例如

```
var1 = 1
var2 = 10
```

您还可以使用 del 语句删除对数字对象的引用。del 语句的语法是

```
del var1[,var2[,var3[....,varN]]]]
```

您可以使用 del 语句删除单个对象或多个对象。例如

```
del var
del var_a, var_b
```

Python 支持四种不同的数字类型

- int（有符号整数）
- long（长整数，也可以用八进制和十六进制表示）
- float（浮点实数值）
- complex（复数）

##### 例子

以下是一些数字示例

| int    | long                  | float      | complex    |
| :----- | :-------------------- | :--------- | :--------- |
| 10     | 51924361L             | 0.0        | 3.14j      |
| 100    | -0x19323L             | 15.20      | 45.j       |
| -786   | 0122L                 | -21.9      | 9.322e-36j |
| 080    | 0xDEFABCECBDAECBFBAEl | 32.3+e18   | .876j      |
| -0490  | 535633629843L         | -90.       | -.6545+0J  |
| -0x260 | -052318172735L        | -32.54e100 | 3e+26J     |
| 0x69   | -4721885298529L       | 70.2-E12   | 4.53e-7j   |

- Python 允许您使用带有 long 的小写 l，但建议您只使用大写 L 以避免与数字 1 混淆。 Python 显示带有大写 L 的长整数。
- 复数由一对有序的实浮点数组成，用 x + yj 表示，其中 x 和 y 是实数，j 是虚数单位。

**Python字符串**

Python 中的字符串被标识为用引号表示的一组连续字符。Python 允许成对的单引号或双引号。可以使用切片运算符（[ ] 和 [:] ）获取字符串的子集，索引从字符串开头的 0 开始，最后从 -1 开始。

加号 (+) 是字符串连接运算符，星号 ( * ) 是重复运算符。例如 上述同样方法建立test.py文件，输入以下代码

```
#!/usr/bin/python

str = 'Hello World!'

print str          # Prints complete string
print str[0]       # Prints first character of the string
print str[2:5]     # Prints characters starting from 3rd to 5th
print str[2:]      # Prints string starting from 3rd character
print str * 2      # Prints string two times
print str + "TEST" # Prints concatenated string
```

保存并运行之后，可以得到以下结果

```
Hello World!
H
llo
llo World!
Hello World!Hello World!
Hello World!TEST
```

### **Python 列表**

列表是 Python 中最通用的复合数据类型。列表包含用逗号分隔并括在方括号 ([]) 中的项目。在某种程度上，列表类似于 C 中的数组。它们之间的一个区别是属于一个列表的所有项目可以是不同的数据类型。

可以使用切片运算符（[ ] 和 [:]）访问存储在列表中的值，索引从列表开头的 0 开始，并以它们的方式结束 -1。加号 (+) 是列表连接运算符，星号 ( * ) 是重复运算符。例如

```
#!/usr/bin/python

list = [ 'abcd', 786 , 2.23, 'john', 70.2 ]
tinylist = [123, 'john']

print list          # Prints complete list
print list[0]       # Prints first element of the list
print list[1:3]     # Prints elements starting from 2nd till 3rd 
print list[2:]      # Prints elements starting from 3rd element
print tinylist * 2  # Prints list two times
print list + tinylist # Prints concatenated lists
```

这会产生以下结果

```
['abcd', 786, 2.23, 'john', 70.2]
abcd
[786, 2.23]
[2.23, 'john', 70.2]
[123, 'john', 123, 'john']
['abcd', 786, 2.23, 'john', 70.2, 123, 'john']
```

### **Python元组**

元组是另一种类似于列表的序列数据类型。元组由多个以逗号分隔的值组成。然而，与列表不同的是，元组被括在括号内。

列表和元组之间的主要区别是： 列表括在方括号 ( [ ] ) 中并且它们的元素和大小可以更改，而元组括在括号 ( ( ) 中并且**不能**更新。元组可以被认为是``只读列表``。例如

```
#!/usr/bin/python

tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
tinytuple = (123, 'john')

print tuple               # Prints the complete tuple
print tuple[0]            # Prints first element of the tuple
print tuple[1:3]          # Prints elements of the tuple starting from 2nd till 3rd 
print tuple[2:]           # Prints elements of the tuple starting from 3rd element
print tinytuple * 2       # Prints the contents of the tuple twice
print tuple + tinytuple   # Prints concatenated tuples
```

这会产生以下结果

```
('abcd', 786, 2.23, 'john', 70.2)
abcd
(786, 2.23)
(2.23, 'john', 70.2)
(123, 'john', 123, 'john')
('abcd', 786, 2.23, 'john', 70.2, 123, 'john')
```

以下代码对元组无效，因为我们尝试更新元组，这是不允许的。列表可能出现类似情况

```
#!/usr/bin/python

tuple = ( 'abcd', 786 , 2.23, 'john', 70.2  )
list = [ 'abcd', 786 , 2.23, 'john', 70.2  ]
tuple[2] = 1000    # Invalid syntax with tuple
list[2] = 1000     # Valid syntax with list
```

### **Python字典**

Python 的字典是一种哈希表类型。它们的工作方式类似于 Perl 中的关联数组或散列，由键值对组成。字典键几乎可以是任何 Python 类型，但通常是数字或字符串。另一方面，值可以是任意的 Python 对象。

字典用{ }括起来，可以使用[ ]分配和访问值。例如

```
#!/usr/bin/python

dict = {}
dict['one'] = "This is one"
dict[2]     = "This is two"

tinydict = {'name': 'john','code':6734, 'dept': 'sales'}


print dict['one']       # Prints value for 'one' key
print dict[2]           # Prints value for 2 key
print tinydict          # Prints complete dictionary
print tinydict.keys()   # Prints all the keys
print tinydict.values() # Prints all the values
```

这会产生以下结果

```
This is one
This is two
{'dept': 'sales', 'code': 6734, 'name': 'john'}
['dept', 'code', 'name']
['sales', 6734, 'john']
```

字典没有元素之间的顺序概念。说元素“乱序”是不正确的；它们只是无序的。

#### 数据类型转换

有时，您可能需要在内置类型之间执行转换。要在类型之间进行转换，只需将类型名称用作函数即可。

有几个内置函数可以执行从一种数据类型到另一种数据类型的转换。这些函数返回一个表示转换值的新对象。

| 序号 | 功能说明                                                     |
| :--- | :----------------------------------------------------------- |
| 1    | **int(x [,base])** 将 x 转换为整数。如果 x 是字符串，则 base 指定基数。 |
| 2    | **long(x [,base] )** 将 x 转换为长整数。如果 x 是字符串，则 base 指定基数。 |
| 3    | **float(x)** 将 x 转换为浮点数。                             |
| 4    | **complex(real [,imag])** 创建一个复数。                     |
| 5    | **str(x)** 将对象 x 转换为字符串表示形式。                   |
| 6    | **repr(x)** 将对象 x 转换为表达式字符串。                    |
| 7    | **eval(str)** 评估一个字符串并返回一个对象。                 |
| 8    | **tuple(s)** 将 s 转换为元组。                               |
| 9    | **list(s)** 将 s 转换为列表。                                |
| 10   | **set(s)** 将 s 转换为集合。                                 |
| 11   | **dict(d)** 创建字典。d 必须是 (key,value) 元组的序列。      |
| 12   | **frozenset(s)** 将 s 转换为冻结集。                         |
| 13   | **chr(x)** 将整数转换为字符。                                |
| 14   | **unichr(x)** 将整数转换为 Unicode 字符。                    |
| 15   | **ord(x)** 将单个字符转换为其整数值。                        |
| 16   | **hex(x)** 将整数转换为十六进制字符串。                      |
| 17   | **oct(x)** 将整数转换为八进制字符串。                        |

## **运算符操作**

Python 语言支持以下类型的运算符。

- 算术运算符
- 比较（关系）运算符
- 赋值运算符
- 逻辑运算符
- 按位运算符
- 成员运算符
- 身份运算符

### **Python 算术运算符**

假设变量 ``a =10，b = 20``，然后

| 操作符      | 描述                                                         | 例子                                                     |
| :---------- | :----------------------------------------------------------- | :------------------------------------------------------- |
| + 加        | 在运算符的任一侧添加值。                                     | a + b = 30                                               |
| - 减        | 从左手操作数中减去右手操作数。                               | a – b = -10                                              |
| * 乘        | 将运算符两侧的值相乘                                         | a * b = 200                                              |
| / 除        | 将左手操作数除以右手操作数                                   | b / a = 2                                                |
| % 取模      | 将左手操作数除以右手操作数并返回余数                         | b % a = 0                                                |
| ** 指数运算 | 对运算符执行指数（幂）计算                                   | a**b 表示 10 的 20 次方                                  |
| //          | Floor Division - 操作数的除法，其**结果是去除小数点后数字的商**。但是，如果操作数之一为负，则结果为底，即从零舍入（向负无穷大） | 9//2 = 4 和 9.0//2.0 = 4.0, -11//3 = -4, -11.0//3 = -4.0 |

例子 假设变量 a 为 21，变量 b 为 10

```
#!/usr/bin/python

a = 21
b = 10
c = 0

c = a + b
print "Line 1 - Value of c is ", c

c = a - b
print "Line 2 - Value of c is ", c 

c = a * b
print "Line 3 - Value of c is ", c 

c = a / b
print "Line 4 - Value of c is ", c 

c = a % b
print "Line 5 - Value of c is ", c

a = 2
b = 3
c = a**b 
print "Line 6 - Value of c is ", c

a = 10
b = 5
c = a//b 
print "Line 7 - Value of c is ", c
```

当您执行上述程序时，它会产生以下结果

```
Line 1 - Value of c is 31
Line 2 - Value of c is 11
Line 3 - Value of c is 210
Line 4 - Value of c is 2
Line 5 - Value of c is 1
Line 6 - Value of c is 8
Line 7 - Value of c is 2
```

### **Python 比较运算符**

这些运算符比较它们两侧的值并决定它们之间的关系。它们也称为关系运算符。

假设变量 a 为 10，变量 b 为 20，然后

| 操作符 | 描述                                                 | 例子                                  |
| :----- | :--------------------------------------------------- | :------------------------------------ |
| ==     | 如果两个操作数的值相等，则条件成立。                 | (a == b) 不是真的。                   |
| !=     | 如果两个操作数的值不相等，则条件为真。               | (a != b) 是真的。                     |
| <>     | 如果两个操作数的值不相等，则条件为真。               | (a <> b) 是真的。这类似于 != 运算符。 |
| >      | 如果左操作数的值大于右操作数的值，则条件为真。       | (a > b) 不正确。                      |
| <      | 如果左操作数的值小于右操作数的值，则条件成立。       | (a < b) 是真的。                      |
| >=     | 如果左操作数的值大于或等于右操作数的值，则条件为真。 | (a >= b) 不是真的。                   |
| <=     | 如果左操作数的值小于或等于右操作数的值，则条件为真。 | (a <= b) 是真的。                     |

**例子**

假设变量 a 为 10，变量 b 为 20，然后

```
#!/usr/bin/python

a = 21
b = 10
c = 0

if ( a == b ):
   print "Line 1 - a is equal to b"
else:
   print "Line 1 - a is not equal to b"

if ( a != b ):
   print "Line 2 - a is not equal to b"
else:
   print "Line 2 - a is equal to b"

if ( a <> b ):
   print "Line 3 - a is not equal to b"
else:
   print "Line 3 - a is equal to b"

if ( a < b ):
   print "Line 4 - a is less than b" 
else:
   print "Line 4 - a is not less than b"

if ( a > b ):
   print "Line 5 - a is greater than b"
else:
   print "Line 5 - a is not greater than b"

a = 5;
b = 20;
if ( a <= b ):
   print "Line 6 - a is either less than or equal to  b"
else:
   print "Line 6 - a is neither less than nor equal to  b"

if ( b >= a ):
   print "Line 7 - b is either greater than  or equal to b"
else:
   print "Line 7 - b is neither greater than  nor equal to b"
```

当您执行上述程序时，它会产生以下结果

```
Line 1 - a is not equal to b
Line 2 - a is not equal to b
Line 3 - a is not equal to b
Line 4 - a is not less than b
Line 5 - a is greater than b
Line 6 - a is either less than or equal to b
Line 7 - b is either greater than or equal to b
```

### **Python 按位运算符**

按位运算符作用于位并执行逐位操作。假设 a = 60; b = 13；现在在二进制格式中，它们的值将分别为 0011 1100 和 0000 1101。下表列出了 Python 语言支持的按位运算符，并在其中每个示例中，我们使用上述两个变量（a 和 b）作为操作数 -

a = 0011 1100

b = 0000 1101

------

a&b = 0000 1100

a|b = 0011 1101

a^b = 0011 0001

~a = 1100 0011

Python语言支持的按位运算符有以下几种

| 操作符 | 描述                                                         | 例子                                                         |
| :----- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| &      | 如果两个操作数中都存在，则运算符将其复制到结果中。           | (a & b) (表示 0000 1100)                                     |
|        |                                                              | 如果它存在于任一操作数中，则它会复制一点。                   |
| ^      | 如果它被设置在一个操作数中而不是两个操作数中，它就会复制该位。 | (a ^ b) = 49（表示 0011 0001）                               |
| ~      | 它是一元的，具有“翻转”位的效果。                             | (~a ) = -61（由于带符号的二进制数，表示 2 的补码形式的 1100 0011。 |
| <<     | 左操作数值向左移动右操作数指定的位数。                       | a << 2 = 240（意味着 1111 0000）                             |
| >>     | 左操作数的值向右移动右操作数指定的位数。                     | a >> 2 = 15（表示 0000 1111）                                |

例子

```
#!/usr/bin/python

a = 60            # 60 = 0011 1100 
b = 13            # 13 = 0000 1101 
c = 0

c = a & b;        # 12 = 0000 1100
print "Line 1 - Value of c is ", c

c = a | b;        # 61 = 0011 1101 
print "Line 2 - Value of c is ", c

c = a ^ b;        # 49 = 0011 0001
print "Line 3 - Value of c is ", c

c = ~a;           # -61 = 1100 0011
print "Line 4 - Value of c is ", c

c = a << 2;       # 240 = 1111 0000
print "Line 5 - Value of c is ", c

c = a >> 2;       # 15 = 0000 1111
print "Line 6 - Value of c is ", c
```

当您执行上述程序时，它会产生以下结果

```
Line 1 - Value of c is 12
Line 2 - Value of c is 61
Line 3 - Value of c is 49
Line 4 - Value of c is -61
Line 5 - Value of c is 240
Line 6 - Value of c is 15
```

### **Python 逻辑运算符**

Python 语言支持以下逻辑运算符。假设变量 a 为 10，变量 b 为 20，则

| 操作符 | 描述                                           | 例子                 |
| :----- | :--------------------------------------------- | :------------------- |
| and    | 如果两个操作数都为真，则条件为真。             | (a 和 b) 是正确的。  |
| or     | 如果两个操作数中的任何一个不为零，则条件为真。 | (a 或 b) 是真的。    |
| not    | 用于反转其操作数的逻辑状态。                   | Not(a 和 b) 是假的。 |

### **Python 成员运算符**

Python 的成员资格运算符测试序列中的成员资格，例如字符串、列表或元组。有两个成员资格运营商，如下所述

| 操作符 | 描述                                                         | 例子                                                         |
| :----- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| in     | 如果找到指定序列中的变量，则计算结果为 true，否则为 false。  | x in y，如果 x 是序列 y 的成员，则此处 in 导致 1。           |
| not in | 如果在指定的序列中没有找到变量，则计算结果为 true，否则计算为 false。 | x not in y, 如果 x 不是序列 y 的成员，这里 not in 结果为 1。 |

例子

```
#!/usr/bin/python

a = 10
b = 20
list = [1, 2, 3, 4, 5 ];

if ( a in list ):
   print "Line 1 - a is available in the given list"
else:
   print "Line 1 - a is not available in the given list"

if ( b not in list ):
   print "Line 2 - b is not available in the given list"
else:
   print "Line 2 - b is available in the given list"

a = 2
if ( a in list ):
   print "Line 3 - a is available in the given list"
else:
   print "Line 3 - a is not available in the given list"
```

当您执行上述程序时，它会产生以下结果

```
Line 1 - a is not available in the given list
Line 2 - b is not available in the given list
Line 3 - a is available in the given list
```

### Python 身份运算符

身份运算符比较两个对象的内存位置。下面解释了两个身份运算符

| 操作符 | 描述                                                         | 例子                                                  |
| :----- | :----------------------------------------------------------- | :---------------------------------------------------- |
| is     | 如果运算符任一侧的变量指向同一对象，则计算结果为真，否则为假。 | x 是 y，如果 id(x) 等于 id(y) ，则结果为 1。          |
| is not | 如果运算符任一侧的变量指向同一对象，则计算结果为 false，否则为 true。 | x 不是 y，如果 id(x) 不等于 id(y) ，这里的结果不是1。 |

例子

```
#!/usr/bin/python

a = 20
b = 20

if ( a is b ):
   print "Line 1 - a and b have same identity"
else:
   print "Line 1 - a and b do not have same identity"

if ( id(a) == id(b) ):
   print "Line 2 - a and b have same identity"
else:
   print "Line 2 - a and b do not have same identity"

b = 30
if ( a is b ):
   print "Line 3 - a and b have same identity"
else:
   print "Line 3 - a and b do not have same identity"

if ( a is not b ):
   print "Line 4 - a and b do not have same identity"
else:
   print "Line 4 - a and b have same identity"
```

当您执行上述程序时，它会产生以下结果

```
Line 1 - a and b have same identity
Line 2 - a and b have same identity
Line 3 - a and b do not have same identity
Line 4 - a and b do not have same identity
```

### Python 运算符优先级

下表列出了从最高优先级到最低优先级的所有运算符。

| 操作符                   | 描述                                            |
| :----------------------- | :---------------------------------------------- |
| **                       | 求幂（提高到幂）                                |
| ~ + -                    | 补码、一元加减（最后两个的方法名称是 +@ 和 -@） |
| * / % //                 | 乘法、除法、取模和除法                          |
| + -                      | 加减                                            |
| >> <<                    | 左右位移                                        |
| &                        | 按位 'AND'td>                                   |
| ^                        |                                                 |
| <= < > >=                | 比较运算符                                      |
| <> == !=                 | 等号运算符                                      |
| = %= /= //= -= += *= **= | 赋值运算符                                      |
| is is not                | 身份运算符                                      |
| in not in                | 会员运算符                                      |
| not or and               | 逻辑运算符                                      |

运算符优先级会影响表达式的计算方式。

例如，x = 7 + 3 * 2；这里，x 被赋值为 13，而不是 20，因为运算符 * 的优先级高于 +，所以它先乘以 3*2，然后加到 7。

在这里，具有最高优先级的运算符出现在表格的顶部，具有最低优先级的运算符出现在底部。

例子

```
#!/usr/bin/python

a = 20
b = 10
c = 15
d = 5
e = 0

e = (a + b) * c / d       #( 30 * 15 ) / 5
print "Value of (a + b) * c / d is ",  e

e = ((a + b) * c) / d     # (30 * 15 ) / 5
print "Value of ((a + b) * c) / d is ",  e

e = (a + b) * (c / d);    # (30) * (15/5)
print "Value of (a + b) * (c / d) is ",  e

e = a + (b * c) / d;      #  20 + (150/5)
print "Value of a + (b * c) / d is ",  e
```

当您执行上述程序时，它会产生以下结果

```
Value of (a + b) * c / d is 90
Value of ((a + b) * c) / d is 90
Value of (a + b) * (c / d) is 90
Value of a + (b * c) / d is 50
```
