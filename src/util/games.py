import json, os, subprocess
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
		# not implemented, as old implementation resized screen in some cases
		instructions = None

		res.append(Game(index, metadata['name'], metadata['authors'], instructions, os.path.join(gameDir, metadata["entrypoint"])))

	return res

def start_game(path):
    print(Constants.CNSL_DATA, "[GAME PATH] ", path, Constants.CNSL_RESET)

    game_dir = os.path.dirname(path)
    game_file = os.path.basename(path)

    # Copy environment and ensure DISPLAY is set for TigerVNC / noVNC
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":1")  # or whatever display VNC uses

    try:
        result = subprocess.run(
            ["python3", game_file],
            cwd=game_dir,
            env=env,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("[GAME ERROR]", result.stderr)
    except Exception as e:
        print(f"{Constants.CNSL_ERROR}[GAME UTIL] Game failed to launch: {e}")