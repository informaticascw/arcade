import sys, glob, json
from util.constants import Constants
from importlib.machinery import SourceFileLoader

class Game():
	def __init__(self ,id, name, author, instructionsPage, game):
		self.id = id
		self.name = name
		self.author = author
		self.instructionsPage = instructionsPage
		self.entrypoint = game

def fetchGames(path=Constants.GAMES_PATH) -> list:
	searchPath = "\\".join(sys.path[0].split("\\")[:-2]) + path
	sys.path.append(searchPath)
	
	files = glob.glob(f"{searchPath}/*")
	res = []
	
	for index, gamePath in enumerate(files):
		gameDir = gamePath.split("\\")[-1]
		
		print(gamePath, gameDir)
		
		metadata = None
		
		with open(f"{path}/{gameDir}/metadata.json", "r") as file:
			metadata = json.load(file)
		
		instructions = SourceFileLoader(metadata['instructionspage'][:-3], f"{path}/{gameDir}/{metadata['instructionspage']}").load_module()
		
		game = SourceFileLoader(metadata['entrypoint'][:-3], f"{path}/{gameDir}/{metadata['entrypoint']}").load_module()
		
		res.append(Game(index, metadata['name'], metadata['author'], instructions.page, game ))
	
	return res