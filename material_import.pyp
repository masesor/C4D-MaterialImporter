import c4d
from c4d import gui
import os
from os.path import isfile, isdir, join
import sys

sys.path.append(c4d.storage.GeGetStartupPath() + "\\plugins\\MaterialImport")
import constants
import material_parser
import material

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


class MaterialImportDialog(c4d.gui.GeDialog):
  def CreateLayout(self):
    return self.LoadDialogResource(constants.MATERIAL_IMPORT_DIALOG)

  def Command(self, id, msg):
    if (id == constants.MATERIAL_DIRECTORY_PATH):
      self.handle_open_directory()
    return super(MaterialImportDialog, self).Command(id, msg)

  def handle_open_directory(self):
    current_path = self.GetString(constants.MATERIAL_DIRECTORY_PATH)
    material_data = self.get_materials_from_path(current_path)      
    for data in material_data:
      specular_material = material.create_octane_specular_material(data)
      doc = c4d.documents.GetActiveDocument()
      doc.InsertMaterial(specular_material)


  def get_materials_from_path(self, file_path):
    walker = Walker()
    directories = walker.get_directories(file_path)
    current_directory_files = walker.get_files(file_path)

    materials = []
    for directory in directories:
      files = walker.get_files(directory)
      materials.append(material_parser.create_material(files, directory))

    if current_directory_files:
      materials.append(material_parser.create_material(current_directory_files, file_path))

    return materials


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
