
from enum import Enum
import errno
import os
from pathlib import Path

import collada as co
import numpy as np

from nano3d.material import Material

class Primitive(Enum):
    POINTS = 1
    LINES = 2
    TRIANGLES = 3

class Mesh():
    def __init__(self):
        # vertex data
        self._positions = None
        self._indices = None
        self._normals = None
        self._colors = None
        self._primitive = None # one of: {Primitive.POINTS/LINES/TRIANGLES}
        self.no_indices = None
        self.material = Material('base')
        self.attribs = {}
        self.uniforms = {}

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        self._positions = np.array(value, dtype=np.float32)

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, value):
        self._indices = np.array(value, dtype=np.int32)

    @property
    def normals(self):
        return self._normals

    @normals.setter
    def normals(self, value):
        self._normals = np.array(value, dtype=np.float32)

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, value):
        self._colors = np.array(value, dtype=np.float32)

    @property
    def primitive(self):
        return self._primitive

    @primitive.setter
    def primitive(self, value):
        # supported_primitives = [item.value for item in Primitive]
        if value.name not in Primitive.__members__:
            raise BadPrimitiveError(
                'Supported primitives: {}, found: {}'.format(
                    Primitive.__members__, value
                )
            )
        self._primitive = value


class BadPrimitiveError(Exception):
    pass


class CubeWired(Mesh):

    def __init__(self):
        super(CubeWired, self).__init__()
        self.primitive = Primitive.LINES
        self.positions = np.array([
            [0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0],
            [0.0, 1.0, 0.0, 1.0], [1.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0],
        ], dtype=np.float32).T  # <-- notice the transpose!
        self.indices = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
            [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7],
        ], dtype=np.int32).T  # <-- notice the transpose!
        self.colors = self.positions
        self.no_indices = self.indices.shape[1]
        self.material = Material('cube-material')
        self.attribs = { 'position': self.positions, 'color': self.colors }
        self.uniforms = {}

class Axes(Mesh):
    def __init__(self):
        super(Axes, self).__init__()
        self.primitive = Primitive.LINES
        positions = np.zeros((12, 4), dtype=np.float32)
        positions[:6, -1] = np.ones(6, dtype=np.float32)
        positions[6:9, :3] = np.eye(3, dtype=np.float32)
        positions[9:, :3] = -np.eye(3, dtype=np.float32)
        self.positions = positions.T
        indices = np.zeros((6, 2), dtype=np.int32)
        indices[:, 0] = np.arange(6, dtype=np.int32)
        indices[:, 1] = np.arange(6, 12, dtype=np.int32)
        self.indices = indices.T
        colors = np.ones((12, 4), dtype=np.float32)
        colors[ :3, :3] = np.eye(3)
        colors[3:6, :3] = 0.3*np.eye(3)
        colors[6:9, :3] = np.eye(3)
        colors[9: , :3] = 0.3*np.eye(3)
        self.colors = colors.T
        self.no_indices = self.indices.shape[1]
        self.material = Material('axes-material')
        self.attribs = { 'position': self.positions, 'color': self.colors }
        self.uniforms = {}


class Grid(Mesh):
    def __init__(self, n):
        super(Grid, self).__init__()
        self.primitive = Primitive.LINES
        positions = np.zeros((n*4+4, 4))
        positions[0, 2] = -1; positions[1, 2] = 1
        positions[2:2*n+2, 0] = np.concatenate((np.arange(-n, 0), np.arange(1, n+1)))
        positions[2:2*n+2, -1] = np.ones(2*n)
        positions[2*n+2, 0] = -1; positions[2*n+3, 0] = 1
        positions[2*n+4:, 2] = np.concatenate((np.arange(-n, 0), np.arange(1, n+1)))
        positions[2*n+4:, -1] = np.ones(2*n)
        self.positions = positions.T

        indices = np.zeros((8*n, 2), dtype=np.int32)
        indices[:2*n, 0] = np.zeros(2*n)
        indices[2*n:4*n, 0] = np.ones(2*n)
        indices[:2*n, 1] = np.arange(2, 2*n+2)
        indices[2*n:4*n, 1] = np.arange(2, 2*n+2)
        indices[4*n:6*n, 0] = (2*n+2)*np.ones(2*n)
        indices[6*n:8*n, 0] = (2*n+3)*np.ones(2*n)
        indices[4*n:6*n, 1] = np.arange(2*n+4, 2*n+4+2*n)
        indices[6*n:8*n, 1] = np.arange(2*n+4, 2*n+4+2*n)
        self.indices = indices.T
        colors = np.zeros((n*4+4, 4), dtype=np.float32)
        colors[:, 0] = 0.3*np.ones(n*4+4)
        colors[:, 1] = 0.3*np.ones(n*4+4)
        colors[:, 2] = 0.3*np.ones(n*4+4)
        colors[:, 3] = 0.3*np.ones(n*4+4)
        self.colors = colors.T
        self.no_indices = self.indices.shape[1]
        self.material = Material('grid-material')
        self.attribs = { 'position': self.positions, 'color': self.colors }
        self.uniforms = {}


class Line(Mesh):
    def __init__(self, positions, colors=[(1, 1, 1, 1),]):
        super(Mesh, self).__init__()
        self.positions = positions
        self.indices = np.zeros((self.positions.shape[0] - 1, 2))
        self.indices[:, 0] = np.arange(0, self.indices.shape[0])
        self.indices[:, 1] = np.arange(1, self.indices.shape[0] + 1)
        self.colors = colors
        if self.colors.shape[0] < self.positions.shape[0]:
            tmp = self.colors
            self.colors = np.zeros((self.positions.shape))
            self.colors[:tmp.shape[0], :] = tmp
            self.colors[tmp.shape[0]:, :] = tmp[-1, :]
        self.positions = self.positions.T
        self.indices = self.indices.T
        self.colors = self.colors.T
        self.no_indices = self.indices.shape[1]
        self.attribs = { 'position': self.positions, 'color': self.colors }
        self.uniforms = {}
        self.primitive = Primitive.LINES
        self.material = Material('line-material')


class Dae(Mesh):
    def __init__(self, daefile):
        '''Instantiates a Mesh from a collada file (.dae)

        Parameters
        ----------
        daefile: the path to the collada file, e.g: /path/to/obj3d.dae
        '''
        super(Mesh, self).__init__()
        self.daefile = daefile
        mesh = co.Collada(self._daefile)

        self.positions = np.array([], dtype=np.float32)
        self.indices = np.array([], dtype=np.int32)
        self.normals = np.array([], dtype=np.float32)
        # self.colors = np.array([], dtype=np.float32)


        self.objects = []
        for g in mesh.scene.objects('geometry'):
            for triset in g.primitives():
                if type(triset) != co.triangleset.BoundTriangleSet:
                    # ignore everything that is not a triangle
                    continue
                normal = np.zeros(triset.vertex.shape)
                for i, tri in enumerate(triset.vertex_index):
                    normal[tri] = triset.normal[triset.normal_index[i]]
                o = {
                    'positions': triset.vertex,
                    'normals': normal,
                    'indices': triset.vertex_index
                }
                self.objects.append(o)

        for o in self.objects:
            self.indices = np.concatenate((
                self.indices.flatten(),
                (o['indices'] + self.positions.shape[0]).flatten()
            )).reshape(-1, 3)
            self.positions = np.concatenate((
                self.positions.flatten(),
                o['positions'].flatten()
            )).reshape(-1, 3)
            self.normals = np.concatenate((
                self.normals.flatten(),
                o['normals'].flatten()
            )).reshape(-1, 3)

        self.no_indices = self.indices.shape[0]

        self.positions = self.positions.T
        self.indices = self.indices.T
        self.normals = self.normals.T
        # self.colors = np.ones(self.positions.shape)

        self.material = Material('dae-material')
        self.material.load_shaders(
            'data/shaders/flat.vs.glsl',
            'data/shaders/flat.fs.glsl',
        )
        self.attribs = {
            'position': self.positions,
            # 'color': self.colors,
            'normal': self.normals
        }
        ldir = np.array([-1.0, -2.0, -3.0])
        self.uniforms = {
            'lAmbColor': np.array([0.1, 0.1, 0.1]),
            'lDiffColor': np.array([0.3, 0.3, 0.3]),
            'lDirection':  ldir/np.linalg.norm(ldir),
        }
        self.primitive = Primitive.TRIANGLES

    @property
    def daefile(self):
        return self._daefile

    @daefile.setter
    def daefile(self, filename):
        f = Path(filename)
        if not f.is_file():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), filename
            )
        self._daefile = filename
