# OCR识别

## 背景

在当前屏幕中识别文本的位置。

## 实现原理

OCR的安装是个很麻烦的事情，虽然操作很简单，但其实安装包有点大，这并不符合我们对框架依赖治理的理解。

因此，我们想到将它做成一个 `RPC` 服务在其他机器上部署，测试机通过远程调用 `RPC` 服务的方式使用它；

RPC 的调用逻辑：

![](https://pic.imgdb.cn/item/64f054c3661c6c8e54ff47b5.png)

这样我们只需要在服务端部署好 OCR 识别的服务，然后通过 RPC 服务将功能提供出来，框架里面只需要调用对应的 RPC 接口就行了。

## 使用说明

Client 代码：

```python
import pylinuxauto
from pylinuxauto.config import config

# 配置OCR服务端IP
config.OCR_SERVER_IP = "192.168.0.1"
# 获取元素对象
pylinuxauto.find_element_by_ocr("中国")
```

对于一些文字的场景非常适用，可以用于**元素定位操作**

```python
pylinuxauto.find_element_by_ocr("中国").click()
pylinuxauto.find_element_by_ocr("中国").right_click()
pylinuxauto.find_element_by_ocr("中国").double_click()
pylinuxauto.find_element_by_ocr("中国").center()
pylinuxauto.find_element_by_ocr("中国").result
```

## 服务端部署

安装 PyLinuxAuto：

```bash
pip install pylinuxauto
```

创建一个目录：

```bash
mkdir ocr
cd ocr/
```

创建服务端代码文件：

```bash
vim server.py
```

写入以下内容：

```python
from pylinuxauto.ocr.server import server

server()
```

启动服务：

```bash
python3 server.py
```

## 负载均衡

只需配置多个服务器 IP 即可：

```python
import pylinuxauto
from pylinuxauto.config import config

# 配置OCR服务端IP
config.OCR_SERVER_IP = "192.168.0.1/192.168.0.2/192.168.0.3"
# 获取元素对象
pylinuxauto.find_element_by_ocr("中国")
```
