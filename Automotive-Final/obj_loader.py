import numpy as np


class ObjLoader:

    buffer = []

    
    # this method takes a single line of obj file and checks the type of the
    # character and appends it into the provided list named coords. since every
    # line of the file starts with character like v, vt... it will skip such characters.
    @staticmethod
    def searchData(values, coords, skip, type) -> None:
        for data in values:
            if data == skip:
                continue
            if type == 'float':
                coords.append(float(data))
            elif type == 'int':
                coords.append(int(data)-1)


    # a function to create a sorted vertex buffer to use it with glDrawArrays function
    # this function checks the verteces and sorts them according to their catagories.
    @staticmethod
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals) -> None:

        for i, ind in enumerate(indices_data):
            # sort the vertex coordinates
            if i % 3 == 0:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            # sort the texture coordinates
            elif i % 3 == 1:
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            # sort the normal vectors
            elif i % 3 == 2:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])


    # This function takes a filepath, reads everyline and categories it into Vertex Coordinates,
    # Texture Coordinates and vertex Normals and returns the vertecies and data in a tuple.
    @staticmethod
    def load_model(filepath) -> tuple:
        vert_coords = []
        tex_coords = []
        norm_coords = []
        
        all_indices = []
        indices = []


        with open(filepath, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    ObjLoader.searchData(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    ObjLoader.searchData(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    ObjLoader.searchData(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        ObjLoader.searchData(val, all_indices, 'f', 'int')
                        indices.append(int(val[0])-1)

                line = f.readline()

        ObjLoader.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)
        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')