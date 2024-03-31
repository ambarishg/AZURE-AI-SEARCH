# AZURE AI SEARCH CONFIGURATION
from dotenv import load_dotenv
from dotenv import dotenv_values


load_dotenv()
values_env = dotenv_values(".env")

searchservice = values_env['searchservice']
index = values_env['index']
searchkey = values_env['searchkey']
category=values_env['category']

#AZURE STORAGE CONFIGURATION
storageaccount  = values_env['storageaccount']
container=values_env['container']
storagekey=values_env['storagekey']

localpdfparser=values_env['localpdfparser']
verbose=values_env['verbose']

FILE_PATH = values_env['FILE_PATH']

formrecognizerservice=values_env['formrecognizerservice']
