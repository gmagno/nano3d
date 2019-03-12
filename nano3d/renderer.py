
import nanogui as ng
import numpy as np


class RendererManager():

    def __init__(self):
        self.renderers = []

    def add_renderer(self, name, scene, camera=''):
        '''Adds a scene renderer for a specific camera.
        By default uses the first camera in the scene.'''
        renderer = Renderer(name, scene, camera)
        self.renderers.append(renderer)
        return renderer

    def remove_renderer(self, name):
        for i, r in enumerate(self.renderers):
            if r.name == name:
                del self.renderers[i]

    def get_renderer(name):
        for r in self.renderers:
            if r.name == name:
                return r
        return None


class Renderer():

    def __init__(self, name, scene, camera):
        '''
        Raises
        ------
        InvalidCameraNodeError: when `camera` does not match any of the
            available cameras.
        '''
        self.name = name
        self.scene = scene
        self.camera_name = camera
        self.camera_node = None
        self.shaders = []
        self.projection = np.eye(4)

        for node in scene.nodes:
            if node.name == self.camera_name:
                self.camera_node = node
                self.projection = self.camera_node.projection_mat(size=(1, 1))
            if node.mesh is None:
                continue  # may be a node without geometry, which is okay
            shader = ng.GLShader()
            shader.initFromFiles(
                'generic',
                'data/shaders/generic.vs.glsl',
                'data/shaders/generic.fs.glsl',
            )
            shader.bind()
            shader.uploadIndices(node.mesh.indices)
            shader.uploadAttrib('position', node.mesh.positions)
            shader.uploadAttrib('color', node.mesh.colors)
            self.shaders.append(shader)
        if self.camera_node == None:
            # the specified camera does not match any of the available cameras
            # in the scene
            raise MissingCameraNodeError()

    def draw_handler(self):
        '''Callback that gets called when rendering is needed'''
        for i, node in enumerate(self.scene.nodes):
            if node.mesh is None:
                continue  # may be a node without geometry, which is okay
            model = node.model_mat()
            view = self.camera_node.view_mat()
            positions = node.mesh.positions
            self.shaders[i].bind()
            self.shaders[i].setUniform(
                'mvp', self.projection @ view @ model
            )
            ng.gl.Enable(ng.gl.DEPTH_TEST)
            ng.gl.Enable(ng.gl.CULL_FACE)
            self.shaders[i].drawIndexed(ng.gl.LINES, 0, node.mesh.no_indices)
            ng.gl.Disable(ng.gl.CULL_FACE)
            ng.gl.Disable(ng.gl.DEPTH_TEST)

    def resize_handler(self, size):
        '''Callback that gets called when the rendering canvas is resized'''
        self.projection = self.camera_node.projection_mat(size)


class MissingCameraNodeError(Exception):
    pass