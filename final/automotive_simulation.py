import os
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader,compileProgram
import pyrr
from PIL import Image
from obj_loader import *


class Automotive:
    
    def __init__(self) -> None:
        pass


    def getFileContents(self, filename) -> str:

        p = os.path.join(os.getcwd(), "final/shaders", filename)
        return open(p, 'r').read()


    def init(self) -> None:

        pygame.init()
        display = (1366, 710)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
        gluPerspective(4, (display[1] / display[0]), 0.1, 50.0)
        glClearColor(0.5294, 0.8078, 0.9216, 0.4)


    def draw(self) -> None:

        indices, data = ObjLoader.load_model("final/object/Car.obj")

        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

        ibuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open("final/texture/car_texture.png")
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        image_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))

        vertex_src = self.getFileContents("vertex.shader")
        fragment_src = self.getFileContents("fragment.shader")

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        shaders = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

        model_loc = glGetUniformLocation(shaders, "model")
        proj_loc = glGetUniformLocation(shaders, "projection")
        view_loc = glGetUniformLocation(shaders, "view")

        trans_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1366/768, 0.1, 100)

        scaler_mat = pyrr.Matrix44.from_scale(pyrr.Vector3([3, 3, 3]))

        view_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1, 0]))

        look_mat = pyrr.matrix44.create_look_at(pyrr.Vector3([-5, 1.5, 0]),pyrr.Vector3([0, 0, 0]),pyrr.Vector3([0, 1, 0]))
        glClearColor(0, 0, 0.2, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(shaders)

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, look_mat)

        rotx = pyrr.Matrix44.from_x_rotation(0 * pygame.time.get_ticks())
        roty = pyrr.Matrix44.from_y_rotation(0.001 * pygame.time.get_ticks())
        rotz = pyrr.Matrix44.from_z_rotation(0 * pygame.time.get_ticks())
        rot_mat = roty * rotx * rotz
        model_mat = pyrr.matrix44.multiply(rot_mat, trans_mat)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model_mat)
        glDrawArrays(GL_TRIANGLES, 0, len(indices))


    def main(self) -> None:

        self.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw()
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    car = Automotive()
    car.main()