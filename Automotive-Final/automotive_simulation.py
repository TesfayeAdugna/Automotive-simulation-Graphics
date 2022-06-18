import os
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader,compileProgram
import pyrr
from PIL import Image
from obj_loader import ObjLoader


class Automotive:
    
    def __init__(self) -> None:
        pass

    # This function reads the shader files and returns their contents as string.
    def getFileContents(self, filename) -> str:

        p = os.path.join(os.getcwd(), "Automotive-Final/shaders", filename)
        return open(p, 'r').read()

    # This function initializes and creates the pygame window.
    def init(self) -> None:

        pygame.init()
        display = (1366, 710)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
        gluPerspective(4, (display[1] / display[0]), 0.1, 50.0)
        glClearColor(0.5294, 0.8078, 0.9216, 0.4)

    # This function parses the image using the PIL library, and converts it into RGBA
    # color and binds it with the 3D object.
    def textureImage(self):
        image = Image.open("Automotive-Final/texture/car_texture.png")
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        image_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # This function draws the object based on the provided indexes and datas from the
    # object loader. It takes rotational direction values for x, y and z based on the
    # pressed keys and rotates the object based on that value. 
    def draw(self, y, z) -> None:

        indices, data = ObjLoader.load_model("Automotive-Final/object/Car.obj")

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

        self.textureImage()

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

        pyrr.Matrix44.from_scale(pyrr.Vector3([3, 3, 3]))
        pyrr.matrix44.create_from_translation(pyrr.Vector3([0, -1, 0]))

        look_mat = pyrr.matrix44.create_look_at(pyrr.Vector3([-5, 1.5, 0]),pyrr.Vector3([0, 0, 0]),pyrr.Vector3([0, 1, 0]))
        glClearColor(0, 0, 0.2, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(shaders)

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, look_mat)

        rotx = pyrr.Matrix44.from_x_rotation(0 * pygame.time.get_ticks())
        roty = pyrr.Matrix44.from_y_rotation(y * 0.0005 * pygame.time.get_ticks())
        rotz = pyrr.Matrix44.from_z_rotation(z * 0.0005 * pygame.time.get_ticks())
        rot_mat = rotx * roty * rotz
        model_mat = pyrr.matrix44.multiply(rot_mat, trans_mat)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model_mat)
        glDrawArrays(GL_TRIANGLES, 0, len(indices))

    # The main function holds the main loop for keeping the pygame window open
    # and managing the key presses.
    def main(self) -> None:
        y = 0
        z = 0
        self.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        y += 0.2
                    if event.key == pygame.K_RIGHT:
                        y -= 0.2
                    if event.key == pygame.K_UP:
                        z += 0.05
                    if event.key == pygame.K_DOWN:
                        z -= 0.05

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(y, z)
            pygame.display.flip()
            pygame.time.wait(10)


if __name__ == "__main__":
    car = Automotive()
    car.main()