# python 3.7.3
# -*- coding:UTF-8 -*-
# AUTHOR: DnecLv
# FILE: D:\dnec_proj\learn_openGL\Instancing\ObjLoader.py
# DATE: 2021/06/20 周日
# TIME: 17:50:30

# DESCRIPTION:
# * 分析一个obj文件
# * 1. load_model,传入文件,并分类
# * 2. 
import numpy as np

class ObjLoader():
    buffer = []
    
    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            # delete sth. like "v"
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1) # int means F which begins from 1 and we want it starts from 0 

    # * 比如obj文件中f 5/15/7 4/14/6 6/16/8 ，表示由第5、第4、第6这三个顶点组成了一个三角平面,平面的纹理由第15、第14、第16这三个纹理坐标形成，这个平面的朝向是第7、第6、第8这三个顶点的法向量求平均值。
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

    # TODO load all the params from *.obj
    @staticmethod
    def load_model(file):
        # 顶点 / 贴图坐标 / 法向量坐标
        vert_coords,tex_coords,norm_coords = [],[],[]

        all_indices = [] # will contain all the vertex, texture and normal indices
        indices = [] # will contain the indices for indexed drawing

        with open(file, 'r') as f:
            line = f.readline()
            while line:
                # * a line may like this ↓
                # * v -0.000000 1.048728 -2.606873
                values = line.split()
                if values[0] == 'v':
                    # 传递进去了一个列表,然后将这一行传递给search函数,每个float数都会被append到vert_coords中
                    ObjLoader.search_data(values, vert_coords, 'v', 'float') 
                elif values[0] == 'vt':
                    ObjLoader.search_data(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    ObjLoader.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    # 一个列表 [f,2505/1506/1501,499/1505/1500,3283/3192/3185]
                    for value in values[1:]:
                        val = value.split('/')
                        # 一个列表 [2505,1506,1501]
                        ObjLoader.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0])-1)

                line = f.readline()
                
        # use with glDrawArrays
        ObjLoader.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)

        buffer = ObjLoader.buffer.copy() # create a local copy of the buffer list, otherwise it will overwrite the static field buffer
        ObjLoader.buffer = [] # after copy, make sure to set it back to an empty list
        # * indices的长度起码告诉了有多少顶点
        # * buffer数组是按照顺序排列的8个8个顶点坐标
        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')