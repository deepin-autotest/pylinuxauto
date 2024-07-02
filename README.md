# PyLinuxAuto
Linux GUI Automation with Python 🔥

--------------------------

<div style="float: left"><img src="https://img.shields.io/badge/python-007CFF?style=for-the-badge&logo=python&logoColor=white"></div>
<div style="float: left">&nbsp;</div>
<div style="float: left"><img src="https://img.shields.io/badge/Linux-007CFF?style=for-the-badge&logo=linux&logoColor=white"></div>
<div style="float: left">&nbsp;</div>
<div style="float: left"><img src="https://img.shields.io/badge/Deepin-007CFF?style=for-the-badge&logo=deepin&logoColor=white"></div>

--------------------------

PyLinuxAuto 是一个用于 Linux 桌面 GUI 自动化测试的 Python 模块，支持多种元素定位方法和键鼠操作。

## 安装

```bash
pip install pylinuxauto
```

## 使用说明

4 种元素定位方法

### 使用 Accessibility 操作元素

通过 Accessibility 路径查找并操作元素，路径名称可以通过 sniff 命令查看。

```python
import pylinuxauto

pylinuxauto.find_element_by_attr_path("/dde-doc/Btn_文件管理器").click()
```

### 使用图像识别操作元素

传入一张目标图片的路径，自动在当前屏幕中查找目标图片。

```python
import pylinuxauto

pylinuxauto.find_element_by_image("~/Desktop/template.png").click()
```

### 使用 OCR 操作元素

使用传入需要识别的文本字符，使用 OCR 在当前屏幕中识别。

```python
import pylinuxauto

pylinuxauto.find_element_by_ocr("中国").click()
```

### 使用 UI 相对位移操作元素

通过将目标按钮相对于应用窗口的位置信息配置到 ini 文件里面，然后动态获取应用窗口在当前屏幕中的信息，最后计算出目标按钮在当前屏幕中的位置。

```python
import pylinuxauto

pylinuxauto.find_element_by_ui(
    appname="dde-file-manager",
    config_path="~/Desktop/ui.ini",
    btn_name="最大化按钮"
).click()
```

## 开源许可证

PyLinuxAuto 在 GPL-2.0 下发布。
