# Get information about the media 
# 

from PIL import ImageFile
from PIL import ExifTags
import os
import pickle
import base64

exif_keys = ["Size", "Make", "Model"]

def get_info( filename ):
  try:
    im = ImageFile.Image.open( filename )
  except:
    return {}
  try:
    exif = { ExifTags.TAGS[k]: v for k, v in im._getexif().items() if k in ExifTags.TAGS }
  except:
    exif = {}
  size = list( im.size )
  size.sort
  exif["Size"] = "x".join( "%d" % x for x in size )
  return exif


def process_folder( root_folder, verbose = 0 ):
  """ Get info of all image files in the folder 
  """
  global exif_keys
  root_folder = os.path.abspath( root_folder )
  metadata = dict()
  db = dict()
  for base_folder, sub_folder, file_list in os.walk(root_folder):
    for f in file_list:
      filename = os.path.join( base_folder, f )
      #print( "%s:" % ( filename )  )
      exif = get_info( filename )
      metadata[filename] = exif
      if len( exif.keys() ) > 0:
        for k in exif_keys:
          if k in exif.keys():
            k2 = "%s: %s" % ( k, exif[k] )
            if not k2 in db.keys():
              db[k2] = list()
            db[k2].append( filename )

  for k in db.keys():
    print( "%s has %d entries" % ( k, len( db[k] ) ) )



