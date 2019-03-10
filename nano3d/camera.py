
import numpy as np


class CameraPerspective():
    def __init__(self,
            aspect=None, fovy=np.pi/3.,
            near=0.1, far=100.,
            *args, **kwargs
    ):
        '''
        Parameters
        ----------
        aspect: None means the Renderer should adapt projection to the size of
            the viewport.
        '''
        super(CameraPerspective, self).__init__(*args, **kwargs)
        # projection properties
        self.aspect = aspect  # aspect ratio
        self.fovy = fovy      # field of view angle
        self.near = near      # frustum near clipping plane
        self.far = far        # frustum far clipping plane


class CameraOrtho():
    def __init__(self, projw=30, projh=None, *args, **kwargs):
        '''

        Parameters
        ----------
        projw:
        projh: if left None, projh should be determined from the viewport aspect
        ratio, i.e: projh = projw / aspect.
        '''
        super(CameraOrtho, self).__init__(*args, **kwargs)
        # projection properties
        self.projw = projw  # projection width
        self.projh = projh  # projection height


class Camera_old():
    def __init__(self,
            pos=(0.0, 0.0, 0.0),
            sens=(0.002, 0.002),
            width=400, height=400, near=0.1, far= 100, fovy=np.pi/6,
            left=-5.0, right=5.0, bottom=-5.0, top=5.0
    ):
        '''Instantiates a camera object.
        The camera initial position is passed in `pos` as a vec3.
        The argument `sens` represents the sensibility to changes of `angd` in
        self.update_view(), it is a vec2 (sensx, sensy).
        The projection matrix is computed with `near`, `far`, `fovy`, `width`
        and `height` which represent the frustum near and far plane, field of
        view angle in radians and the viewport width and height, respectively.
        '''
        width = 1 if width <= 0 else width
        height = 1 if height <= 0 else height
        self._pos = np.array(pos)
        self.sens = np.array(sens)  # mouse sensitivity (x, y)
        self.width, self.height, aspect = width, height, width/height
        self.near, self.far, self.fovy, self.aspect = near, far, fovy, aspect
        self.left, self.right, self.bottom, self.top = left, right, bottom, top
        self.c = 1 / np.tan(fovy/2)  # precomputing cotan(fovy)

        self._angpos = np.array([0.0, 0.0])    # (pitch, yaw)
        self.yrot = np.eye(4)
        self.xrot = np.eye(4)
        self.trans = np.eye(4)
        self.update_view()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = np.array(value, dtype=np.float32)

    @property
    def angpos(self):
        return -self._angpos

    @angpos.setter
    def angpos(self, value):
        self._angpos = -np.array(value, dtype=np.float32)

    def update_projection(self, width, height, near=None, far=None, fovy=None):
        '''Generates a perspective projection matrix according to the parameters
        of a frustum, that is the viewport `width` and `height`, the distance to
        the near and far planes, `near` and `far`, the field of view angle
        `fovy` in radiands.
        Returns the projection matrix.
        '''
        self.width, self.height, aspect = width, height, width/height
        n = near if near is not None else self.near; self.near = n
        f = far if far is not None else self.far; self.far = f
        c = 1/np.tan(fovy/2) if fovy is not None else self.c; self.c = c
        self.projection = np.array([
            [c/aspect, 0.0, 0.0, 0.0],
            [0.0,     c,   0.0, 0.0],
            [0.0,     0.0, (f+n)/(n-f), 2*n*f/(n-f)],
            [0.0,     0.0, -1.0, 0.0],
        ])

        return self.projection

    def update_projection_ortho(self,
            width, height,
            left=None, right=None,
            bottom=None, top=None,
            near=None, far=None):
        self.width, self.height = width, height
        left = left if left is not None else self.left; self.left = left
        right = right if right is not None else self.right; self.right = right
        bottom = bottom if bottom is not None else self.bottom; self.bottom = bottom
        top = top if top is not None else self.top; self.top = top
        near = near if near is not None else self.near; self.near = near
        far = far if far is not None else self.far; self.far = far
        tx = -(right+left)/(right-left)
        ty = -(top+bottom)/(top-bottom)
        tz = -(far+near)/(far-near)
        self.projection = np.eye(4)
        self.projection[0, 0] = 2/(right-left)
        self.projection[1, 1] = 2/(top-bottom)
        self.projection[2, 2] = -2/(far-near)
        self.projection[:-1, -1] = np.array((tx, ty, tz))

        return self.projection


    def update_view(self, angd=(0.0, 0.0), lind=(0.0, 0.0, 0.0)):
        '''Trasforms the view matrix according to user input.
        Param `angd` is a tuple with (xd, yd) deltas. Typically mousex and
        mousey deltas are passed here.
        Param `lind` is a tuple with (left/right, forward/backward, up/down)
        deltas. Can take combinations of {(0, 0, -1), (0, 0, 1), (0, -1, 0),
        etc} describing the linear movement of the camera.
        Updates internally and returns the new view matrix.
        '''
        self._angpos += np.array(angd[::-1])*self.sens

        # constrain x and y angles to [-pi/2, pi/2] and [0, 2pi] repectively
        self._angpos[0] = np.clip(
            (self._angpos[0] + np.pi) % (2 * np.pi ) - np.pi,
            a_min=-np.pi/2, a_max=np.pi/2
        )
        self._angpos[1] = self._angpos[1] % (2*np.pi)

        ya = self._angpos[1]
        cosya = np.cos(ya)
        sinya = np.sin(ya)
        yrot = np.array([
            [ cosya,  0.0,    sinya,   0.0 ],
            [ 0.0,    1.0,    0.0,     0.0 ],
            [-sinya,  0.0,    cosya,   0.0 ],
            [ 0.0,    0.0,    0.0,     1.0 ]
        ])

        xa = self._angpos[0]
        cosxa = np.cos(xa)
        sinxa = np.sin(xa)
        xrot = np.array([
            [ 1.0,    0.0,     0.0,     0.0 ],
            [ 0.0,    cosxa,  -sinxa,   0.0 ],
            [ 0.0,    sinxa,   cosxa,   0.0 ],
            [ 0.0,    0.0,     0.0,     1.0 ],
        ])
        self.yrot = yrot
        self.xrot = xrot

        if lind == (0, 0, 1):     # move forward
            self._pos += np.array([np.sin(ya), 0.0, -np.cos(ya)])
        elif lind == (0, 0, -1):  # move backward
            self._pos += np.array([-np.sin(ya), 0.0, np.cos(ya)])
        elif lind == (1, 0, 0):   # strafe right
            self._pos += np.array([np.cos(ya), 0.0, np.sin(ya)])
        elif lind == (-1, 0, 0):  # strafe left
            self._pos += np.array([-np.cos(ya), 0.0, -np.sin(ya)])
        elif lind == (0, 1, 0):  # step up
            self._pos += np.array([0.0, 1.0, 0.0])
        elif lind == (0, -1, 0):  # step down
            self._pos += np.array([0.0, -1.0, 0.0])
        trans = np.eye(4)
        trans[:-1, 3] = np.around(np.array(-self._pos), decimals=0)
        self.trans = trans

        self.view = xrot @ yrot @ trans
        return self.view
