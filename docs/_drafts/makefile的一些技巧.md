1. 忽略错误继续运行，并且不输出错误信息？

    比如在清理文件过程中，可能遇到被清理文件并不存在的错误。这种错误应该忽略并继续运行make。可以使用下面的语法：

    ```
    @cmd 2>/dev/null ||:
    ```
    上面`cmd`是待运行的命令。 `2>/dev/null`是不输出错误信息。 `||:`相当于 `|| trure`。 `:`这里是`true`的简写.
    如果要禁止输出命令本身，可以使用make -s

2. 如何把shell命令的结果赋值给变量？

    ```
    output_file := $(shell echo "`pwd`/../doccs/")
    ```
    注意这里`shell`和`echo`都不能省略

3. 为何在Makefile中声明的环境变量不起作用？
    在Makefile中，每个recipe都是一个单独的shell，所以命令：
    ```
    mytarget:
        export MYVAR=myvar
        echo "MYVAR is $(myvar)"
    ```
    将不会输出"MYVAR is myvar"

    正确的语法是使用target variable

    ```
    # next line will defined a target variable and export it
    mytarget: export MYVAR := myvar
    mytarget:
        echo "MYVAR is ${myvar}"
    ```

4. 如何在make中遍历文件并执行copy?
    ```
    for f in $(shell "ls /apps/omega/omega/config/sql/*"); do sudo docker cp $$f ${postgres_init_dir};done
    ```
    注意这里的`$$f`
5. 如何发现未定义的变量？
    make --warn-undefined-variables -n TARGET | grep warning
6. safe-rm?
    可以安装safe-rm，并通过它来调用rm。但是，safe-rm并不能拯救 rm /*
