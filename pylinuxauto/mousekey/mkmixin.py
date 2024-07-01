from pylinuxauto import exceptions


class MouseKeyChainMixin:

    def __init__(self):
        self.x = None
        self.y = None
        self.result = None
        self.target_strings = None

    def _check_xy(self):
        if self.x is None and self.y is None:
            raise exceptions.ElementNotFound(f"坐标未找到 {self.target_strings}")

    def click(self):
        self._check_xy()
        from pylinuxauto.mousekey import click
        click(self.x, self.y)
        return self

    def right_click(self):
        self._check_xy()
        from pylinuxauto.mousekey import right_click
        right_click(self.x, self.y)
        return self

    def double_click(self):
        self._check_xy()
        from pylinuxauto.mousekey import double_click
        double_click(self.x, self.y)
        return self

    def center(self):
        if self.x is None and self.y is None:
            return None
        return self.x, self.y
