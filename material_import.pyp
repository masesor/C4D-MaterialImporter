import c4d
from c4d import gui
import collections
import os
from os.path import isfile, isdir, join
import re
import json
import glob
import sys

sys.path.append(c4d.storage.GeGetStartupPath() + "\\plugins\\MaterialImport")
import constants
import material_parser
import material
# class Material():
#   def __init__(self):
#     self.paths = {}
#     self.name = ''

#   def get_paths(self):
#     return self.paths

#   def set_material_path(self, material_type, file_path):
#     self.paths[material_type] = file_path

#   def get_name(self):
#     return self.name

#   def set_name(self, name):
#     self.name = name

#   def is_float(self):
#     return self.is_float

#   def set_is_float(self, is_float):
#     self.is_float = is_float

# class ParserData():
#   def __init__(self, regex, material_id, is_float = False):
#     self.regex = regex
#     self.material_id = material_id
#     self.is_float = is_float

# class MaterialParser():
#   parser_data = {
#     DIFFUSE: ParserData(re.compile('(?i).*(diffuse|diff|albedo|col|color|colour).*'), c4d.OCT_MATERIAL_DIFFUSE_LINK),
#     SPECULAR: ParserData(re.compile('(?i).*(spec|specular).*'), c4d.OCT_MATERIAL_SPECULAR_LINK, True),
#     ROUGHNESS: ParserData(re.compile('(?i).*(rough).*'), c4d.OCT_MATERIAL_ROUGHNESS_LINK, True),
#     GLOSS: ParserData(re.compile('(?i).*(refl|reflection|gloss).*'), True),
#     BUMP: ParserData(re.compile('(?i).*(bump).*'), c4d.OCT_MATERIAL_BUMP_LINK, True),
#     NORMAL: ParserData(re.compile('(?i).*(normal|nrm).*'), c4d.OCT_MATERIAL_NORMAL_LINK),
#     DISPLACEMENT: ParserData(re.compile('(?i).*(displacement|disp).*'), c4d.OCT_MATERIAL_DISPLACEMENT_LINK, True),
#     AO: ParserData(re.compile('(?i).*(ao).*'), True) 
#   }

#   def create_material(self, files, directory):
#     material = Material()
#     for file_path in files:
#       for regex_type, parser_data in self.parser_data.items():
#         # print("Checking pattern {} for type {} on path {}" % pattern, regex_type, path)
#         if parser_data.regex.match(file_path):
#           material.set_material_path(regex_type, file_path)
#           material.set_is_float(parser_data.is_float)
#           self.set_material_name(material, directory)
#           continue
#     return material

#   def set_material_name(self, material, directory):
#     manifest_data = self.read_json_manifest(directory)
#     if not manifest_data:
#       split_path = directory.split(os.sep)
#       material_name = split_path[len(split_path)]
#     material.set_name(manifest_data['name'] if manifest_data else material_name)

#   def read_json_manifest(self, directory):
#     manifest_file = [f for f in os.listdir(directory) if f.endswith('.json')][0]

#     if manifest_file:
#       with open(directory + os.sep + manifest_file, 'r') as manifest:
#         data = manifest.read()
      
#         return json.loads(data)

class Walker():
  def print_files(self, path):
    onlyfiles = [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]
    print(onlyfiles)

  def get_files(self, path):
    return [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]

  def print_dirs(self, path):
    onlyfiles = [join(path, f) for f in os.listdir(path) if isdir(join(path, f))]
    print(onlyfiles)

  def get_directories(self, path):
    return [join(path, f) for f in os.listdir(path) if isdir(join(path, f))]

# def create_octane_image_texture(file_path, is_float = False):
#   shd = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
  
#   shd[c4d.IMAGETEXTURE_FILE] = file_path
#   shd[c4d.IMAGETEXTURE_MODE] = 1 if is_float else 0
#   shd[c4d.IMAGETEXTURE_GAMMA] = 2.2
#   shd[c4d.IMAGETEX_BORDER_MODE] = 0

#   return shd

# def create_octane_displacement(file_path):
#   shd = c4d.BaseShader(ID_OCTANE_DISPLACEMENT)

#   # image_texture = create_octane_image_texture(file_path)
  
#   return shd

class MaterialImportDialog(c4d.gui.GeDialog):
  def CreateLayout(self):
    return self.LoadDialogResource(constants.MATERIAL_IMPORT_DIALOG)

  def Command(self, id, msg):
    if (id == constants.MATERIAL_DIRECTORY_PATH):
      self.handle_open_directory()
    return super(MaterialImportDialog, self).Command(id, msg)

  def handle_open_directory(self):
    current_path = self.GetString(constants.MATERIAL_DIRECTORY_PATH)
    material_paths = self.get_materials_from_path(current_path)      
    for material_path in material_paths:
      print("Loading material from {}".format(material_path.get_name()))
      specular_material = material.create_octane_specular_material(material_path)
      doc = c4d.documents.GetActiveDocument()
      doc.InsertMaterial(specular_material)


  def get_materials_from_path(self, file_path):
    walker = Walker()
    # walker.print_dirs(file_path)
    directories = walker.get_directories(file_path)

    materials = []
    for directory in directories:
      files = walker.get_files(directory)
      materials.append(material_parser.create_material(files, directory))

    return materials

  # def CreateOctaneSpecularMaterial(self, material):
  #  mat = c4d.BaseMaterial(constants.ID_OCTANE_DIFFUSE_MATERIAL)
  #  mat[c4d.OCT_MATERIAL_TYPE] = constants.ID_OCTANE_SPECULAR_TYPE

  #  for material_type, texture_path in material.get_paths().items():
  #    shader = create_octane_image_texture(texture_path)      
  #    mat[MaterialParser.parser_data[material_type].material_id] = shader
  #    mat.InsertShader(shader)
  #  mat.SetName(material.get_name())

  #  return mat

class MaterialImportCommandData(c4d.plugins.CommandData):
    """
    Command Data class that holds the Dialog instance.
    """
    dialog = None

    def Execute(self, doc):
        """
        Called when the user Execute the command (CallCommand or a clicks on the Command from the plugin menu)
        :param doc: the current active document
        :type doc: c4d.documents.BaseDocument
        :return: True if the command success
        """
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = MaterialImportDialog()

        # Opens the dialog
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=constants.PLUGIN_ID, defaulth=400, defaultw=400)

    def RestoreLayout(self, sec_ref):
        """
        Used to restore an asynchronous dialog that has been placed in the users layout.
        :param sec_ref: The data that needs to be passed to the dlg (almost no use of it).
        :type sec_ref: PyCObject
        :return: True if the restore success
        """
        # Creates the dialog if its not already exists
        if self.dialog is None:
            self.dialog = MaterialImportDialog()

        # Restores the layout
        return self.dialog.Restore(pluginid=constants.PLUGIN_ID, secret=sec_ref)



if __name__ == "__main__":

    # Registers the Command plugin
    c4d.plugins.RegisterCommandPlugin(id=constants.PLUGIN_ID, #TODO UPDATE
                                      str="Material Importer",
                                      help="Imports materials for Octane Renderer.",
                                      info=0,
                                      dat=MaterialImportCommandData(),
                                      icon=None)
