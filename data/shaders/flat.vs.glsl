#version 330
in vec4 position;
in vec3 normal;
out vec4 fColor;

uniform mat4 mvp;

uniform vec3 lAmbColor;
uniform vec3 lDiffColor;
uniform vec3 lDirection;

void main()
{
    gl_Position = mvp * position;
    vec4 ambient = vec4(lAmbColor, 0.2);
    vec4 diffuse = vec4(max(dot(lDirection, -normal), 0) * lDiffColor, 0.2);
    fColor = ambient + diffuse;
}
