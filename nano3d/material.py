
import os
import errno
from pathlib import Path

class Material():
    def __init__(self, name):
        self.name = name
        self.vsh = '''
            #version 330
            in vec4 position;
            in vec4 color;
            out vec4 fColor;
            uniform mat4 mvp;
            void main(void) {
                fColor = color;
                gl_Position = mvp * position;
            }
        '''
        self.fsh = '''
            #version 330
            in vec4 fColor;
            out vec4 outColor;
            void main() {
                outColor = fColor;
            }
        '''

    def load_shaders(self, vsh_path, fsh_path):
        for path in [vsh_path, fsh_path]:
            f = Path(path)
            if not f.is_file():
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), path
                )
        with open(vsh_path, 'r') as f:
            self.vsh = f.read()
        with open(fsh_path, 'r') as f:
            self.fsh = f.read()

