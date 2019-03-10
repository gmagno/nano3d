
import numpy as np
import pytest
import quaternion as qua

from nano3d.camera import CameraPerspective
from nano3d.mesh import Mesh
from nano3d.scene import CameraFPSNode, Node


def test_node_position():
    node = Node('node', Mesh())
    node.position = (1.0, 2.0, 3.0)
    node.position += (2.0, 3.0, 4.0)
    assert np.allclose(node.translation_mat(), np.array([
        [1.0, 0.0, 0.0, 3.0],
        [0.0, 1.0, 0.0, 5.0],
        [0.0, 0.0, 1.0, 7.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float32))

def test_node_rotate_in_xx():
    node = CameraFPSNode(name='node', mesh=Mesh(), camera=CameraPerspective())
    node.orientation = (1.0, 0.0, 0.0, 0.0)
    node.rotate_in_xx(pitch=np.pi/2.)
    rotation = node.rotation_mat()
    expected_rotation = np.array([
        [ 1.0,  0.0,  0.0,  0.0 ],
        [ 0.0,  0.0, -1.0,  0.0 ],
        [ 0.0,  1.0,  0.0,  0.0 ],
        [ 0.0,  0.0,  0.0,  1.0 ],
    ], dtype=np.float32)
    assert np.allclose(rotation, expected_rotation)

def test_node_rotate_in_yy():
    node = CameraFPSNode(name='node', mesh=Mesh(), camera=CameraPerspective())
    node.orientation = (1.0, 0.0, 0.0, 0.0)
    node.rotate_in_yy(yaw=np.pi/2.)
    rotation = node.rotation_mat()
    expected_rotation = np.array([
        [ 0.0,  0.0,  1.0,  0.0 ],
        [ 0.0,  1.0,  0.0,  0.0 ],
        [-1.0,  0.0,  0.0,  0.0 ],
        [ 0.0,  0.0,  0.0,  1.0 ]
    ], dtype=np.float32)
    assert np.allclose(rotation, expected_rotation)

def test_node_scale():
    node = Node(name='node', mesh=Mesh())
    node.scale = (1.0, 2.0, 3.0)
    assert np.allclose(node.scaling_mat(), np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 2.0, 0.0, 0.0],
        [0.0, 0.0, 3.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ], dtype=np.float32))

