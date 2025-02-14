import sys, glob, json
from util.constants import Constants
from importlib.machinery import SourceFileLoader

class Game():
	def __init__(self ,id, name, author, instructionsPage, pathToGame):
		self.id = id
		self.name = name
		self.author = author
		self.instructionsPage = instructionsPage
		self.entrypoint = pathToGame

def fetchGames(path=Constants.GAMES_PATH) -> list:
	searchPath = "\\".join(sys.path[0].split("\\")[:-2]) + path
	sys.path.append(searchPath)
	
	files = glob.glob(f"{searchPath}/*")
	res = []
	
	for index, gamePath in enumerate(files):
		gameDir = gamePath.split("\\")[-1]
		
		metadata = None
		
		with open(f"{path}/{gameDir}/metadata.json", "r") as file:
			metadata = json.load(file)
		
		instructions = SourceFileLoader(metadata['instructionspage'][:-3], f"{path}/{gameDir}/{metadata['instructionspage']}").load_module()
		
		# game = SourceFileLoader(metadata['entrypoint'][:-3], f"{path}/{gameDir}/{metadata['entrypoint']}").load_module()
		pathToGame = f"{path}/{gameDir}/{metadata['entrypoint']}"
		
		res.append(Game(index, metadata['name'], metadata['author'], instructions.page, pathToGame ))
	
	return res

def start_game(path):
    SourceFileLoader("main", path).load_module()