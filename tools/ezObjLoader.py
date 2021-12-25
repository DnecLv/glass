import numpy as np


class ObjLoader:
    def __init__(self):
        self.vert_coords = []
        self.text_coords = []
        self.norm_coords = []

        self.vertex_index_vvn = []
        self.normal_index_vvn = []
        
        self.vertex_index_vvt = []
        self.texture_index_vvt = []
        
        self.vertex_index_vvtvn = []
        self.texture_index_vvtvn = []
        self.normal_index_vvtvn = []
        
        self.model_vvn = []
        self.model_vvt = []
        self.model_vvtvn = []

    def load_model(self, file):
        for line in open(file, 'r'):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                self.vert_coords.append(values[1:4])
            if values[0] == 'vt':
                self.text_coords.append(values[1:3])
            if values[0] == 'vn':
                self.norm_coords.append(values[1:4])

            if values[0] == 'f':
                # check f's format
                
                # v/vn
                if values[1].split('//')[0] != values[1]:
                    face_i = []
                    norm_i = []
                    for v in values[1:4]:
                        w = v.split('/')
                        face_i.append(int(w[0])-1)
                        norm_i.append(int(w[2])-1)
                    self.vertex_index_vvn.append(face_i)
                    self.normal_index_vvn.append(norm_i)

                    if len(values) == 5:
                        face_i = []
                        text_i = []
                        norm_i = []
                        for v in [values[1],values[3],values[4]]:
                            w = v.split('/')
                            face_i.append(int(w[0])-1)
                            norm_i.append(int(w[2])-1)
                        self.vertex_index_vvn.append(face_i)
                        self.normal_index_vvn.append(norm_i)
                        
                # v/vt
                elif len(values[1].split('/')) == 2:
                    print(values,values[1].split('/')[0])
                    face_i = []
                    text_i = []
                    for v in values[1:4]:
                        w = v.split('/')
                        face_i.append(int(w[0])-1)
                        text_i.append(int(w[1])-1)
                    self.vertex_index_vvt.append(face_i)
                    self.texture_index_vvt.append(text_i)

                    if len(values) == 5:
                        face_i = []
                        text_i = []
                        for v in [values[1],values[3],values[4]]:
                            w = v.split('/')
                            face_i.append(int(w[0])-1)
                            text_i.append(int(w[1])-1)
                        self.vertex_index_vvt.append(face_i)
                        self.texture_index_vvt.append(text_i)
                        
                # vvn
                elif len(values[1].split('/')) == 3:
                    face_i = []
                    text_i = []
                    norm_i = []
                    for v in values[1:4]:
                        w = v.split('/')
                        face_i.append(int(w[0])-1)
                        text_i.append(int(w[1])-1)
                        norm_i.append(int(w[2])-1)
                    self.vertex_index_vvtvn.append(face_i)
                    self.texture_index_vvtvn.append(text_i)
                    self.normal_index_vvtvn.append(norm_i)

                    if len(values) == 5:
                        face_i = []
                        text_i = []
                        norm_i = []
                        for v in [values[1],values[3],values[4]]:
                            w = v.split('/')
                            face_i.append(int(w[0])-1)
                            text_i.append(int(w[1])-1)
                            norm_i.append(int(w[2])-1)
                        self.vertex_index_vvtvn.append(face_i)
                        self.texture_index_vvtvn.append(text_i)
                        self.normal_index_vvtvn.append(norm_i)
                        
                                            
        self.vertex_index_vvn = [y for x in self.vertex_index_vvn for y in x]
        self.normal_index_vvn = [y for x in self.normal_index_vvn for y in x]
        
        self.vertex_index_vvt = [y for x in self.vertex_index_vvt for y in x]
        self.texture_index_vvt = [y for x in self.texture_index_vvt for y in x]
        
        self.vertex_index_vvtvn = [y for x in self.vertex_index_vvtvn for y in x]
        self.texture_index_vvtvn = [y for x in self.texture_index_vvtvn for y in x]
        self.normal_index_vvtvn = [y for x in self.normal_index_vvtvn for y in x]

        for i in self.vertex_index_vvtvn:
            self.model_vvtvn.extend(self.vert_coords[i])
        for i in self.normal_index_vvtvn:
            self.model_vvtvn.extend(self.norm_coords[i])
        for i in self.texture_index_vvtvn:
            self.model_vvtvn.extend(self.text_coords[i])
            
        for i in self.vertex_index_vvn:
            self.model_vvn.extend(self.vert_coords[i])
        for i in self.normal_index_vvn:
            self.model_vvn.extend(self.norm_coords[i])
            
        
        for i in self.vertex_index_vvt:
            self.model_vvt.extend(self.vert_coords[i])
        for i in self.texture_index_vvt:
            self.model_vvt.extend(self.text_coords[i])
            
                
        self.model_vvn = np.array(self.model_vvn, dtype='float32')
        self.model_vvt = np.array(self.model_vvt, dtype='float32')
        self.model_vvtvn = np.array(self.model_vvtvn, dtype='float32')
