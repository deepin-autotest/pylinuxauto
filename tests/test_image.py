from pylinuxauto.image import Image

from pylinuxauto.config import config

config.IMAGE_SERVER_IP = "10.8.12.216"

def test_image():
    a = Image().find_element_by_image("~/Desktop/1.png").result
    print(a)