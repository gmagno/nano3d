
import gc
import time

import nanogui as ng
import numpy as np

from example.example1.gui import MainScreen
from nano3d.camera import CameraOrtho, CameraPerspective
from nano3d.mesh import Axes, CubeWired, Grid
from nano3d.renderer import RendererManager
from nano3d.scene import CameraFPSNode, CameraNode, Node, Scene, SceneManager


class Viewer():

    def __init__(self):
        self.scene_mngr = None
        self.rend_mngr = None
        self.screen = None

        # create opengl context and ui
        ng.init()
        self.screen = MainScreen(title='Window title')

        # register mouse and keyboard event handlers
        self.screen.reg_mouse_motion_handler(self.mouse_motion_handler)
        self.screen.reg_keyboard_handler(self.keyboard_handler)

        # create a scene
        self.scene_mngr = SceneManager()
        main_scene = self.setup_scene()
        self.scene_mngr.add_scene(main_scene)

        # create renderers for the screen
        # NOTE: adding a renderer needs an opengl context initialized!
        self.rend_mngr = RendererManager()
        screen_rend = self.rend_mngr.add_renderer(
            'screen', main_scene, camera='main'
        )

        # register screen draw callback
        self.screen.reg_screen_draw_handler(screen_rend.draw_handler)

        # register screen resize callback
        self.screen.reg_screen_resize_handler(screen_rend.resize_handler)

        self.screen.drawAll()
        self.screen.setVisible(True)

    def setup_scene(self):
        scene = Scene('main')
        scene.add_node(Node('axes', Axes()))
        scene.add_node(Node('cube', CubeWired()))
        self.camnode_screen = CameraFPSNode(
            CameraPerspective(), name='main', snap=0
        )
        self.camnode_screen.position = (2.0, 1.0, 5.0)
        scene.add_node(self.camnode_screen)
        return scene

    def mouse_motion_handler(self, pos, rel, button, modifiers):
        if button == ng.glfw.MOUSE_BUTTON_3:
            self.camnode_screen.rotate_in_yy(-0.0025*rel[0])
            self.camnode_screen.rotate_in_xx(-0.0025*rel[1])
            return True

    def keyboard_handler(self, key, scancode, action, modifiers):
        if key == ng.glfw.KEY_ESCAPE and action == ng.glfw.PRESS:
            self.screen.setVisible(False)
            return True

        if key == ng.glfw.KEY_W and action == ng.glfw.PRESS:
            self.camnode_screen.move_frwd(1)
        if key == ng.glfw.KEY_S and action == ng.glfw.PRESS:
            self.camnode_screen.move_frwd(-1)
        if key == ng.glfw.KEY_A and action == ng.glfw.PRESS:
            self.camnode_screen.move_right(-1)
        if key == ng.glfw.KEY_D and action == ng.glfw.PRESS:
            self.camnode_screen.move_right(1)
        if key == ng.glfw.KEY_SPACE and action == ng.glfw.PRESS:
            self.camnode_screen.move_up(1)
        if key == ng.glfw.KEY_LEFT_CONTROL and action == ng.glfw.PRESS:
            self.camnode_screen.move_up(-1)

        if key == ng.glfw.KEY_J and action == ng.glfw.PRESS:
            self.camnode_screen.rotate_in_yy(np.pi/16.)
        if key == ng.glfw.KEY_L and action == ng.glfw.PRESS:
            self.camnode_screen.rotate_in_yy(-np.pi/16.)
        if key == ng.glfw.KEY_I and action == ng.glfw.PRESS:
            self.camnode_screen.rotate_in_xx(np.pi/16.)
        if key == ng.glfw.KEY_K and action == ng.glfw.PRESS:
            self.camnode_screen.rotate_in_xx(-np.pi/16.)

        self.screen.performLayout()
        return True


    def start(self):
        ng.mainloop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type != None:
            print('Exception running the Viewer!')
            print('Exc type: {}\nexc value: {}'.format(
                exc_type, exc_value
            ))
        self = None
        gc.collect()
        ng.shutdown()

def run():
    with Viewer() as viewer:
        viewer.start()

def run_detached():
    viewer = Viewer()
    time.sleep(2)  # <-- otherwise I get a SIGSEGV: address boundary error
    h = ng.mainloop(detach=viewer.screen)
    h.join()
    viewer = None
    gc.collect()
    ng.shutdown()

def main():
    run()
    # run_detached()

if __name__ == '__main__':
    main()
