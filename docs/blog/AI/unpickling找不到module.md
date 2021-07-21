如果我们使用notebook（比如kaggle.com)来训练模型并保存为pickle文件，很可能模型处在top level名字空间下。在工程中使用这个模型时，我们往往会进行一些包装，在非顶级名字空间下unpickling这个模型，这样就会出现找不到模型类的错误。

比如，我们通过kaggle.com训练如下模型：


```python
from math import sqrt
from pathlib import Path
from typing import List, Tuple, Callable
import numpy as np
from fastai.vision.all import *
from torch import nn
import tempfile
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MyRandomSplitter:
    def __init__(self, valid_pct:float=0.2, seed:int=None):
        self.valid_pct = valid_pct
        self.seed = seed

    def __call__(self, o):
        if self.seed is not None: torch.manual_seed(self.seed)
        rand_idx = L(list(torch.randperm(len(o)).numpy()))
        cut = int(self.valid_pct * len(o))
        return rand_idx[cut:],rand_idx[:cut]
    
class HacktchaLoss(BaseLoss):
    def __init__(self, nclasses:int, nletters:int, axis=-1, **kwargs):
        self.func = None
        self._nclasses = nclasses
        self._nletters = nletters

    def __call__(self, inp, *y):
        preds = inp.split(self._nclasses, dim = 1)
        
        _loss = nn.CrossEntropyLoss()(preds[0], y[0])
        for i in range(self._nletters):
            _loss += nn.CrossEntropyLoss()(preds[i], y[i])
    
        return _loss

    def decodes(self, x):
        preds = x.split(self._nclasses, dim = 1)
        return [preds[i].argmax(dim=1) for i in range(self._nletters)]

class LabellingWrapper():
    def __init__(self, pos: int):
        self._pos = pos
        
    def __call__(self, filepath: Path):
        """get label from file name

        It's assumed that the filename, or parts of it contains the label. The filename should be in either "1234.jpg" or "1234_xxx.jpg" format. The latter form is used when there's multiple image belongs to same label

        Args:
            filepath (Path): [description]

        Returns:
            [type]: [description]
        """
        label = filepath.parts[-1].split(".")[0]
    
        if label.find("_"):
            label = label.split("_")[0]
            
        return label[self._pos]

class HacktchaModel:
    def __init__(self, vocab:str, nletters:int, arch: Callable=None, image_path:Tuple[str, str] = None):
        self._nletters = nletters
        self._vocab = vocab
        self._bs = 64
        self._nclasses = len(self._vocab)
        self._arch = arch
        self._lr = 3e-3
        
        if image_path is not None:
            if len(image_path) == 1:
                self._fine_tune_images = image_path[0]
                self._pretrain_images = None
            else:
                self._pretrain_images = image_path[0]
                self._fine_tune_images = image_path[1]

        self._dls = None
        self._learner:Learner = None

        blocks = (ImageBlock(cls=PILImageBW), *([CategoryBlock] * self._nletters))

        self._datasets = DataBlock(
            blocks=blocks, 
            n_inp=1, 
            get_items=get_image_files, 
            get_y= [LabellingWrapper(i) for i in range(self._nletters)],
            batch_tfms=[*aug_transforms(do_flip=False, size=108), Normalize()],
        splitter = MyRandomSplitter(seed=42))


    def create_learner(self, image_path:str, has_pretrain:bool=False):
        """create a cnn_learner. 
        
        Args:
            has_pretrain (bool): if True then loads pretrained model
        """
        if has_pretrain: # this is fine tune stage
            nfiles = len(os.listdir(image_path))
            self._bs = min(self._bs, int((sqrt(nfiles))))

        self._dls = self._datasets.dataloaders(source=image_path, bs=self._bs)

        self._learner = cnn_learner(
            self._dls, 
            self._arch, 
            n_out = (self._nclasses * self._nletters), 
            loss_func=HacktchaLoss(self._nclasses, self._nletters), 
            lr=self._lr,
            metrics=self.accuracy,
            cbs = [SaveModelCallback, EarlyStoppingCallback(patience=3)])

        if has_pretrain:
            self._learner.load("model")

    def accuracy(self, preds, *y):
        """calcualte accuracy of the prediction

        Args:
            preds ([type]): [description]
        """
        preds = preds.split(self._nclasses, dim=1)

        r0 = (preds[0].argmax(dim=1) == y[0]).float().mean()
        for i in range(1, self._nletters):
            r0 += (preds[i].argmax(dim=1) == y[i]).float().mean()

        return r0/self._nletters

    def train(self, save_to: str, epoch: int=100):
        # do the training on general captcha images dataset
        if self._pretrain_images is not None:
            logger.info("pretrain with images at %s", self._pretrain_images)
            self.create_learner(self._pretrain_images)        
            lr, _ = self._learner.lr_find()

            self._learner.fine_tune(epoch, lr)

            self._learner.save("tmp", pickle_protocol = 4)

        # fine_tune on specific images found on specific website
        logger.info("fine tune with images at %s", self._fine_tune_images)
        self.create_learner(self._fine_tune_images, self._pretrain_images is not None)
        lr, _ = self._learner.lr_find()
        
        self._learner.fine_tune(epoch, lr)
        loss, acc = self._learner.validate(ds_idx=1)

        model_file = os.path.join(save_to, f"hacktcha-{self._arch.__name__}-{self._nletters}-{self._nclasses}-{acc:.2f}.pkl")
        self._learner.export(model_file)
    
    @staticmethod
    def from_model(model: str, vocab:str, nletters: int):
        hacktcha = HacktchaModel(vocab, nletters)
        hacktcha._learner = load_learner(model)
        
        return hacktcha
    
    def predict(self, filepath:str):
        letters, _, _ = self._learner.predict(filepath)
        
        return ''.join(letters)
    
    def test(self, test_images_dir:str):
        missed = 0
        test_images = Path(test_images_dir).ls()
        for test_image in test_images:
            letters = self.predict(str(test_image))
            
            if letters != test_image.stem:
                missed  += 1
                print(f"pred {letters}, actual: {test_image.stem}")
                
        return missed / len(test_images)
        ```

这里的模型包装在类`HacktchaModel`中，这个类又依赖于`HacktchaLoss`和`LabellingWrapper`。在训练`train`结束时，我们会将模型导出为.pkl文件。此时的HacktchaLoss, HacktchaModel都处于`__main__`名字空间下。

如果我们在工程中加载这个模型，只要加载的位置不处于顶级名字空间下，就会报错：

```text
AttributeError: Can't get attribute 'LabellingWrapper' on <module '__main__'
```
这里的`LabellingWrapper`也可能是`HacktchaModel`依赖的其它类，也可能是`HacktchaModel`本身。

如何理解加载位置不在顶级名字空间下？具体地说，如果你的工程结构如下：

```
myproject
    |
    myproject
    |---cli.py
    |---models
        |----hacktcha.py

```
如果程序通过`python cli.py`来启动，则在`cli.py`中引入和声明的变量都处于顶级名字空间下，而在`models\hacktcha.py`文件中引入的变量则不是。

出于封装的考虑，我们可能更希望`hacktcha.py`来加截模型，并提供服务，然后在`cli.py`中调用。为此，我们需要对上述unpickling错误进行修复。修复的方法就是将上述类的定义注入到`__main__`模块中（注意，需要与训练时的top level名字空间对应即可，并不一定是__main__)。

我们使用下面的方法：
```
def fix_unpickle_namespace():
    mm = sys.modules["__main__"]
    setattr(mm, "LabellingWrapper", LabellingWrapper)
    setattr(mm, "HacktchaLoss", HacktchaLoss)
    setattr(mm, "MyRandomSplitter", MyRandomSplitter)
    setattr(mm, "HacktchaModel", HacktchaModel)
```
然后在加载模型之前调用上述函数即可。
