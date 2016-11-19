import sys
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np

import sdl2
from sdl2 import video

vertex_shader = """
#version 330
in vec3 position;
void main()
{
   gl_Position = vec4(position, 1.f);
}
"""

fragment_shader = """
#version 330
void main()
{
gl_FragColor = vec4(0.5f, 1.0f, 1.0f, 1.0f);
}
"""

vertices = [ 0.6, 0.6, 0.0,
            -0.6, 0.6, 0.0,
             0.0, -0.6, 0.0]

vertices = np.array(vertices, dtype=np.float32)

def create_vbo(shader):
    
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray( vertex_array_object )
    
    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    
    # Get the position of the 'position' in parameter of our shader and bind it.
    position = glGetAttribLocation(shader, 'position')
    glEnableVertexAttribArray(position)
    
    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    
    # Send the data over to the buffer
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    
    # Unbind the VAO first (Important)
    glBindVertexArray( 0 )

    
    # Unbind other stuff
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    
    
    return vertex_array_object, vertex_buffer


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader)


    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    global vertices
    vertices += 0.001
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STREAM_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


    glBindVertexArray(vertex_array_object )
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray( 0 )
    
    glUseProgram(0)

if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
    print(sdl2.SDL_GetError())

window = sdl2.SDL_CreateWindow(b"OpenGL demo",
    sdl2.SDL_WINDOWPOS_UNDEFINED,
    sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
    sdl2.SDL_WINDOW_OPENGL)

if not window:
    print(sdl2.SDL_GetError())

video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)
context = sdl2.SDL_GL_CreateContext(window)

glClearColor(0.5, 0.5, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
glViewport(0, 0, 800, 600)

shader = OpenGL.GL.shaders.compileProgram(
    shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

vertex_array_object, vertex_buffer = create_vbo(shader)

event = sdl2.SDL_Event()
running = True
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif (event.type == sdl2.SDL_KEYDOWN and
            event.key.keysym.sym == sdl2.SDLK_ESCAPE):
            running = False

    render()

    sdl2.SDL_GL_SwapWindow(window)
    sdl2.SDL_Delay(10)

sdl2.SDL_GL_DeleteContext(context)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()