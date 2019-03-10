#version 330
in vec4 position;
in vec4 color;
out vec4 fColor;

uniform mat4 mvp;  // projection * view * model: mvp matrix

void main(void) {
    fColor = color;
    gl_Position = mvp * position;
}

