import c4d
from c4d import gui
import collections
import os
from os.path import isfile, join
import re

PLUGIN_ID = 1025249

materialImportDialog = 100001
MATERIAL_DIRECTORY_PATH = 100002

# Octane IDs
ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_OCTANE_IMAGE_TEXTURE = 1029508

# Material IDs
DIFFUSE = 'DIFFUSE'
SPECULAR = 'SPECULAR'
ROUGHNESS = 'ROUGHNESS'
GLOSS = 'GLOSS'
BUMP = 'BUMP'
NORMAL = 'NORMAL'
DISPLACEMENT = 'DISPLACEMENT'

class Material():
  def __init__(self):
    self.paths = {}

  def set_material_path(self, material_type, file_path):
    self.paths[material_type] = file_path

  def get_material_path(self, material_type):
    return self.paths[material_type]

class MaterialParser():
  def __init__(self): 
    self.regexes = {
      "DIFFUSE": re.compile('(?i).*(diffuse|diff|albedo|col|color|colour).*'),
      "SPECULAR": re.compile('(?i).*(spec|specular).*'),
      "ROUGHNESS": re.compile('(?i).*(refl|reflection).*'),
      "GLOSS": re.compile('(?i).*(refl|reflection|gloss).*'),
      "BUMP": re.compile('(?i).*(bump).*'),
      "NORMAL": re.compile('(?i).*(normal|nrm).*'),
      "DISPLACEMENT": re.compile('(?i).*(displacement|disp).*'),
      "AO": re.compile('(?i).*(ao).*') 
    }

  def create_material(self, files):
    material = Material()
    for path in files:
      for regex_type, pattern in self.regexes.items():
        # print("Checking pattern {} for type {} on path {}" % pattern, regex_type, path)
        if pattern.match(path):
          material.set_material_path(regex_type, path)
          print("Set material id: {} with path: {}".format(regex_type, path))
          continue
    return material

  '''
  regexes

  - Diffuse 
  diffuse
  diff
  albedo
  col
  color
  colour


  - Specular (Reflection)
  _spec
  specular

  - Roughness (or gloss if inverted)
  _refl_
  reflection
  gloss (invert)

  - Bump 
  bump

  - Normal 
  normal
  nrm


  - Displacement
  displacement
  disp
  '''

class FileWalker():
  def print_files(self, path):
    onlyfiles = [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]
    print(onlyfiles)

  def get_files(self, path):
    return [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]


class MaterialImportDialog(c4d.gui.GeDialog):
  def CreateLayout(self):
    return self.LoadDialogResource(materialImportDialog)

  def Command(self, id, msg):
    if (id == MATERIAL_DIRECTORY_PATH):
      file_path = self.GetString(MATERIAL_DIRECTORY_PATH)
      walker = FileWalker()
      walker.print_files(file_path)
      files = walker.get_files(file_path)

      material_parser = MaterialParser()
      material = material_parser.create_material(files)

      doc = c4d.documents.GetActiveDocument()
      mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

      shd = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
      mat.InsertShader(shd)
      mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = shd
      shd[c4d.IMAGETEXTURE_FILE] = material.get_material_path("DIFFUSE")
      shd[c4d.IMAGETEXTURE_MODE] = 0
      shd[c4d.IMAGETEXTURE_GAMMA] = 2.2
      shd[c4d.IMAGETEX_BORDER_MODE] = 0
      doc.InsertMaterial(mat)

    return super(MaterialImportDialog, self).Command(id, msg)


class MaterialImportCommandData(c4d.plugins.CommandData):
    """
    Command Data class that holds the MemoryViewerDialog instance.
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
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaulth=400, defaultw=400)

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
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)



if __name__ == "__main__":
    # Registers the Command plugin
    c4d.plugins.RegisterCommandPlugin(id=PLUGIN_ID, #TODO UPDATE
                                      str="Material Importer",
                                      help="Imports materials for Octane Renderer.",
                                      info=0,
                                      dat=MaterialImportCommandData(),
                                      icon=None)