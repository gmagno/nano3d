
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
    def __init__(self,
            projw=30, projh=None, near=0.0, far=9.0, *args, **kwargs
    ):
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
        self.near = near
        self.far = far

