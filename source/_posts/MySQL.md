---
title: MySQL
date: 2023-09-03 19:52:43
tags:
---





## 启动,停止,登录:

```
  net stop mysql
  net start mysql
  mysql （-h）-u 用户名 -p 用户密码
  注意，如果是连接到另外的机器上，则需要加入一个参数-h机器IP

```

## 新增新用户:

```
grant 权限 on 数据库.* to 用户名@登录主机 identified by "密码"

```

> 例：增加一个用户user密码为password，让其可以在本机上登录， 并对所有数据库有查询、插入、修改、删除的权限。首先用以root用户连入mysql，然后键入以下命令：
>
> grant select,insert,update,delete on . to user@localhost Identified by “password”;
>
> 如果希望该用户能够在任何机器上登陆mysql，则将localhost改为"%"。
> ————————————————
> 原文链接：https://blog.csdn.net/weixin_44870139/article/details/105555238

## 操作数据库:

```
use 数据库名   //表示使用哪一个数据库

//导入数据库文件:
mysql>use 数据库名;
mysql>source d:/mysql.sql; 
```

## 显示数据库:

```
show databases;

//显示数据表:
use 库名;
tables;
//显示数据表结构:
describe 表名;
```

## 建立与删除:

```
#建立\删除库:
create database 库名（character set utf8）;
drop database 库名;

#建立\删除表:
use 库名;
create table 表名(字段列表);
drop table 表名;

```

## 清空\显示表记录:

```
#清空
delete from 表名;
#显示
select * from 表名;
```

## 插入:

```
insert into 表名 values (字段列表);
```

## 更新表中数据:

```
update 表名 set 字段="值" where 子句 order by 子句 limit 子句
WHERE 子句：可选项。用于限定表中要修改的行。若不指定，则修改表中所有的行。
ORDER BY 子句：可选项。用于限定表中的行被修改的次序。
LIMIT 子句：可选项。用于限定被修改的行数。

```

## 导出和导入数据:

```
mysqldump --opt test > mysql.test
即将数据库test数据库导出到mysql.test文本文件
例：mysqldump -u root -p用户密码 --databases dbname > mysql.dbname

mysqlimport -u root -p用户密码 < mysql.dbname。

#文本数据导入数据库:
文本数据的字段数据之间用tab键隔开。
use test;
load data local infile "文件名" into table 表名;

```

## 表操作:

```
创建表：
1、创建表：
　　　　>CREATE TABLE table_name(
　　　　>id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,　　　　//id值，无符号、非空、递增——唯一性，可做主键。
　　　　>name VARCHAR(60) NOT NULL
　　　　>score TINYINT UNSIGNED NOT NULL DEFAULT 0,　　　　//设置默认列值
　　　　>PRIMARY KEY(id)
　　　　>)ENGINE=InnoDB　　　　//设置表的存储引擎，一般常用InnoDB和MyISAM；InnoDB可靠，支持事务；MyISAM高效不支持全文检索
　　　　>DEFAULT charset=utf8;　　//设置默认的编码，防止数据库中文乱码
　　　　如果有条件的创建数据表还可以使用 >CREATE TABLE IF NOT EXISTS tb_name(…
　　2、复制表：
　　　　>CREATE TABLE tb_name2 SELECT * FROM tb_name;
　　　　或者部分复制：
　　　　>CREATE TABLE tb_name2 SELECT id,name FROM tb_name;
　　3、创建临时表：
　　　　>CREATE TEMPORARY TABLE tb_name(这里和创建普通表一样);
　　4、查看数据库中可用的表：
　　　　>SHOW TABLES;
　　5、查看表的结构：
　　　　>DESCRIBE tb_name;
　　　　也可以使用：
　　　　>SHOW COLUMNS in tb_name; 　　　　//from也可以
　　6、删除表：
　　　　>DROP [ TEMPORARY ] TABLE [ IF EXISTS ] tb_name[ ,tb_name2…];
　　　　实例：
　　　　>DROP TABLE IF EXISTS tb_name;
　　7、表重命名：
　　　　>RENAME TABLE name_old TO name_new;
　　　　还可以使用：
　　　　>ALTER TABLE name_old RENAME name_new;

三、修改表：
1、更改表结构：
　　　　>ALTER TABLE tb_name ADD[CHANGE,RENAME,DROP] …要更改的内容…
　　　　实例：
　　　　>ALTER TABLE tb_name ADD COLUMN address varchar(80) NOT NULL;
　　　　>ALTER TABLE tb_name DROP address;
　　　　>ALTER TABLE tb_name CHANGE score score SMALLINT(4) NOT NULL;

四、插入数据：
1、插入数据：
　　　　>INSERT INTO tb_name(id,name,score)VALUES(NULL,‘张三’,140),(NULL,‘张四’,178),(NULL,‘张五’,134);
　　　　这里的插入多条数据直接在后边加上逗号，直接写入插入的数据即可；主键id是自增的列(需要设置)，设置之后可以不用写。
　　2、插入检索出来的数据：
　　　　>INSERT INTO tb_name(name,score) SELECT name,score FROM tb_name2;

五、更新数据：
1、指定更新数据：
　　　　>UPDATE tb_name SET score=189 WHERE id=2;
　　　　>UPDATE tablename SET columnName=NewValue [ WHERE condition ]

六、删除数据：
1、删除数据：
　　　　>DELETE FROM tb_name WHERE id=3;
```

## 条件控制(where,having):

```
1、WHERE 语句：
　　　　>SELECT * FROM tb_name WHERE id=3;
　　2、HAVING 语句：
　　　　>SELECT * FROM tb_name GROUP BY score HAVING count(*)>2
　　3、相关条件控制符：
　　　　=、>、<、<>、IN(1,2,3…)、BETWEEN a AND b、NOT
　　　　AND 、OR
　　　　Linke()用法中 % 为匹配任意、 _ 匹配一个字符（可以是汉字）
　　　　IS NULL 空值检测

```

## MySQL支持REGEXP的正则表达式：　

```
 　　　>SELECT * FROM tb_name WHERE name REGEXP ‘1’ //找出以A-D 为开头的name　　2、特殊字符需要转义。
```

## MySQL的一些函数：

```
1、字符串链接——CONCAT()
　　　　>SELECT CONCAT(name,‘=>’,score) FROM tb_name
　　2、数学函数：
　　　　AVG、SUM、MAX、MIN、COUNT；
　　3、文本处理函数：
　　　　TRIM、LOCATE、UPPER、LOWER、SUBSTRING
　　4、运算符：
　　　　+、-、*、
　　5、时间函数：
　　　　DATE()、CURTIME()、DAY()、YEAR()、NOW()…

```

> ###### UNION规则——可以执行两个语句（可以去除重复行）

> 分组查询：
> 1、分组查询可以按照指定的列进行分组：
> 　　　　>SELECT COUNT() FROM tb_name GROUP BY score HAVING COUNT()>1;
> 　　2、条件使用Having；
> 　　3、ORDER BY 排序：
> 　　　　ORDER BY DESC|ASC　　　　=>按数据的降序和升序排列

## 全文检索——MATCH和AGAINST:

```
1、SELECT MATCH(note_text)AGAINST(‘PICASO’) FROM tb_name;
　　2、InnoDB引擎不支持全文检索，MyISAM可以；
```

## 视图:

```
1、创建视图
　　　　>CREATE VIEW name AS SELECT * FROM tb_name WHERE ~~ ORDER BY ~~;
　　2、视图的特殊作用：
　　　　　　a、简化表之间的联结（把联结写在select中）；
　　　　　　b、重新格式化输出检索的数据（TRIM，CONCAT等函数）；
　　　　　　c、过滤不想要的数据（select部分）
　　　　　　d、使用视图计算字段值，如汇总这样的值。

```

## 存储过程：

> 个人理解，存储过程就是一个自定义函数在于返回类型的差别(自定义函数必须指定返回类型)，有局部变量参数，可传入参数，不过这语法够呆滞的

```
　　1、创建存储过程：
　　　　>CREATE PROCEDURE pro(
　　　　>IN num INT,OUT total INT)
　　　　>BEGIN
　　　　>SELECT SUM(score) INTO total FROM tb_name WHERE id=num;
　　　　>END;
　　　***这里的 IN (传递一个值给存储过程)，OUT（从存储过程传出一个值），INOUT（对存储过程传入、传出），INTO（保存变量）
　　2、调用存储过程：
　　　　>CALL pro(13,@total)　　　　　　//这里的存储过程两个变量，一个是IN一个是OUT，这里的OUT也是需要写上的，不写会出错
　　　　>SELECT @total　　　　　　　　　//这里就可以看到结果了；
　　3、存储过程的其他操作：
　　　　>SHOW PROCEDURE STATUS;　　　　　　//显示当期的存储过程
　　　　>DROP PROCEDURE pro;　　　　　　　　　//删除指定存储过程

```

## 游标:

>  *游标是一段私有的**SQL**工作区**,**也就是一段内存区域**,**用于暂时存放受**SQL**语句影响到的数据。通俗理解就是将受影响的数据暂时放到了一个内存区域的虚表中，而这个虚表就是游标。*

```
游标的操作
　　　　>CREATE PROCEDURE pro()
　　　　>BEGIN
　　　　>DECLARE ordername CURSOR FOR
　　　　>SELECT order_num FROM orders;
　　　　>END;
　　　　
　　　　>OPEN ordername;　　　　//打开游标

>CLOSE ordername;　　　　//关闭游标

```

> 数据库中的事物可以回滚，而游标在其中起着非常重要的作用，由于对数据库的操作我们会暂时放在游标中，只要不提交，我们就可以根据游标中内容进行回滚，在一定意义有利于数据库的安全。
>
>               2，另外，在Oracle中PL/SQL只能返回单行数据，而游标弥补了这个不足。相当于ADO.NET中的Data table吧。

## 简单游标使用:

| 步骤 | 关键词                    | 说明                             |
| ---- | ------------------------- | -------------------------------- |
| 1    | *在**DECLARE**中**cursor* | 声明游标，创建一个命名的查询语句 |
| 2    | Open                      | 打开游标                         |
| 3    | Fetch                     | 取出游标中的一条记录装入变量     |
| 4    | Close                     | 释放游标                         |

> 当然游标中可以存放一条数据，也可以存放多条数据，后者是我们用游标，前者我们通过PL/SQL语句即可完成的，这样我们在这里就必须用到循环结构了，在Oracle数据库中我们可以使用while…… loop……end loop , for…… loop……end loop，loop……end loop。在这里需要提出的是，for循环结构在Oracle中被简化了，我们只需要声明和使用即可:

```
		declare
		  --定义记录类型的变量
		  v_user user%rowtype;
		  --1，利用cursor关键字声明游标
		  cursor user_cur is
		    select * from user;
		begin
		  --2,打开游标
		  open user_cur;
		  --3,利用fetch读取数据
		  fetch user_cur
		    into v_user;
		  while user_cur%found loop
		    dbms_output.put_line(v_user.userName);
		    fetch user_cur
		      into v_user;
		  end loop;
		  --4，释放游标
		  close user_cur;
		end;
```

> 简化的for循环:
>
> ​		declare
> ​		  --1，利用cursor关键字声明游标
> ​		  cursor user_cur is
> ​		    select * from user;
> ​		begin
> ​		  --2,直接使用，Oracle会自动打开和关闭等操作。
> ​		   for v_user in user_cur loop
> ​		       dbms_output.put_line(v_user.userName);
> ​		    end loop
> ​		end;

### 带参数的游标:

```
	declare
	  --定义记录类型的变量
	  v_User user%rowtype;
	  --1，利用cursor关键字声明带参数的游标
	  cursor user_Cur(v_UserNo number) is
	    select * from user where  userNo=v_UserNo;
	begin
	  --2,打开带参数的游标，使之更加灵活 。
	  open user_Cur(1012);
	  --3,利用fetch读取数据
	  loop
	       fetch user_Cur into v_User;
	       exit when user_Cur%notfound;
	       dbms_output.put_line(v_user.userName);
	  end loop;
	  --4，释放游标
	  close user_Cur;
	end;
```

## 触发器:

> DEFINER：定义该触发器的用户和主机地址，一般默认为当前用户和主机地址。
> trigger_name：触发器名称 AFTER|BEFORE：触发器触发状态，二选一。
> INSERT|UPDATE|DELETE：触发器触发状态，三选一。
> table_name：监控的数据表名称。
> FOR EACH ROW：行级触发器，修改一行数据触发一次。不写就默认语句级触发器，不管修改多少行数据，只执行一次。

```
触发器是指在进行某项指定操作时，触发触发器内指定的操作；
　　1、支持触发器的语句有DELETE、INSERT、UPDATE,其他均不支持
　　2、创建触发器：
　　　　>CREATE TRIGGER trig AFTER INSERT ON ORDERS FOR EACH ROW SELECT NEW.orser_name;
　　　　>INSERT语句，触发语句，返回一个值
　　3、删除触发器
　　　　>DROP TRIGGER trig;

```

```sql
-- 数据库操作工具方法（navicat、sqlyog）
CREATE DEFINER=`root`@`localhost` TRIGGER trigger_name AFTER|BEFORE INSERT|UPDATE|DELETE ON table_name
FOR EACH ROW -- 行级触发器，修改一行数据触发一次。不写就默认语句级触发器，不管修改多少行数据，只执行一次。
BEGIN
	... -- 具体执行语句
END

```

```sql
-- 命令行方式
--先更改语句结束符号
delimiter ##  -- 切换自定义结束符号，在可视化操作页面不需要，在命令行中创建触发器则需要。创建存储过程时候也需要
-- 再创建触发器
CREATE TRIGGER trigger_name AFTER|BEFORE INSERT|UPDATE|DELETE ON table_name
FOR EACH ROW -- 行级触发器
BEGIN
	... -- 具体执行语句
END
## -- 代表创建触发器语句结束，这样就不会执行到分号;的时候暂停执行了。
delimiter ; --恢复mysql默认语句结束符号

```

```
-- 在插入bysj_et表后触发
DROP TRIGGER if EXISTS testi; -- 如果存在testi触发器则删除
CREATE TRIGGER testi AFTER INSERT ON bysj_et
FOR EACH ROW
BEGIN
	INSERT INTO bysj_dt VALUES (new.id,new.et_name);
END

-- 在删除bysj_et表后触发
DROP TRIGGER if EXISTS testd; -- 如果存在testd触发器则删除
CREATE TRIGGER testd AFTER DELETE ON bysj_et
FOR EACH ROW
BEGIN
	DELETE FROM bysj_dt WHERE id = old.id AND dt_name = old.et_name;
END

-- 在更新bysj_et表后触发
DROP TRIGGER if EXISTS testu; -- 如果存在testu触发器则删除
CREATE TRIGGER testu AFTER UPDATE ON bysj_et
FOR EACH ROW
BEGIN
	-- SET @oid = old.id; -- 获取更新前旧数据行id
	-- SET @odt_name = old.et_name; -- 获取更新前旧数据行et_name
	-- SET @nid = new.id; -- 获取新数据行id
	-- SET @ndt_name = new.et_name; -- 获取新数据行et_name
	--UPDATE bysj_dt SET id = @nid,dt_name = @ndt_name WHERE id = @oid AND dt_name = @odt_name; --具体执行语句
	-- 上面的语句熟悉了之后可以优化成下面这样
	UPDATE bysj_dt SET id = new.id,dt_name = new.et_name WHERE id = old.id AND dt_name = old.et_name;
END

```

> 1.new.字段的值可以在before类型的触发器中进行赋值和取值，在after类型触发器中只能取值。(在after类型触发器中进行对new数据行赋值操作会报错。因为after是在操作之后，已经产生了新数据行，不可修改。)
> 2.在insert操作中，只有new数据行，没有old数据行。(使用old关键字会报错)
> 3.在update操作中，new数据行和old数据行存在。
> 4.在delete操作中，只有old数据行。(使用new关键字会报错)
> 5.在mysql5.7之前的版本，同一张表中，不能存在两个类型一样的触发器。如果想在一个触发器种实现两种不同的处理语句执行，可以增加条件判断。

```
#用if语句:

CREATE DEFINER=`root`@`localhost` TRIGGER testi AFTER INSERT ON bysj_et
FOR EACH ROW
BEGIN
	IF(new.id = 6) -- 当新id为6时
	THEN IF(new.et_name = '6') -- 当新id为6，并且name也为6才执行插入语句
		THEN INSERT INTO bysj_dt VALUES (new.id,new.et_name);
		END IF;
	END IF;
END;

用case when:
CREATE DEFINER=`root`@`localhost` TRIGGER testi AFTER INSERT ON bysj_et
FOR EACH ROW
BEGIN
	CASE 
	WHEN new.id = 6 AND new.et_name = '6' THEN
		INSERT INTO bysj_dt VALUES (new.id,'等于6');
	WHEN new.id < 6 THEN
		INSERT INTO bysj_dt VALUES (new.id,'小于6');
	ELSE
		INSERT INTO bysj_dt VALUES (100,'100');
END CASE;
END

```

## 语法整理：

```
1、ALTER TABLE（修改表）
　　　　ALTER TABLE table_name
　　　　(　　ADD　　　　column　　datatype 　　[ NULL | NOT NULL ]　　[ CONSTRAINTS ]
　　　　　　 CHANGE　　column 　　datatype 　　COLUMNS　　[ NULL | NOT NULL ]　　 [ CONSTRAINTS ]
　　　　　　 DROP　　　 column，
　　　　　　　。。。。
　　　　)
　　2、COMMIT(处理事务)
　　　　>COMMIT;
　　3、CREATE INDEX(在一个或多个列上创建索引)
　　　　CREATE INDEX index_name ON tb_name (column [ ASC | DESC ] , …);
　　4、CREATE PROCEDURE (创建存储过程)
　　　　CREATE PROCEDURE pro([ parameters ])
　　　　BEGIN
　　　　…
　　　　END
　　5、CREATE TABLE(创建表)
　　　　CREATE TABLE tb_name(
　　　　column_name　　datetype　　[ NULL | NOT NULL ] 　　[ condtraints] ,
　　　　column_name　　datetype　　[ NULL | NOT NULL ] 　　[ condtraints] ,
　　　　…
　　　　PRIMARY KEY( column_name )
　　　　)ENGINE=[ InnoDB | MyiSAM ]DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
　　6、CREATE USER(创建用户)
　　　　CREATE USER user_name [ @hostname ] [ IDENTIFIED BY [ PASSWORD ] ‘pass_word’ ];
　　7、CREATE VIEW （在一个或多个表上创建视图）
　　　　CREATE [ OR REPLACE ] VIEW view_name AS SELECT。。。。。。
　　8、DELETE (从表中删除一行或多行)
　　　　DELETE FROM table_name [WHERE …]
　　9、DROP(永久删除数据库及对象，如视图、索引等)
　　　　DROP DATEBASE | INDEX | PROCEDURE | TABLE | TRIGGER | USER | VIEW name
　　10、INSERT （给表添加行）
　　　　INSERT INTO tb_name [ ( columns,… ) ] VALUES(value1,…);
　　　　使用SELECT值插入：
　　　　INSERT INTO tb_name [ ( columns,… ) ]
　　　　SELECT columns , … FROM tb_name [ WHERE … ] ;
　　 11、ROLLBACK（撤销一个事务处理块）
　　　　ROLLBACK [ TO savapointname ];
　　 12、SAVEPOINT(为ROLLBACK设置保留点)
　　　　SAVEPOINT sp1;
　　 13、SELECT (检索数据，显示信息)
　　　　SELECT column_name,…FROM tb_name [ WHERE ] [ UNION ] [ RROUP BY ] [ HAVING ] [ ORDER BY ]
　　14、START TRANSACTION (一个新的事务处理块的开始)
　　　　START TRANSACTION
　　 15、UPDATE(更新一个表中的一行或多行)
　　　　UPDATE tb_name SET column=value,…[ where ]
```



