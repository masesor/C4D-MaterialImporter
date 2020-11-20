# import c4d
# from c4d import gui
import os
from os.path import isfile, isdir, join
import sys

# sys.path.append(c4d.storage.GeGetStartupPath() + "\\plugins\\MaterialImport")
import constants
# import material_parser
# import material

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


class MaterialImportDialog():
  def Command(self):
    self.handle_open_directory()

  def handle_open_directory(self):
    current_path = "D:\Cloud\Documents\Sams Stuff\Resources\VFX\Assets\STOCK IMAGES\TEXTURES\RD-Textures\RDT Collection 1\RDT-Collection-one_direct_1of7"
    # print("path {}".format(current_path))
    material_data = self.get_materials_from_path(current_path)      
    for data in material_data:
      print(data)
      # specular_material = material.create_octane_specular_material(data)


  def get_materials_from_path(self, file_path):
    walker = Walker()
    directories = walker.get_directories(file_path)
    current_directory_files = walker.get_files(file_path)

    materials = []
    # for directory in directories:
    for (root, _, _) in os.walk(file_path, topdown = True): 
      print("directory {}\n".format(root))
      files = walker.get_files(root)
      print("files {}\n".format(files))
      # materials.append(material_parser.create_material(files, directory))

    # if current_directory_files:
    #   print(current_directory_files)
    #   materials.append(material_parser.create_material(current_directory_files, file_path))

    return materials

if __name__ == "__main__":
    x = MaterialImportDialog()
    x.Command()