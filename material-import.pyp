import c4d
from c4d import gui
import collections
import os
from os.path import isfile, join

PLUGIN_ID = 1025249

materialImportDialog = 100001
MATERIAL_DIRECTORY_PATH = 100002

# OCtane IDs
ID_OCTANE_DIFFUSE_MATERIAL = 1029501
ID_OCTANE_IMAGE_TEXTURE = 1029508

class MaterialParser():
  self.diffuse_regex = '(?i).*(diffuse|diff|albedo|col|color|colour).*'
  self.specular_regex = '(?i).*(spec|specular).*'
  self.roughness_regex = '(?i).*(refl|reflection).*'
  self.gloss_regex = '(?i).*(refl|reflection).*'
  self.bump_regex = '(?i).*(bump).*'
  self.normal_regex = '(?i).*(normal|nrm).*'
  self.displacement_regex = '(?i).*(displacement|disp).*'
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
    onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
    print(onlyfiles)


class MaterialImportDialog(c4d.gui.GeDialog):
  def CreateLayout(self):
    return self.LoadDialogResource(materialImportDialog)

  def Command(self, id, msg):
    if (id == MATERIAL_DIRECTORY_PATH):
      file_path = self.GetString(MATERIAL_DIRECTORY_PATH)
      walker = FileWalker()
      walker.print_files(file_path)

      doc = c4d.documents.GetActiveDocument()
      mat = c4d.BaseMaterial(ID_OCTANE_DIFFUSE_MATERIAL)

      shd = c4d.BaseShader(ID_OCTANE_IMAGE_TEXTURE)
      mat.InsertShader(shd)
      mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = shd
      shd[c4d.IMAGETEXTURE_FILE] = "texture.jpg"
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