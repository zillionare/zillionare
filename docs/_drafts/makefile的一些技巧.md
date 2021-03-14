1. 忽略错误继续运行，并且不输出错误信息？

    比如在清理文件过程中，可能遇到被清理文件并不存在的错误。这种错误应该忽略并继续运行make。可以使用下面的语法：

    ```
    @cmd 2>/dev/null ||:
    ```
    上面`cmd`是待运行的命令。 `2>/dev/null`是不输出错误信息。 `||:`相当于 `|| trure`。 `:`这里是`true`的简写.

2. 如何把shell命令的结果赋值给变量？

    ```
    output_file := $(shell echo "`pwd`/../doccs/")
    ```
    注意这里`shell`和`echo`都不能省略

3. 为何在Makefile中声明的环境变量不起作用？
    在Makefile中，每个target都是一个单独的shell,所以环境变量声明必须在target内部声明，仅对本target有效。