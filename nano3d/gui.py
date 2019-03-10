
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
        self.setBackground(ng.Color(0.2, 0.10, 0.10, 0.1))

        # screen layout
        screen_layout = ng.BoxLayout(
            ng.Orientation.Horizontal, ng.Alignment.Minimum, 2, 10
        )
        self.setLayout(screen_layout)

        # ortho window layout
        self.ortho_win = ng.Window(self, 'Ortho Projection')
        ortho_layout = ng.BoxLayout(
            ng.Orientation.Vertical, ng.Alignment.Fill, 0, 0
        )
        self.ortho_win.setLayout(ortho_layout)

        self.topview_panel = ng.Widget(self.ortho_win)
        self.sideview_panel = ng.Widget(self.ortho_win)

        self.win = ng.Window(self, "Control")
        self.win.setLayout(ng.GroupLayout())
        self.win.setSize((100, 100))
        ng.Label(self.win, "Push buttons", "sans-bold")
        b = ng.Button(self.win, "Plain button")

        # initialize the view and projection matrices for the main camera
        # self.cam = Camera(width=100, height=100, fovy=np.pi/3, near=.1, far=100)
        # self.cam.update_view()
        # self.projection = self.cam.update_projection(
        #     width=self.width(), height=self.height()
        # )

        # create the scene
        # self.scene = Scene()

        # create canvas
        self.topview_canvas = RACanvas(
            self.topview_panel,
            None, (100, 100), cam_t='ortho'
        )
        self.sideview_canvas = RACanvas(
            self.sideview_panel,
            None, (100, 100), cam_t='ortho'
        )

        self.topview_canvas.setBackgroundColor(ng.Color(0.10, 0.2, 0.10, 0.1))
        self.sideview_canvas.setBackgroundColor(ng.Color(0.10, 0.10, 0.2, 0.1))

        # self.cam.near = .1
        # self.topview_canvas.cam.near = -30
        # self.sideview_canvas.cam.near = -30
        # self.cam.far = 100
        # self.topview_canvas.cam.far = 30
        # self.sideview_canvas.cam.far = 30

        # set cameras linear positions
        # self.cam.pos = (0, 1, 4)
        # self.topview_canvas.cam.pos = (3, 2, 3)
        # self.sideview_canvas.cam.pos = (3, 2, 3)

        # set orthographic cameras angular positions
        # self.topview_canvas.cam.angpos = (-np.pi/2, 0.0)
        # self.sideview_canvas.cam.angpos = (0.0, np.pi/2)

        # self.cam.update_view()
        # self.topview_canvas.cam.update_view()
        # self.sideview_canvas.cam.update_view()

    def resizeEvent(self, size):
        w, h = size
        # self.cam.update_projection(width=w, height=h)

        self.win.setSize((w/8, h))
        self.topview_panel.setSize(np.array([w/5, h/2-20], dtype=np.int32))
        self.sideview_panel.setSize(np.array([w/5, h/2-20], dtype=np.int32))
        self.topview_canvas.set_size(self.topview_panel.size())
        self.sideview_canvas.set_size(self.sideview_panel.size())

        self.screen_resize_handler(size)
        self.topview_canvas.resize_handler(self.topview_panel.size())
        self.sideview_canvas.resize_handler(self.sideview_panel.size())

        self.performLayout()
        return super().resizeEvent(size)

    def reg_screen_draw_handler(self, handler):
        self.screen_draw_handler = handler

    def reg_topview_canvas_draw_handler(self, handler):
        self.topview_canvas.reg_draw_handler(handler)

    def reg_sideview_canvas_draw_handler(self, handler):
        self.sideview_canvas.reg_draw_handler(handler)

    def reg_screen_resize_handler(self, handler):
        self.screen_resize_handler = handler

    def reg_topview_canvas_resize_handler(self, handler):
        self.topview_canvas.reg_resize_handler(handler)

    def reg_sideview_canvas_resize_handler(self, handler):
        self.sideview_canvas.reg_resize_handler(handler)

    def drawContents(self):
        # self.scene.draw(self.cam.view, self.cam.projection)
        self.screen_draw_handler()
        super(MainScreen, self).drawContents()


    def reg_mouse_motion_handler(self, handler):
        self.mouse_motion_handler = handler

    def mouseMotionEvent(self, pos, rel, button, modifiers):
        return self.mouse_motion_handler(pos, rel, button, modifiers)

    def reg_keyboard_handler(self, handler):
        self.keyboard_handler = handler

    def keyboardEvent(self, key, scancode, action, modifiers):
        return self.keyboard_handler(key, scancode, action, modifiers)
        # if super(MainScreen, self).keyboardEvent(
        #         key, scancode, action, modifiers):
        #     return True
        # if key == ng.glfw.KEY_ESCAPE and action == ng.glfw.PRESS:
        #     self.setVisible(False)
        #     return True

        # if key == ng.glfw.KEY_W and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(0, 0, 1))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True
        # if key == ng.glfw.KEY_S and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(0, 0, -1))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True
        # if key == ng.glfw.KEY_A and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(-1, 0, 0))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True
        # if key == ng.glfw.KEY_D and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(1, 0, 0))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True
        # if key == ng.glfw.KEY_SPACE and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(0, 1, 0))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True
        # if key == ng.glfw.KEY_LEFT_CONTROL and action == ng.glfw.PRESS:
        #     self.cam.update_view(lind=(0, -1, 0))
        #     self.topview_canvas.cam.pos = self.cam.pos
        #     self.sideview_canvas.cam.pos = self.cam.pos
        #     self.topview_canvas.cam.update_view()
        #     self.sideview_canvas.cam.update_view()
        #     return True

        return True

    # def mouseMotionEvent(self, pos, rel, button, modifiers):
    #     if button == ng.glfw.MOUSE_BUTTON_3:
    #         self.cam.update_view(angd=rel)
    #         return True


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

        # by default a perspective camera is created but an orthographic one
        # can also be used
        # cam_args = dict(
        #     width=size[0], height=size[1],
        #     fovy=np.pi/3, near=.1, far=100,
        # )
        # if cam_t == 'ortho':
        #     w = 30.*size[0]/size[1]
        #     h = 30.
        #     cam_args = dict(
        #         pos=(0.0, 0.0, 0.0),
        #         width=size[0], height=size[1],
        #         left=-w/2., right=w/2.,
        #         bottom=-h/2., top=h/2.,
        #         near=-5, far=5,
        #     )
        # self.cam = Camera(**cam_args)

        # initialize the view and projection matrices
        # self.cam.update_view()
        # self.projection = self.cam.update_projection(
        #     width=self.width(), height=self.height()
        # )

        # set the scene
        # self.scene = scene

    def set_size(self, size):
        self.setSize(size)
        self.resize_handler(size)
        # if self.cam_t == 'ortho':
        #     w = 80.*size[0]/size[1]
        #     h = 80.
        #     self.cam.update_projection_ortho(
        #         width=size[0], height=size[1],
        #         left=-w/2., right=w/2,
        #         bottom=-h/2, top=h/2,
        #     )
        # else:
        #     self.cam.update_projection(width=size[0], height=size[1])

    def reg_draw_handler(self, handler):
        self.draw_handler = handler

    def reg_resize_handler(self, handler):
        self.resize_handler = handler

    def drawGL(self):
        self.draw_handler()
        # self.scene.draw(self.cam.view, self.cam.projection)
