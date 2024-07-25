import os
import sys

from pylinuxauto.config import config


def install_depends():
    os.environ['QT_ACCESSIBILITY'] = '1'
    os.environ['QT_LINUX_ACCESSIBILITY_ALWAYS_ON'] = '1'

    for p in [
        "gir1.2-atspi-2.0",
        "libatk-adaptor",
        "at-spi2-core",
    ]:
        check_installed: bool = os.popen(f"dpkg -s {p}").read().strip() == ""
        if check_installed:
            os.system(f"echo '{config.PASSWORD}' | sudo -S apt install {p} -y")

    dps = [
        "python3-gi",
        "python3-pyatspi",
        "python3-cairo",
    ]
    if config.IS_IN_VIRTUALENV:
        python_path = sys.executable
        site_packages_path = os.path.join(
            os.path.dirname(os.path.dirname(python_path)),
            'lib',
            f'python{sys.version_info.major}.{sys.version_info.minor}',
            'site-packages'
        )
        for p in dps:
            wheel_name = p.split("-")[-1]
            if not os.path.exists(os.path.join(site_packages_path, wheel_name)):
                os.system(f"apt download {p} > /dev/null 2>&1")
                os.system(f"dpkg -x {p}*.deb {p}")
                os.system(f"cp -r {p}/usr/lib/python3/dist-packages/* {site_packages_path}/")
                os.system(f"rm -rf {p}*")

        git_cairo_so_name = "_gi_cairo.cpython-37m-x86_64-linux-gnu.so"
        if not os.path.exists(os.path.join(site_packages_path, "gi", git_cairo_so_name)):
            px = "python3-gi-cairo"
            os.system(f"apt download {px} > /dev/null 2>&1")
            os.system(f"dpkg -x {px}*.deb {px}")
            os.system(f"cp -r {px}/usr/lib/python3/dist-packages/gi/* {site_packages_path}/gi/")
            os.system(f"rm -rf {px}*")
    else:
        for p in dps:
            check_installed: bool = os.popen(f"dpkg -s {p}").read().strip() == ""
            if check_installed:
                os.system(f"echo '{config.PASSWORD}' | sudo -S apt install {p} -y")

    if os.popen("gsettings get org.gnome.desktop.interface toolkit-accessibility").read().strip() == "false":
        os.system("gsettings set org.gnome.desktop.interface toolkit-accessibility true")


if __name__ == '__main__':
    install_depends()