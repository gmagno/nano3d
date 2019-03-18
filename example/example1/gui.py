
import nanogui as ng
import numpy as np

from nano3d.scene import Scene


class MainScreen(ng.Screen):

    def __init__(self, title):
        super(MainScreen, self).__init__(
            (800, 600),         # window size
            title,              # window title
            True,               # resizable (boolean)
            False               # fullscreen (boolean)
        )
        # initialize handlers
        self.screen_draw_handler = lambda : None
        self.screen_resize_handler = lambda size: None
        self.mouse_motion_handler = lambda pos, rel, button, modifiers: None
        self.keyboard_handler = lambda key, scancode, action, modifiers: None

        # screen properties
        self.setBackground(ng.Color(0.1, 0.1, 0.1, 1.0))

    ##  Draw handling  ################
    def reg_screen_draw_handler(self, handler):
        self.screen_draw_handler = handler

    def drawContents(self):
        self.screen_draw_handler()
        super(MainScreen, self).drawContents()

    ##  Resize handling  ##############
    def reg_screen_resize_handler(self, handler):
        self.screen_resize_handler = handler

    def resizeEvent(self, size):
        self.screen_resize_handler(size)
        self.performLayout()
        return super().resizeEvent(size)

    ##  Mouse handling  ###############
    def reg_mouse_motion_handler(self, handler):
        self.mouse_motion_handler = handler

    def mouseMotionEvent(self, pos, rel, button, modifiers):
        return self.mouse_motion_handler(pos, rel, button, modifiers)

    ##  Keyboard handling  ############
    def reg_keyboard_handler(self, handler):
        self.keyboard_handler = handler

    def keyboardEvent(self, key, scancode, action, modifiers):
        return self.keyboard_handler(key, scancode, action, modifiers)

