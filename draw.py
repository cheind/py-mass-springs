import sys
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

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


def display(w, h):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader)


    
    glBindVertexArray(vertex_array_object )

    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    global vertices
    vertices += 0.001
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray( 0 )
    
    glUseProgram(0)

    # ... render stuff in here ...
    # It will go to an off-screen frame buffer.

    # Copy the off-screen buffer to the screen.
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glutDisplayFunc(lambda: display(w, h))
    glutPostRedisplay()



glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutCreateWindow(b'mass-spring')
glutReshapeFunc(reshape)
glutIdleFunc(glutPostRedisplay)

glClearColor(0.5, 0.5, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
shader = OpenGL.GL.shaders.compileProgram(
    shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

vertex_array_object, vertex_buffer = create_vbo(shader)

glutMainLoop()