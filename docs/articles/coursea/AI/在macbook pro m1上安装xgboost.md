# 在apple m1上安装xgboost
xgboost在apple m1上没有wheels可用，需要自己编译。
xgboost依赖于numpy,scipy，这些package最好也使用native的，因此选用miniforge来安装。
xgboost还依赖libomp。当前版本12，有兼容性问题（会导致segmentation fault），需要回退到11。这个回退操作比较复杂，我们会专门讲到。

1. 先安装miniforge, 在[github](https://github.com/conda-forge/miniforge)下找到[Miniforge3-MacOSX-arm64](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh)，下载安装。

2. 运行conda init，然后退出重进terminal，创建一个新的虚拟环境：
```
# python 3.9才是mac m1下的native版本
conda create -n xgboost python=3.9
```

3. 安装好numpy, scipy和sklearn:
```
conda install numpy scipy scikit-learn
```
然后进入虚拟环境。

4. clone xgboost源码到本地：
```
git clone https://github.com/dmlc/xgboost.git
```
然后进入xgboost目录，创建一个build目录，进入build目录，执行如下命令：
```
cmake ..
make -j4 # 同时运行4个任务，也可以调整为-j8
```
这里需要gcc, cmake，可以通过brew安装。

5. 进入xgboost下的python-packages目录，准备执行如下命令：
```
python setup.py bdist_wheel
```

在执行上述命令之前，先查看一下setup.py文件，找到"install_requires"那一节,在其中添加已安装好的numpy和scipy的版本。如果不这样做，那么安装xgboost的时候，会搜索pip库，从而可能安装上非native编译的numpy和scipy。

然后执行上述命令，这样就构建好了xgboost的wheel包，可以将其保存起来。现在我们通过pip来安装这个包。注意为了能尽可能使用macos m1的native构建库，我们在安装python库时，一般使用conda来安装，而不是pip, 因为我们安装的miniforge会优先安装m1 native的库。

6. 现在检查一下libomp的版本：
```
brew info libomp
```
如果显示为12.0，则需要回退到11.1.0，否则在运行xgboot时，可能出现segmentation fault。

在brew里回滚是一个比较烦琐的事情，特别是有时候brew仓库里不会列出历史版本，在libomp上我们就刚好遇到此情况。

首先，我们进行[homebrew core](https://github.com/Homebrew/homebrew-core/find/master)的搜索页面，在这里输入libomp:

![](https://images.jieyu.ai/images/202110/20211001111448.png)

点击搜索出来的文件(libomp.rb)，进入以下页面，然后再点击“history"按钮：
![](https://images.jieyu.ai/images/202110/Screen Shot 2021-10-01 at 11.19.09.png)

然后我们将进入以下页面：
![](https://images.jieyu.ai/images/202110/20211001112339.png)

找到11.1.0的版本，点击raw按钮，将文件内容复制下来。

然后在brew里执行如下命令，以定位repo中的同名文件：
```
find $(brew --repository) -name libomp.rb
```
然后我们编辑这个文件，将文件内容完全替换为之前从git上复制的内容，再运行如下命令：
```
brew uninstall libomp # 删除之前的版本
brew install libomp
brew pin libomp # 防止意外更新
```

6. 现在，让我们运行xgboost的单元测试，以证明安装成功：
```
export PYTHONPATH=./python-package
pytest -v -s --fulltrace tests/python
```
如果没有报错，则说明xgboost的python包安装成功。

m1运行一直很安静，一度让我认为他没有风扇。运行XGBOOST之后，我听到了m1低低的嘶吼！所以，当运行一般任务时，m1的芯片十分出色，完全不会有发热。一旦涉及到机器学习和深度学习，不给电还是不行的。
