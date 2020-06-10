import c4d
import collections
import os
from os.path import isfile, join

PLUGIN_ID = 1025249

materialImportDialog = 100001
MATERIAL_DIRECTORY_PATH = 100002

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