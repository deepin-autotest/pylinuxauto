from pylinuxauto import MouseKeyChainMixin
from pylinuxauto.ui.ui_base import ButtonCenter


class UI(MouseKeyChainMixin):

    def find_element_by_ui(
            self,
            appname,
            config_path,
            btn_name,
            number=-1,
            pause=1,
            retry=1,
            offset_x=None,
            multiplier_x=None,
            offset_y=None,
            multiplier_y=None,
    ):
        self.result = ButtonCenter(
            appname=appname,
            config_path=config_path,
            number=number,
            pause=pause,
            retry=retry
        ).btn_center(
            btn_name,
            offset_x=offset_x,
            multiplier_x=multiplier_x,
            offset_y=offset_y,
            multiplier_y=multiplier_y,
        )
        if isinstance(self.result, tuple):
            self.x, self.y = self.result
        return self
