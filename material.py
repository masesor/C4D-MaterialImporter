import c4d
import constants
import material_parser

class Material():
    def __init__(self):
        self.__paths = {}
        self.__name = ''

    def get_paths(self):
        return self.__paths

    def set_material_path(self, material_type, file_path):
        self.__paths[material_type] = file_path

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def is_float(self):
        return self.__is_float

    def set_is_float(self, is_float):
        self.__is_float = is_float


def create_octane_image_texture(file_path, is_float=False):
    shd = c4d.BaseShader(constants.ID_OCTANE_IMAGE_TEXTURE)

    shd[c4d.IMAGETEXTURE_FILE] = file_path
    shd[c4d.IMAGETEXTURE_MODE] = 1 if is_float else 0
    shd[c4d.IMAGETEXTURE_GAMMA] = 2.2
    shd[c4d.IMAGETEX_BORDER_MODE] = 0

    return shd


def create_octane_displacement(file_path):
    shd = c4d.BaseShader(ID_OCTANE_DISPLACEMENT)

    # image_texture = create_octane_image_texture(file_path)
    return shd

def create_octane_specular_material(material):
    mat = c4d.BaseMaterial(constants.ID_OCTANE_DIFFUSE_MATERIAL)
    mat[c4d.OCT_MATERIAL_TYPE] = constants.ID_OCTANE_SPECULAR_TYPE

    for material_type, texture_path in material.get_paths().items():
      shader = create_octane_image_texture(texture_path)      
      mat[material_parser.PARSER_DATA[material_type].get_material_id()] = shader
      mat.InsertShader(shader)
    mat.SetName(material.get_name())

    return mat

