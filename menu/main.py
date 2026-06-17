import math
import os
import time
import json
import subprocess

import pygame as pg

class Constants:
	RESOLUTION:tuple = (1920, 1080)
	FPS:int = 100
	DISPLAY_MODE:int = pg.FULLSCREEN
	DEFAULT_FONT_SIZE = 16

	GAMES_PATH = "games"
	MENU_GRID_ROWS = 3
	MENU_GRID_COLS = 5
	MENU_GAMES_PER_SLIDE = MENU_GRID_ROWS * MENU_GRID_COLS

	CNSL_ERROR:str = "\x1b[1;31m"
	CNSL_SUCCESS:str = "\x1b[1;32m"
	CNSL_DATA:str = "\x1b[1;33m"
	CNSL_INFO:str = "\x1b[1;34m"
	CNSL_RESET:str = "\x1B[0m"

	COLOR_PRIMARY:pg.Color = pg.Color("#0094AA")
	COLOR_SECONDARY:pg.Color = pg.Color("#52AE32")
	COLOR_DARK:pg.Color = pg.Color("#424242")

	SCREENSAVER_TIMEOUT_MS = 10000
	SCREENSAVER_OVERLAY_OPACITY = 127
	SCREENSAVER_FONT_PATH = "./assets/font.ttf"
	SCREENSAVER_MESSAGE_OF_THE_DAY = "New games expected soon!"


def fetchGames(path=Constants.GAMES_PATH):
	games = []
	if not os.path.isdir(path):
		return games

	for index, folder in enumerate(sorted(os.listdir(path))):
		game_dir = os.path.join(path, folder)
		if not os.path.isdir(game_dir):
			continue

		metadata_path = os.path.join(game_dir, "metadata.json")
		if not os.path.exists(metadata_path):
			continue

		try:
			with open(metadata_path, "r", encoding="utf-8") as f:
				metadata = json.load(f)
		except Exception:
			continue

		screenshot_path = os.path.join(game_dir, "screenshot.jpg")
		if not os.path.exists(screenshot_path):
			screenshot_path = None

		entrypoint = metadata.get("entrypoint")
		if not entrypoint:
			continue

		games.append(
			{
				"id": index,
				"name": metadata.get("name", folder),
				"authors": metadata.get("authors", []),
				"entrypoint": os.path.join(game_dir, entrypoint),
				"screenshotPath": screenshot_path,
			}
		)

	return games


def start_game(path):
	print(Constants.CNSL_DATA, "[GAME PATH]", path, Constants.CNSL_RESET)
	game_dir = os.path.dirname(path)
	game_file = os.path.basename(path)
	env = os.environ.copy()
	env.setdefault("DISPLAY", ":1")

	try:
		result = subprocess.run(
			["python3", game_file],
			cwd=game_dir,
			env=env,
			capture_output=True,
			text=True,
		)
		if result.stdout:
			print(result.stdout)
		if result.stderr:
			print("[GAME ERROR]", result.stderr)
	except Exception as e:
		print(f"{Constants.CNSL_ERROR}[GAME UTIL] Game failed to launch: {e}")


TILE_W = 300
TILE_H = 168
TILE_X_SPACING = 330
TILE_Y_SPACING = 250
GRID_PADDING = 6
HEADER_Y = 100
GRID_TOP_OFFSET = 80
LABEL_FONT_SIZE = 22
LABEL_TOP_MARGIN = 10
LABEL_LINE_SPACING = 4
LABEL_MAX_LINES = 2
LABEL_SIDE_PADDING = 10
SCREENSAVER_CONFIG = [
	{"mode": "scroll", "duration_ms": 500},
	{"mode": "visible", "duration_ms": 2000},
	{"mode": "invisible", "duration_ms": 250},
	{"mode": "visible", "duration_ms": 500},
	{"mode": "invisible", "duration_ms": 250},
	{"mode": "visible", "duration_ms": 500},
	{"mode": "invisible", "duration_ms": 250},
	{"mode": "visible", "duration_ms": 10000},
]
SCREENSAVER_TEXT_COLOR = (0, 255, 0)
SCREENSAVER_MESSAGE_COLOR = (255, 255, 255)
SCREENSAVER_LINES = [
	{"text": "HIT ANY KEY", "font_size": 80, "color": SCREENSAVER_TEXT_COLOR, "y_offset": -220},
	{"text": "LET'S PLAY!", "font_size": 120, "color": SCREENSAVER_TEXT_COLOR, "y_offset": -60},
	{"text": "games gemaakt door leerlingen", "font_size": 80, "color": SCREENSAVER_TEXT_COLOR, "y_offset": 220},
	{"text": "4e klas informatica", "font_size": 80, "color": SCREENSAVER_TEXT_COLOR, "y_offset": 380},
	{"text": "{MOTD}", "font_size": 40, "color": SCREENSAVER_MESSAGE_COLOR, "y_offset": 460},
]


def load_font(size:int):
	try:
		return pg.font.Font("./assets/font.ttf", size)
	except Exception:
		return pg.font.SysFont(None, size)


def load_background() -> pg.Surface:
	try:
		return pg.image.load("assets/menu_background.jpg").convert()
	except Exception:
		bg = pg.Surface(Constants.RESOLUTION)
		bg.fill((15, 20, 25))
		return bg


def build_placeholder(size:tuple[int, int]) -> pg.Surface:
	surf = pg.Surface(size)
	surf.fill((24, 28, 36))
	pg.draw.rect(surf, (36, 44, 56), surf.get_rect(), 3, border_radius=8)
	return surf


def load_tile_image(path:str | None, placeholder:pg.Surface) -> pg.Surface:
	if path:
		try:
			img = pg.image.load(path).convert()
			return pg.transform.smoothscale(img, (TILE_W, TILE_H))
		except Exception:
			pass
	return placeholder.copy()


def trim_to_width(text:str, max_width:int, font:pg.font.Font) -> str:
	if font.render(text, True, Constants.COLOR_PRIMARY).get_width() <= max_width:
		return text

	value = text
	while len(value) > 1:
		candidate = value[:-1].rstrip() + "..."
		if font.render(candidate, True, Constants.COLOR_PRIMARY).get_width() <= max_width:
			return candidate
		value = value[:-1]
	return "..."


def wrap_title(text:str, font:pg.font.Font) -> list[str]:
	max_width = TILE_W - (LABEL_SIDE_PADDING * 2)
	words = text.split()
	if not words:
		return [""]

	lines = []
	current = ""
	i = 0
	while i < len(words) and len(lines) < LABEL_MAX_LINES:
		word = words[i]
		candidate = word if not current else f"{current} {word}"
		if font.render(candidate, True, Constants.COLOR_PRIMARY).get_width() <= max_width:
			current = candidate
			i += 1
			continue

		if current:
			lines.append(current)
			current = ""
		else:
			lines.append(trim_to_width(word, max_width, font))
			i += 1

	if len(lines) < LABEL_MAX_LINES and current:
		lines.append(current)

	if i < len(words):
		overflow = " ".join(words[i:])
		if lines:
			lines[-1] = trim_to_width(f"{lines[-1]} {overflow}".strip(), max_width, font)
		else:
			lines.append(trim_to_width(overflow, max_width, font))

	return lines[:LABEL_MAX_LINES]


def build_tiles() -> tuple[list[dict], dict]:
	games = fetchGames()
	print(f"{Constants.CNSL_DATA}[GAMES]: {[g['name'] for g in games]}{Constants.CNSL_RESET}")

	placeholder = build_placeholder((TILE_W, TILE_H))
	page_size = Constants.MENU_GAMES_PER_SLIDE
	page_count = max(1, math.ceil(len(games) / page_size))
	page_cols = max(1, math.ceil(math.sqrt(page_count)))
	page_rows = max(1, math.ceil(page_count / page_cols))

	tiles = []
	for idx, game in enumerate(games):
		page_index = idx // page_size
		slot_index = idx % page_size

		page_x = page_index % page_cols
		page_y = page_index // page_cols
		grid_col = slot_index % Constants.MENU_GRID_COLS
		grid_row = slot_index // Constants.MENU_GRID_COLS

		tile_rect = pg.Rect(
			grid_col * TILE_X_SPACING + GRID_PADDING,
			grid_row * TILE_Y_SPACING + GRID_PADDING,
			TILE_W,
			TILE_H,
		)

		tiles.append(
			{
				"id": idx,
				"name": game["name"],
				"entrypoint": game["entrypoint"],
				"page_x": page_x,
				"page_y": page_y,
				"grid_col": grid_col,
				"grid_row": grid_row,
				"rect": tile_rect,
				"image": load_tile_image(game["screenshotPath"], placeholder),
			}
		)

	state = {
		"page_cols": page_cols,
		"page_rows": page_rows,
		"page_count": page_count,
		"page_x": 0,
		"page_y": 0,
		"sel_col": 0,
		"sel_row": 0,
		"last_input_ms": int(time.time() * 1000),
		"screensaver": build_screensaver(),
	}
	return tiles, state


def _load_screensaver_font(size:int) -> pg.font.Font:
	try:
		return pg.font.Font(Constants.SCREENSAVER_FONT_PATH, size)
	except Exception:
		return load_font(size)


def build_screensaver() -> dict:
	lines = []
	for line in SCREENSAVER_LINES:
		resolved_text = line["text"].replace("{MOTD}", Constants.SCREENSAVER_MESSAGE_OF_THE_DAY)
		lines.append(
			{
				"text": resolved_text,
				"font_size": line["font_size"],
				"color": line["color"],
				"y_offset": line["y_offset"],
			}
		)

	font_cache = {}
	for line in lines:
		size = line["font_size"]
		if size not in font_cache:
			font_cache[size] = _load_screensaver_font(size)

	image = pg.Surface(Constants.RESOLUTION, pg.SRCALPHA)
	for line in lines:
		font = font_cache[line["font_size"]]
		text_surf = font.render(line["text"], True, line["color"])
		rect = text_surf.get_rect(
			center=(Constants.RESOLUTION[0] // 2, Constants.RESOLUTION[1] // 2 + line["y_offset"])
		)
		image.blit(text_surf, rect)

	overlay = pg.Surface(Constants.RESOLUTION, pg.SRCALPHA)
	overlay.fill((0, 0, 0, Constants.SCREENSAVER_OVERLAY_OPACITY))

	now = time.time()
	return {
		"active": False,
		"visible": True,
		"image": image,
		"overlay": overlay,
		"config": SCREENSAVER_CONFIG,
		"state_index": 0,
		"current_mode": "scroll",
		"current_duration_s": SCREENSAVER_CONFIG[0]["duration_ms"] / 1000.0,
		"state_start_s": now,
		"last_update_s": now,
		"scroll_y": float(Constants.RESOLUTION[1]),
		"scroll_speed": float(Constants.RESOLUTION[1]) / (SCREENSAVER_CONFIG[0]["duration_ms"] / 1000.0),
	}


def _set_screensaver_state(saver:dict, state_index:int) -> None:
	state = saver["config"][state_index]
	saver["state_index"] = state_index
	saver["current_mode"] = state["mode"]
	saver["current_duration_s"] = state["duration_ms"] / 1000.0
	saver["state_start_s"] = time.time()
	if saver["current_mode"] == "scroll":
		saver["scroll_y"] = float(Constants.RESOLUTION[1])
		saver["scroll_speed"] = float(Constants.RESOLUTION[1]) / saver["current_duration_s"]


def activate_screensaver(state:dict) -> None:
	saver = state["screensaver"]
	saver["active"] = True
	saver["visible"] = True
	saver["last_update_s"] = time.time()
	_set_screensaver_state(saver, 0)


def deactivate_screensaver(state:dict) -> None:
	state["screensaver"]["active"] = False


def update_screensaver(state:dict) -> None:
	saver = state["screensaver"]
	if not saver["active"]:
		return

	now = time.time()
	mode = saver["current_mode"]

	if mode == "scroll":
		elapsed = now - saver["last_update_s"]
		saver["scroll_y"] -= saver["scroll_speed"] * elapsed
		if saver["scroll_y"] <= 0:
			saver["scroll_y"] = 0
		saver["visible"] = True
	elif mode == "invisible":
		saver["visible"] = False
	else:
		saver["visible"] = True

	if now - saver["state_start_s"] >= saver["current_duration_s"]:
		next_index = saver["state_index"] + 1
		if next_index >= len(saver["config"]):
			next_index = 0
		_set_screensaver_state(saver, next_index)

	saver["last_update_s"] = now


def tiles_on_page(tiles:list[dict], page_x:int, page_y:int) -> list[dict]:
	return [t for t in tiles if t["page_x"] == page_x and t["page_y"] == page_y]


def select_best_tile(page_tiles:list[dict], preferred_col:int, preferred_row:int):
	if not page_tiles:
		return None

	exact = [t for t in page_tiles if t["grid_col"] == preferred_col and t["grid_row"] == preferred_row]
	if exact:
		return exact[0]

	same_row = [t for t in page_tiles if t["grid_row"] == preferred_row]
	if same_row:
		return min(same_row, key=lambda t: abs(t["grid_col"] - preferred_col))

	return min(page_tiles, key=lambda t: (abs(t["grid_row"] - preferred_row), abs(t["grid_col"] - preferred_col)))


def current_tile(tiles:list[dict], state:dict):
	page_tiles = tiles_on_page(tiles, state["page_x"], state["page_y"])
	return select_best_tile(page_tiles, state["sel_col"], state["sel_row"])


def try_move_selection(tiles:list[dict], state:dict, delta_col:int, delta_row:int):
	new_col = state["sel_col"] + delta_col
	new_row = state["sel_row"] + delta_row

	# Try local movement first.
	local_tile = select_best_tile(tiles_on_page(tiles, state["page_x"], state["page_y"]), new_col, new_row)
	if local_tile and local_tile["grid_col"] == new_col and local_tile["grid_row"] == new_row:
		state["sel_col"] = new_col
		state["sel_row"] = new_row
		return

	# Horizontal page overflow.
	if new_col >= Constants.MENU_GRID_COLS:
		target_x = state["page_x"] + 1
		target_y = state["page_y"]
		if target_x < state["page_cols"]:
			target_tile = select_best_tile(tiles_on_page(tiles, target_x, target_y), 0, state["sel_row"])
			if target_tile:
				state["page_x"] = target_x
				state["sel_col"] = target_tile["grid_col"]
				state["sel_row"] = target_tile["grid_row"]
		return

	if new_col < 0:
		target_x = state["page_x"] - 1
		target_y = state["page_y"]
		if target_x >= 0:
			target_tile = select_best_tile(tiles_on_page(tiles, target_x, target_y), Constants.MENU_GRID_COLS - 1, state["sel_row"])
			if target_tile:
				state["page_x"] = target_x
				state["sel_col"] = target_tile["grid_col"]
				state["sel_row"] = target_tile["grid_row"]
		return

	# Vertical page overflow.
	if new_row >= Constants.MENU_GRID_ROWS:
		target_x = state["page_x"]
		target_y = state["page_y"] + 1
		if target_y < state["page_rows"]:
			target_tile = select_best_tile(tiles_on_page(tiles, target_x, target_y), state["sel_col"], 0)
			if target_tile:
				state["page_y"] = target_y
				state["sel_col"] = target_tile["grid_col"]
				state["sel_row"] = target_tile["grid_row"]
		return

	if new_row < 0:
		target_x = state["page_x"]
		target_y = state["page_y"] - 1
		if target_y >= 0:
			target_tile = select_best_tile(tiles_on_page(tiles, target_x, target_y), state["sel_col"], Constants.MENU_GRID_ROWS - 1)
			if target_tile:
				state["page_y"] = target_y
				state["sel_col"] = target_tile["grid_col"]
				state["sel_row"] = target_tile["grid_row"]
		return

	# In bounds but empty cell: snap to closest tile in that row.
	same_page = tiles_on_page(tiles, state["page_x"], state["page_y"])
	snapped = select_best_tile(same_page, new_col, new_row)
	if snapped and snapped["grid_row"] == new_row:
		state["sel_col"] = snapped["grid_col"]
		state["sel_row"] = snapped["grid_row"]


def launch_selected(screen:pg.Surface, tile:dict | None):
	if not tile:
		return screen
	try:
		pg.display.set_mode((1, 1), pg.HIDDEN)
	except Exception:
		pg.display.iconify()

	start_game(tile["entrypoint"])
	pg.event.clear()
	return pg.display.set_mode(Constants.RESOLUTION, Constants.DISPLAY_MODE)


def draw_menu(screen:pg.Surface, bg:pg.Surface, tiles:list[dict], state:dict, header_font:pg.font.Font, label_font:pg.font.Font):
	screen.blit(bg, (0, 0))

	title = header_font.render("STANISLAS ARCADE", True, Constants.COLOR_PRIMARY)
	title_shadow = header_font.render("STANISLAS ARCADE", True, Constants.COLOR_SECONDARY)
	title_rect = title.get_rect(center=(Constants.RESOLUTION[0] // 2, HEADER_Y))
	shadow_rect = title_shadow.get_rect(center=(title_rect.centerx + 10, title_rect.centery - 2))
	screen.blit(title_shadow, shadow_rect)
	screen.blit(title, title_rect)

	selected = current_tile(tiles, state)
	for tile in tiles_on_page(tiles, state["page_x"], state["page_y"]):
		tile_rect = tile["rect"].move(
			Constants.RESOLUTION[0] // 2 - ((Constants.MENU_GRID_COLS - 1) * TILE_X_SPACING + TILE_W + 12) // 2,
			Constants.RESOLUTION[1] // 2 - ((Constants.MENU_GRID_ROWS - 1) * TILE_Y_SPACING + TILE_H + 12) // 2 + GRID_TOP_OFFSET,
		)

		screen.blit(tile["image"], tile_rect.topleft)
		if selected and tile["id"] == selected["id"]:
			pg.draw.rect(screen, Constants.COLOR_PRIMARY, tile_rect.inflate(8, 8), 6, border_radius=10)

		lines = wrap_title(tile["name"], label_font)
		for i, line in enumerate(lines):
			txt = label_font.render(line, True, Constants.COLOR_PRIMARY)
			txt_rect = txt.get_rect(midtop=(tile_rect.centerx, tile_rect.bottom + LABEL_TOP_MARGIN + i * (LABEL_FONT_SIZE + LABEL_LINE_SPACING)))
			screen.blit(txt, txt_rect)

	# simple page indicator
	page_label = label_font.render(
		f"Pagina {state['page_y'] * state['page_cols'] + state['page_x'] + 1}/{state['page_count']}",
		True,
		Constants.COLOR_SECONDARY,
	)
	screen.blit(page_label, (40, Constants.RESOLUTION[1] - 60))


def draw_screensaver(screen:pg.Surface, state:dict):
	saver = state["screensaver"]
	if not saver["active"]:
		return

	screen.blit(saver["overlay"], (0, 0))
	if saver["visible"]:
		screen.blit(saver["image"], (0, int(saver["scroll_y"])))


def run_menu():
	pg.init()
	screen = pg.display.set_mode(Constants.RESOLUTION, Constants.DISPLAY_MODE)
	clock = pg.time.Clock()
	pg.mouse.set_visible(False)

	header_font = load_font(108)
	label_font = load_font(LABEL_FONT_SIZE)
	bg = load_background()

	tiles, state = build_tiles()
	if not tiles:
		print(f"{Constants.CNSL_ERROR}[MENU] Geen games gevonden.{Constants.CNSL_RESET}")
		return

	running = True
	launch_keys = {
		pg.K_q, pg.K_e, pg.K_r, pg.K_z, pg.K_x, pg.K_c,
		pg.K_u, pg.K_o, pg.K_p, pg.K_b, pg.K_n, pg.K_m,
		pg.K_RETURN, pg.K_SPACE,
	}

	while running:
		now_ms = int(time.time() * 1000)
		if not state["screensaver"]["active"] and now_ms - state["last_input_ms"] > Constants.SCREENSAVER_TIMEOUT_MS:
			activate_screensaver(state)

		update_screensaver(state)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
				break

			if event.type != pg.KEYDOWN:
				continue

			state["last_input_ms"] = now_ms
			if state["screensaver"]["active"]:
				deactivate_screensaver(state)
				continue

			if event.key == pg.K_ESCAPE:
				running = False
				break

			if event.key in (pg.K_w, pg.K_i):
				try_move_selection(tiles, state, 0, -1)
			elif event.key in (pg.K_s, pg.K_k):
				try_move_selection(tiles, state, 0, 1)
			elif event.key in (pg.K_a, pg.K_j):
				try_move_selection(tiles, state, -1, 0)
			elif event.key in (pg.K_d, pg.K_l):
				try_move_selection(tiles, state, 1, 0)
			elif event.key in launch_keys:
				screen = launch_selected(screen, current_tile(tiles, state))

		if not running:
			break

		draw_menu(screen, bg, tiles, state, header_font, label_font)
		draw_screensaver(screen, state)

		pg.display.update()
		clock.tick(Constants.FPS)

	pg.quit()


if __name__ == "__main__":
	run_menu()
