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
  constants.SPECULAR: ParserData(re.compile('(?i).*(spec|specular).*'), c4d.OCT_MATERIAL_SPECULAR_LINK, True),
  constants.ROUGHNESS: ParserData(re.compile('(?i).*(rough).*'), c4d.OCT_MATERIAL_ROUGHNESS_LINK, True),
  constants.GLOSS: ParserData(re.compile('(?i).*(refl|reflection|gloss).*'), True),
  constants.BUMP: ParserData(re.compile('(?i).*(bump).*'), c4d.OCT_MATERIAL_BUMP_LINK, True),
  constants.NORMAL: ParserData(re.compile('(?i).*(normal|nrm).*'), c4d.OCT_MATERIAL_NORMAL_LINK),
  constants.DISPLACEMENT: ParserData(re.compile('(?i).*(displacement|disp).*'), c4d.OCT_MATERIAL_DISPLACEMENT_LINK, True),
  constants.AO: ParserData(re.compile('(?i).*(ao).*'), True)
}	
	
def create_material(files, directory):
  material = Material()
  for file_path in files:
    for regex_type, data in PARSER_DATA.items():
      if data.get_regex().match(file_path):
        material.set_material_path(regex_type, file_path)
        material.set_is_float(data.is_float)
        set_material_name(material, directory)
        continue
  return material

def set_material_name(material, directory):
  manifest_data = read_json_manifest(directory)
  if not manifest_data:
    split_path = directory.split(os.sep)
    material_name = split_path[len(split_path)]
  material.set_name(manifest_data['name'] if manifest_data else material_name)

def read_json_manifest(directory):
  manifest_file = [f for f in os.listdir(directory) if f.endswith('.json')][0]

  if manifest_file:
    with open(directory + os.sep + manifest_file, 'r') as manifest:
      data = manifest.read()
    
      return json.loads(data)