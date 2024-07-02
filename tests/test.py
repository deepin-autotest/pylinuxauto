import pylinuxauto


def test_attr_001():
    pylinuxauto.find_element_by_attr_path("/dde-dock/Btn_文件管理器").click()

def test_image_001():
    from pylinuxauto.config import config
    config.IMAGE_SERVER_IP = "10.8.11.139"
    pylinuxauto.find_element_by_image("~/Desktop/1.png").click()