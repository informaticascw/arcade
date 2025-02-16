import sys, glob, json, os, subprocess
from util.constants import Constants
from importlib.machinery import SourceFileLoader

class Game():
	def __init__(self ,id, name, authors, instructionsPage, pathToGame):
		self.id = id
		self.name = name
		self.authors = authors
		self.instructionsPage = instructionsPage
		self.entrypoint = pathToGame

def fetchGames(path=Constants.GAMES_PATH) -> list:
	res = []
	for index, dir in enumerate(os.listdir(path)):
		gameDir = os.path.join(path, dir)
  
		# Get the metadata
		metadata = None
		try:
			with open(os.path.join(gameDir, "metadata.json"), "r") as f:
				metadata = json.load(f)
		except:
			raise Exception(f"{gameDir} does not contain a metadata.json file, please add one or remove the game.")

		# Get the instruction if there are
		instructions = None
		try:
			file = SourceFileLoader(metadata["instructionspage"].replace(".py", ""), os.path.join(gameDir, metadata["instructionspage"])).load_module()
			instructions = file.page
		except:
			pass

		res.append(Game(index, metadata['name'], metadata['authors'], instructions, os.path.join(gameDir, metadata["entrypoint"])))

	return res
 
def start_game(path):
	print(Constants.CNSL_DATA, "[GAME PATH] ", path, Constants.CNSL_RESET)
	
	# os.system(f"python {path}") THIS WORKS AS WELL BUT NOT SURE IF IT WORKS SAME ON ALL OS
 
	print(f"cd {os.path.dirname(path)} && python {os.path.basename(path)}",)
 
	try:
		result = subprocess.run(f"cd {os.path.dirname(path)} && python {os.path.basename(path)}", shell=True)
		print(result.stderr, result.stdout)
	except:
		print(f"{Constants.CNSL_ERROR}[GAME UTIL] Game failed to launch")