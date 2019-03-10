
import gc

import nanogui as ng
import numpy as np

from nano3d.camera import CameraOrtho, CameraPerspective
from nano3d.renderer import RendererManager
from nano3d.scene import CameraFPSNode, CameraNode, Node, Scene, SceneManager
from nano3d.mesh import Axes, CubeWired, Grid
from nano3d.gui import MainScreen, RACanvas


class Viewer():

    def __init__(self):
        self.scene_mngr = None
        self.rend_mngr = None
        self.screen = None
        self.sim_data = None  # simulation data

        # create opengl context and ui
        ng.init()
        self.screen = MainScreen(title='Window title')
        self.screen.reg_mouse_motion_handler(self.mouse_motion_handler)
        self.screen.reg_keyboard_handler(self.keyboard_handler)

        # create a scene
        self.scene_mngr = SceneManager()
        main_scene = self.setup_scene()
        self.scene_mngr.add_scene(main_scene)  # add an empty scene
        # self.scene_mngr.add_scene_from_collada()

        # create renderers for the screen and both canvas
        # NOTE: adding a renderer needs an opengl context initialized!
        self.rend_mngr = RendererManager()
        screen_rend = self.rend_mngr.add_renderer(
            'screen', main_scene, camera='main'
        )
        topview_rend = self.rend_mngr.add_renderer(
            'topview', main_scene, camera='ortho_top'
        )
        sideview_rend = self.rend_mngr.add_renderer(
            'sideview', main_scene, camera='ortho_side'
        )

        # register screen and canvas draw callbacks
        self.screen.reg_screen_draw_handler(screen_rend.draw_handler)
        self.screen.reg_topview_canvas_draw_handler(topview_rend.draw_handler)
        self.screen.reg_sideview_canvas_draw_handler(sideview_rend.draw_handler)
        # register screen and canvas resize callbacks
        self.screen.reg_screen_resize_handler(screen_rend.resize_handler)
        self.screen.reg_topview_canvas_resize_handler(topview_rend.resize_handler)
        self.screen.reg_sideview_canvas_resize_handler(sideview_rend.resize_handler)

        self.screen.drawAll()
        self.screen.setVisible(True)

    def setup_scene(self):
        scene = Scene('main')

        axes_mesh = Axes()
        axes_node = Node('axes', axes_mesh)
        scene.add_node(axes_node)

        grid_mesh = Grid(50)
        grid_node = Node('grid', grid_mesh, position=(0.0, 0.0, 0.0))
        scene.add_node(grid_node)

        cube_mesh = CubeWired()
        cube_node0 = Node('cube0', cube_mesh, position=( 0.0, 0.0, 0.0))
        cube_node1 = Node('cube1', cube_mesh, position=(-4.5, 1.0, -4.5))
        cube_node2 = Node('cube2', cube_mesh, position=( 4.5, 1.0, -4.5))
        cube_node3 = Node('cube3', cube_mesh, position=(-0.5, 1.0,  10.0))
        scene.add_node(cube_node0)
        scene.add_node(cube_node1)
        scene.add_node(cube_node2)
        scene.add_node(cube_node3)

        self.camnode_screen = CameraFPSNode(
            CameraPerspective(), name='main', snap=0
        )
        self.camnode_screen.position = (1.0, 2.0, 3.0)
        scene.add_node(self.camnode_screen)

        camnode_top = CameraNode(CameraOrtho(), name='ortho_top')
        scene.add_node(camnode_top)

        camnode_side = CameraNode(CameraOrtho(), name='ortho_side')
        scene.add_node(camnode_side)

        return scene

    def mouse_motion_handler(self, pos, rel, button, modifiers):
        if button == ng.glfw.MOUSE_BUTTON_3:
            self.camnode_screen.rotate_in_yy(0.0025*rel[0])
            self.camnode_screen.rotate_in_xx(0.0025*rel[1])
            return True

    def keyboard_handler(self, key, scancode, action, modifiers):
        if key == ng.glfw.KEY_ESCAPE and action == ng.glfw.PRESS:
            self.screen.setVisible(False)

        if key == ng.glfw.KEY_W and action == ng.glfw.PRESS:
            self.camnode_screen.move_frwd(1)
            return True
        if key == ng.glfw.KEY_S and action == ng.glfw.PRESS:
            self.camnode_screen.move_frwd(-1)
            return True
        if key == ng.glfw.KEY_A and action == ng.glfw.PRESS:
            self.camnode_screen.move_right(-1)
            return True
        if key == ng.glfw.KEY_D and action == ng.glfw.PRESS:
            self.camnode_screen.move_right(1)
            return True
        if key == ng.glfw.KEY_SPACE and action == ng.glfw.PRESS:
            self.camnode_screen.move_up(1)
            return True
        if key == ng.glfw.KEY_LEFT_CONTROL and action == ng.glfw.PRESS:
            self.camnode_screen.move_up(-1)
            return True

        return True


    def start(self):
        ng.mainloop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type != None:
            print('Exception running RAUi!')
            print('Exc type: {}\nexc value: {}'.format(
                exc_type, exc_value
            ))
        self = None
        gc.collect()
        ng.shutdown()

def main():

    with Viewer() as raui:
        raui.start()

if __name__ == '__main__':
    main()
