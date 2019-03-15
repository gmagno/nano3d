
import numpy as np
import quaternion as qua

from nano3d.camera import CameraOrtho, CameraPerspective
from nano3d.mesh import Mesh

class SceneManager():

    def __init__(self):
        self.scenes = []
        self.active_scene = None

    def add_scene(self, scene):
        '''Adds an empty scene'''
        self.scenes.append(scene)
        if self.active_scene == None:
            self.active_scene = self.scenes[-1]

    def add_scene_from_collada(self, filepath):
        '''Adds a scene from a collada file (.dae)'''
        scene = Scene()
        # parse collada file and populate scene
        # ...
        self.scenes.append(scene)

    # TODO: convert to property
    def get_active_scene(self):
        return self.active_scene

    def get_scene(self, name):
        for s in self.scenes:
            if s.name == name:
                return s
        return None  # TODO: potentially raise an exception

class Scene():
    def __init__(self, name):
        self.name = name
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)


class Node():
    '''The Node object maintains the position, orientation and scaling factor of
    a mesh linked to it. All the applied transformations impact the respective
    mesh geometry.
    '''
    def __init__(self, name,
            mesh=None,
            scale=(1.0, 1.0, 1.0),
            orientation=(1.0, 0.0, 0.0, 0.0),  # quaternion (w, x, y, z)
            position=(0.0, 0.0, 0.0),
    ):
        '''Instantiate a Node object.

        Parameters
        ----------
        name: a string that identifies the node.
            mesh: a `Mesh` object with geometry data: vertices, indices,
            normals, colors, etc.
        scale: a 3-tuple or numpy.ndarray with scaling factors for x, y, z.
        orientation: a 4-tuple or a numpy.quaternion. Quaternions may be
            created, for instance, from a rotation vector as follows
            `rotx = qua.from_rotation_vector((np.pi/2, 0.0, 0.0))`, which
            represents a rotation of 90deg in local space around xx axis. A
            quaternion object can then be rotated by multiplying with another
            quaternion object, e.g: `rot = q * rotx`. Finally a rotation matrix
            can be generated with `qua.as_rotation_matrix(rot)`.
        position: a 3-tuple of numpy.ndarray representing the position of the
            node in world coordinates.
        visible: a boolean for whether the node should be rendered.

        Raises
        ------
        ValueError: if any of the input parameters does not respect its type.
        '''
        self.name = name if isinstance(name, str) else None
        self.mesh = mesh if isinstance(mesh, Mesh) or mesh == None else -1
        if self.name is None or self.mesh == -1:
            raise ValueError(
                'name and mesh must be a string and an instance of Mesh'
                'respectively.'
            )

        self.position = position
        self.orientation = orientation
        self.scale = scale
        self.visible = True  # whether this node is visible for rendering

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if type(position) in [np.ndarray, tuple] and len(position) == 3:
            self._position = np.array(position, dtype=np.float32)
        else:
            raise ValueError(
                'position must be either a 3-tuple or an numpy.ndarray'
            )

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        if type(orientation) == np.quaternion:
            self._orientation = orientation
        elif type(orientation) == tuple and len(orientation) == 4:
            self._orientation = np.quaternion(*orientation)
        else:
            raise ValueError(
                'orientation must be either a 4-tuple or an numpy.quaternion'
            )

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = np.array(scale, dtype=np.float32)
        if type(scale) in [np.ndarray, tuple] and len(scale) == 3:
            self._scale = np.array(scale, dtype=np.float32)
        else:
            raise ValueError(
                'scale must be either a 3-tuple or an numpy.ndarray'
            )

    def model_mat(self):
        '''Returns the model matrix, i.e: translation * rotation * scaling.'''
        return \
            self.translation_mat() @ self.rotation_mat() @ self.scaling_mat()

    def translation_mat(self):
        '''Returns the translation matrix for this node'''
        translation = np.eye(4, dtype=np.float32)
        translation[:-1, -1] = self.position
        return translation

    def rotation_mat(self):
        '''Returns the rotation matrix for this node'''
        rotation = np.eye(4, dtype=np.float32)
        rotation[:-1, :-1] = qua.as_rotation_matrix(self.orientation)
        return rotation

    def scaling_mat(self):
        '''Returns the scaling matrix for this node'''
        return np.diag(np.append(self.scale, 1.0))

    def rotate(self, pitch, yaw, roll):
        rot = qua.from_rotation_vector((pitch, yaw, roll))
        self.orientation *= rot


class CameraNode(Node):
    def __init__(self, camera, name, mesh=None, *args, **kwargs):
        self.camera = camera
        super(CameraNode, self).__init__(name, mesh, *args, **kwargs)

    def view_mat(self):
        '''Returns the view matrix for this camera node.'''
        trans = self.translation_mat()
        trans[:-1, 3] = -trans[:-1, 3]  # <-- efficient matrix inversion
        rot = self.rotation_mat()
        rot = rot.T                     # <-- efficient matrix inversion

        self.view = rot @ trans
        return self.view

    def projection_mat(self, size=None):
        '''Returns the projection matrix for this camera node

        Parameters
        ----------
        size: a 2-tuple with width and height of the viewprt. It is an optional
            parameter because cameras may define a fixed aspect ratio which
            should be respected regardless of the viewport size. Only if the
            camera aspect ratio is None the viewport size is needed, in which
            case an exception is raised if size is None.
        '''
        if isinstance(self.camera, CameraPerspective):
            proj_mat = self.persp_projection(size)
        elif isinstance(self.camera, CameraOrtho):
            proj_mat = self.ortho_projection(size)
        else:
            # TODO: check if an exception should be raised, or if this
            # verification should be done upstream in the constructor
            pass
        return proj_mat

    def ortho_projection(self, size=None):
        '''Returns a 4x4 projection matrix for an orthographic camera.

        Parameters
        ----------
        size: a 2-tuple with width and height of the viewprt. Check
        `projection()` for more details.

        Raises
        ------
        ValueError: raised when size is None and the camera does not
            specify ans aspect ratio.
        '''
        projw = self.camera.projw
        projh = self.camera.projh
        if projh == None:
            try:
                aspect = size[0] / size[1]
            except TypeError:
                raise ValueError(
                    'Bad size, expected a 2-tuple, but got: {}'.format(size)
                )
            projh = projw / aspect

        left, right, bottom, top = -projw/2., projw/2., -projh/2., projh/2.
        # near, far = 0, 5  # TODO: should be determined by some camera parameter
        near, far = self.camera.near, self.camera.far  # TODO: should be determined by some camera parameter
        tx = -(right+left)/(right-left)
        ty = -(top+bottom)/(top-bottom)
        tz = -(far+near)/(far-near)
        self.projection = np.eye(4)
        self.projection[0, 0] = 2/(right-left)
        self.projection[1, 1] = 2/(top-bottom)
        self.projection[2, 2] = -2/(far-near)
        self.projection[:-1, -1] = np.array((tx, ty, tz))
        return self.projection

    def persp_projection(self, size=None):
        '''Returns a 4x4 projection matrix for a perspective camera.

        Parameters
        ----------
        size: a 2-tuple with width and height of the viewprt. Check
        `projection()` for more details.

        Raises
        ------
        ValueError: raised when size is None and the camera does not
            specify ans aspect ratio.
        '''
        aspect = self.camera.aspect
        if aspect == None:
            try:
                w, h = size
            except TypeError:
                raise ValueError(
                    'Bad size, expected a 2-tuple, but got: {}'.format(size)
                )
            aspect = w / h
        n = self.camera.near
        f = self.camera.far
        fovy = self.camera.fovy
        c = 1/np.tan(fovy/2)
        self.projection = np.array([
            [ c/aspect, 0.0,  0.0,          0.0         ],
            [ 0.0,      c,    0.0,          0.0         ],
            [ 0.0,      0.0,  (f+n)/(n-f),  2*n*f/(n-f) ],
            [ 0.0,      0.0, -1.0,          0.0         ],
        ], dtype=np.float32)
        return self.projection

class CameraFPSNode(CameraNode):

    def __init__(self, camera, name, mesh=None, snap=None, *args, **kwargs):
        '''
        Parameters:
        snap: int or None. Rounds the positon to `snap` number of decimals, e.g
            if set to 0, the camera will snap to integer positions. If None the
            camera moves freely.
        '''
        self.camera = camera
        self.snap = snap
        super(CameraNode, self).__init__(name, mesh, *args, **kwargs)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if type(position) in [np.ndarray, tuple] and len(position) == 3:
            self._position = np.array(position, dtype=np.float32)
            if self.snap != None:
                self._position = np.around(self._position, decimals=self.snap)
        else:
            raise ValueError(
                'position must be either a 3-tuple or an numpy.ndarray'
            )

    def rotate_in_xx(self, pitch):
        rot = qua.from_rotation_vector((pitch, 0.0, 0.0))
        self.orientation *= rot

    def rotate_in_yy(self, yaw):
        rot = qua.from_rotation_vector((0.0, yaw, 0.0))
        self.orientation = rot * self.orientation

    def move_frwd(self, amount):
        frwd = -amount*self.view_mat()[2, :-1]
        frwd[1] = 0.0
        self.position += frwd


    def move_right(self, amount):
        right = amount*self.view_mat()[0, :-1]
        right[1] = 0.0
        self.position += right

    def move_up(self, amount):
        self.position += amount*np.array([0.0, 1.0, 0.0])


class LightNode(Node):
    pass
