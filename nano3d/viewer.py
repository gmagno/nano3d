
import gc
import time

import nanogui as ng
import numpy as np

from nano3d.camera import CameraOrtho, CameraPerspective
from nano3d.renderer import RendererManager
from nano3d.scene import CameraFPSNode, CameraNode, Node, Scene, SceneManager
from nano3d.mesh import Axes, CubeWired, Dae, Grid
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

        # self.ref_node = Node('ref', axes_mesh)
        # self.ref_node.position = (8, 1, -10)
        # scene.add_node(self.ref_node)

        # dae_mesh = Dae('data/primitives/cube1.dae')
        # dae_node = Node('dae', dae_mesh)
        # scene.add_node(dae_node)


        grid_mesh = Grid(100)
        grid_node = Node('grid', grid_mesh, position=(0.0, 0.0, 0.0))
        scene.add_node(grid_node)

        cube_mesh = CubeWired()
        # cube_node0 = Node('cube0', cube_mesh, position=( 0.0, 0.0, -1.0))
        # cube_node1 = Node('cube1', cube_mesh, position=(-1.0, 0.0, -1.0))
        cube_node2 = Node('cube2', cube_mesh, position=( 4.5, 1.0, -4.5))
        # cube_node3 = Node('cube3', cube_mesh, position=(-0.5, 1.0,  10.0))
        cube_node4 = Node('cube4', cube_mesh, position=( 2.0, 0.0, -10.0))
        cube_node5 = Node('cube5', cube_mesh, position=( 1.0, 0.0, -10.0))
        # scene.add_node(cube_node0)
        # scene.add_node(cube_node1)
        scene.add_node(cube_node2)
        # scene.add_node(cube_node3)
        scene.add_node(cube_node4)
        scene.add_node(cube_node5)

        self.camnode_screen = CameraFPSNode(
            CameraPerspective(), name='main', snap=0
        )
        self.camnode_screen.position = (2.0, 3.0, 0.0)
        scene.add_node(self.camnode_screen)

        self.camnode_top = CameraFPSNode(CameraOrtho(near=-3, ), name='ortho_top')
        self.camnode_top.position = self.camnode_screen.position
        self.camnode_top.rotate(pitch=-np.pi/2., yaw=0.0, roll=0.0)
        scene.add_node(self.camnode_top)

        self.camnode_side = CameraNode(CameraOrtho(near=-3), name='ortho_side')
        self.camnode_side.position = self.camnode_screen.position
        self.camnode_side.rotate(pitch=0.0, yaw=np.pi/2, roll=0.0)
        scene.add_node(self.camnode_side)

        self.screen.scenenodes.load_scene(scene)

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

        if key == ng.glfw.KEY_LEFT and action == ng.glfw.PRESS:
            self.ref_node.rotate(pitch=0.0, yaw=np.pi/16., roll=0.0)
        if key == ng.glfw.KEY_RIGHT and action == ng.glfw.PRESS:
            self.ref_node.rotate(pitch=0.0, yaw=-np.pi/16., roll=0.0)
        if key == ng.glfw.KEY_UP and action == ng.glfw.PRESS:
            self.ref_node.rotate(pitch=np.pi/16, yaw=0.0, roll=0.0)
        if key == ng.glfw.KEY_DOWN and action == ng.glfw.PRESS:
            self.ref_node.rotate(pitch=-np.pi/16, yaw=0.0, roll=0.0)


        self.camnode_top.position = self.camnode_screen.position
        self.camnode_side.position = self.camnode_screen.position

        camview_m = np.around(self.camnode_screen.view_mat(), decimals=1)
        camrot_m = np.around(self.camnode_screen.rotation_mat(), decimals=1)
        camtra_m = np.around(self.camnode_screen.translation_mat(), decimals=1)
        self.screen.camview_label.set_array(camview_m)
        self.screen.camrot_label.set_array(camrot_m)
        self.screen.camtra_label.set_array(camtra_m)

        # refrot_m = np.around(self.ref_node.rotation_mat(), decimals=1)
        # reftra_m = np.around(self.ref_node.translation_mat(), decimals=1)
        # self.screen.refrot_label.set_array(refrot_m)
        # self.screen.reftra_label.set_array(reftra_m)

        self.screen.performLayout()
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
