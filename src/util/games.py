import sys, glob, json, os, subprocess
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
	files = glob.glob(os.path.join(path, "/", "*"))
 
	print(files)

	pass
	res = []
	
	for index, gamePath in enumerate(files):
		gameDir = gamePath.split("\\")[-1]
		
		metadata = None
		
		with open(f"{path}/{gameDir}/metadata.json", "r") as file:
			metadata = json.load(file)
		
		instructions = None

		try:
			file = SourceFileLoader(metadata['instructionspage'][:-3], f"{path}/{gameDir}/{metadata['instructionspage']}").load_module()
			instructions = file.page
		except:
			pass

		pathToGame = f"{path}/{gameDir}/{metadata['entrypoint']}"
		
		res.append(Game(index, metadata['name'], metadata['author'], instructions, pathToGame ))
	
	return res

def start_game(path):
	print(Constants.CNSL_DATA, "[GAME PATH] ", path, Constants.CNSL_RESET)
	
	# os.system(f"python {path}") THIS WORKS AS WELL BUT NOT SURE IF IT WORKS SAME ON ALL OS
	
	try:
		result = subprocess.run(["python", path], shell=True, capture_output=True, text=True, check=True)
		print(result.stderr, result.stdout)
	except:
		print(f"{Constants.CNSL_ERROR}[GAME UTIL] Game failed to launch")