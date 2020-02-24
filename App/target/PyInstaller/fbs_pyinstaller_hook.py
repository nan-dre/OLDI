import importlib
module = importlib.import_module('fbs_runtime._frozen')
module.BUILD_SETTINGS = {'app_name': 'Biblioteca', 'author': 'Andy', 'version': '0.0.0', 'environment': 'local'}