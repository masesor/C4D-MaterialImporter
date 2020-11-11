from material import Material
from os.path import isfile, isdir, join
import re
import c4d
import os
import json

import constants

class ParserData():
  def __init__(self, regex, material_id, is_float = False):
    self.__regex = regex
    self.__material_id = material_id
    self.__is_float = is_float

  def get_regex(self):
    return self.__regex

  def get_material_id(self):
    return self.__material_id

  def is_float(self):
    return self.__is_float

PARSER_DATA = {
  constants.DIFFUSE: ParserData(re.compile('(?i).*(diffuse|diff|albedo|col|color|colour).*'), c4d.OCT_MATERIAL_DIFFUSE_LINK),
  constants.SPECULAR: ParserData(re.compile('(?i).*(spec|specular|refl|reflection).*'), c4d.OCT_MATERIAL_SPECULAR_LINK, True),
  constants.ROUGHNESS: ParserData(re.compile('(?i).*(rough).*'), c4d.OCT_MATERIAL_ROUGHNESS_LINK, True),
  # constants.GLOSS: ParserData(re.compile('(?i).*(refl|reflection|gloss).*'), True),
  constants.BUMP: ParserData(re.compile('(?i).*(bump).*'), c4d.OCT_MATERIAL_BUMP_LINK, True),
  constants.NORMAL: ParserData(re.compile('(?i).*(normal|nrm).*'), c4d.OCT_MATERIAL_NORMAL_LINK),
  constants.DISPLACEMENT: ParserData(re.compile('(?i).*(displacement|disp).*'), c4d.OCT_MATERIAL_DISPLACEMENT_LINK, True)
  # constants.AO: ParserData(re.compile('(?i).*(ao).*'), True)
}	
	
def create_material(files, directory):
  material = Material()
  for file_path in files:
    for regex_type, data in PARSER_DATA.items():
      file_name = get_file_name_from_path(file_path)
      if data.get_regex().match(file_name):
        material.set_material_path(regex_type, file_path)
        set_material_name(material, directory, file_name)
        break
  return material

def set_material_name(material, directory, file_name):
  manifest_data = read_json_manifest(directory)
  material.set_name(manifest_data['name'] if manifest_data else file_name)

def get_file_name_from_path(file_path):
  split_path = file_path.split(os.sep)
  return split_path[len(split_path) - 1]

def read_json_manifest(directory):
  json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
  
  manifest_file = None
  if json_files:
    manifest_file = json_files[0]

  if manifest_file:
    with open(directory + os.sep + manifest_file, 'r') as manifest:
      data = manifest.read()
    
      return json.loads(data)