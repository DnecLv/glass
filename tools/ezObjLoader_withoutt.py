import numpy as np

class ObjLoader:
    def __init__(self):
        self.vert_coords = []
        self.norm_coords = []

        self.vertex_index = []
        self.normal_index = []
    
        self.model = []

    def load_model(self, file):
        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                self.vert_coords.append(values[1:4])
            if values[0] == 'vn':
                self.norm_coords.append(values[1:4])

            if values[0] == 'f':
                face_i = []
                norm_i = []
                for v in values[1:4]:
                    w = v.split('//')
                    face_i.append(int(w[0])-1)
                    norm_i.append(int(w[1])-1)
                self.vertex_index.append(face_i)
                self.normal_index.append(norm_i)

        self.vertex_index = [y for x in self.vertex_index for y in x]
        self.normal_index = [y for x in self.normal_index for y in x]

        for i in self.vertex_index:
            self.model.extend(self.vert_coords[i])

        for i in self.normal_index:
            self.model.extend(self.norm_coords[i])

        self.model = np.array(self.model, dtype='float32')

    @staticmethod
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # sort the vertex coordinates
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # sort the texture coordinates
                start = ind * 2
                end = start + 2
                ObjLoader.buffer.extend(textures[start:end])
            elif i % 3 == 2: # sort the normal vectors
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])



















