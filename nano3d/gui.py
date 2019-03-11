
import nanogui as ng
import numpy as np

from nano3d.globj import Axes, Cube, Grid
from nano3d.scene import Scene


class MainScreen(ng.Screen):

    def __init__(self, title):
        super(MainScreen, self).__init__(
            (800, 600),         # window size
            title,              # window title
            True,               # resizable (boolean)
            False               # fullscreen (boolean)
        )
        self.setBackground(ng.Color(0.12, 0.10, 0.10, 0.1))

        # screen
        # screen_layout = ng.BoxLayout(
        #     ng.Orientation.Horizontal, ng.Alignment.Minimum, 2, 10
        # )
        # self.setLayout(screen_layout)

        # ortho window
        self.ortho_win = ng.Window(self, 'Ortho Projection')
        ortho_layout = ng.BoxLayout(
            ng.Orientation.Vertical, ng.Alignment.Fill, 0, 0
        )
        self.ortho_win.setLayout(ortho_layout)
        self.topview_panel = ng.Widget(self.ortho_win)
        self.sideview_panel = ng.Widget(self.ortho_win)

        # camera window
        self.cam_win = ng.Window(self, 'Camera')
        self.cam_win.setLayout(ng.GroupLayout())
        self.cam_win.setSize((100, 100))
        self.camview_label = MatrixLabel(self.cam_win, caption='View Matrix')
        self.camrot_label = MatrixLabel(self.cam_win, caption='Rotation Matrix')
        self.camtra_label = MatrixLabel(self.cam_win, caption='Translation Matrix')

        # reference object window
        self.ref_win = ng.Window(self, 'Reference object')
        self.ref_win.setLayout(ng.GroupLayout())
        self.ref_win.setSize((100, 100))
        self.refrot_label = MatrixLabel(self.ref_win, caption='Rotation Matrix')
        self.reftra_label = MatrixLabel(self.ref_win, caption='Translation Matrix')


        # create canvas
        self.topview_canvas = RACanvas(
            self.topview_panel,
            None, (100, 100), cam_t='ortho'
        )
        self.sideview_canvas = RACanvas(
            self.sideview_panel,
            None, (100, 100), cam_t='ortho'
        )
        self.topview_canvas.setBackgroundColor(ng.Color(0.10, 0.12, 0.10, 0.1))
        self.sideview_canvas.setBackgroundColor(ng.Color(0.10, 0.10, 0.12, 0.1))

    ##  Draw handling  ################
    def reg_screen_draw_handler(self, handler):
        self.screen_draw_handler = handler

    def reg_topview_canvas_draw_handler(self, handler):
        self.topview_canvas.reg_draw_handler(handler)

    def reg_sideview_canvas_draw_handler(self, handler):
        self.sideview_canvas.reg_draw_handler(handler)

    def drawContents(self):
        self.screen_draw_handler()
        super(MainScreen, self).drawContents()

    ##  Resize handling  ##############
    def reg_screen_resize_handler(self, handler):
        self.screen_resize_handler = handler

    def reg_topview_canvas_resize_handler(self, handler):
        self.topview_canvas.reg_resize_handler(handler)

    def reg_sideview_canvas_resize_handler(self, handler):
        self.sideview_canvas.reg_resize_handler(handler)

    def resizeEvent(self, size):
        w, h = size
        # self.win.setSize((w/8, h))
        self.topview_panel.setSize(np.array([w/5, h/2-20], dtype=np.int32))
        self.sideview_panel.setSize(np.array([w/5, h/2-20], dtype=np.int32))
        self.topview_canvas.set_size(self.topview_panel.size())
        self.sideview_canvas.set_size(self.sideview_panel.size())
        self.screen_resize_handler(size)
        self.topview_canvas.resize_handler(self.topview_panel.size())
        self.sideview_canvas.resize_handler(self.sideview_panel.size())
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


class RACanvas(ng.GLCanvas):
    def __init__(self, parent,
            scene, size=(100, 100), cam_t='persp'
    ):
        ''' Creates an OpenGL canvas with a viewport size of `size` pixels, a
        2d np.array and the associated camera. `cam_t` can be one of: {'persp',
        'ortho'}, for perspective or orthographic camera type, respectively.
        '''
        super(RACanvas, self).__init__(parent)
        # self.cam_t = cam_t
        self.size = np.array(size)
        self.setSize(size)
        self.setBackgroundColor(ng.Color(0.3, 0.3, 0.3, 1.0))

    def set_size(self, size):
        self.setSize(size)
        self.resize_handler(size)

    def reg_draw_handler(self, handler):
        self.draw_handler = handler

    def reg_resize_handler(self, handler):
        self.resize_handler = handler

    def drawGL(self):
        self.draw_handler()


class MatrixLabel(ng.Widget):
    def __init__(
            self, parent, caption, array=None, fontSize=30, *args, **kwargs
        ):
        super(MatrixLabel, self).__init__(parent, *args, **kwargs)
        self.setLayout(ng.GroupLayout())
        ng.Label(self, caption, 'sans-bold', fontSize=fontSize)
        self.labels = []
        self.font_size = fontSize
        if array != None:
            self.set_array(array)

    def set_array(self, array):
        if len(array.shape) != 2:
            raise ValueError('MatrixLabel must be passed a 2D shaped arraya')
        self.array = array
        for l in self.labels:
            self.removeChild(l)
        self.labels = []
        for row in array:
            fmtline = ''
            for e in row:
                fmtline += ' %4.1f '
            fmtline = fmtline % (tuple(row))
            # fmtline = ' %4.1f  %4.1f  %4.1f  %4.1f ' % ( tuple(row) )
            self.labels.append(ng.Label(
                self, fmtline, fontSize=int(0.9*self.font_size)
            ))
