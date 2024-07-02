import os
import sys

from pylinuxauto.config import config


def install_depends():
    python_path = sys.executable
    site_packages_path = os.path.join(
        os.path.dirname(os.path.dirname(python_path)),
        'lib',
        f'python{sys.version_info.major}.{sys.version_info.minor}',
        'site-packages'
    )
    dps = [
        "python3-pil",
    ]
    if config.IS_IN_VIRTUALENV:
        for p in dps:
            wheel_name = p.split("-")[-1].upper()
            if not os.path.exists(os.path.join(site_packages_path, wheel_name)):
                os.system(f"apt download {p} > /dev/null 2>&1")
                os.system(f"dpkg -x {p}*.deb {p}")
                os.system(f"cp -r {p}/usr/lib/python3/dist-packages/* {site_packages_path}/")
                os.system(f"rm -rf {p}*")
    else:
        for p in dps:
            check_installed: bool = os.popen(f"dpkg -l {p}").read().strip().startswith("dpkg-query")
            if check_installed:
                os.system(f"echo '{config.PASSWORD}' | sudo -S apt install {p}")


if __name__ == '__main__':
    install_depends()
