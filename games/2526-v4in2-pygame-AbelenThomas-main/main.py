#
# BREAKOUT GAME 
#

import pygame
import random
import json
import os
import time

# definitions 
FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16 
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32    # ballsize in y-direction in pixels
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

ball_x = 0           # x-position of ball in pixels
ball_speed_x = 6     # speed of ball in x-direction in pixels per frame
ball_y = 0
ball_speed_y = 10
paddle_x = 0
paddle_y = SCREEN_HEIGHT - 100
score = 0
brick_effects = []

player_name = ""
combo = 1
last_hit_time = 0.0
multiplier = 1
score_saved = False

ball_locked = True

lives = 3



HIGHSCORE_FILE = "highscores.json"

def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE): # Controleert of het highscores-bestand bestaat
        return [] # Als het bestand niet bestaat, geef een lege lijst terug
    with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f) # Lees de JSON-data uit het bestand en geef deze terug
        except json.JSONDecodeError:
            return [] # Als de JSON-data een error heeft of leeg is, geef een lege lijst terug

def save_highscore(name, score_value):
    scores = load_highscores() # Laad de bestaande highscores
    scores.append({"name": name, "score": score_value}) # Voeg de nieuwe score toe aan de lijst
    scores = sorted(scores, key=lambda x: x["score"], reverse=True) # Sorteer de scores van hoog naar laag
    scores = scores[:9]  # bewaar top 9
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4) # Schrijf de highscores netjes geformatteerd naar het bestand

def start_brick_effect(x, y, color):
  brick_effects.append({
    "x": x,
    "y": y,
    "color": color,
    "vy": -8, # snelheid omhoog
    "alpha": 255 # begint volledig zichtbaar
  })

# originele bricks setup voor reset
bricks_x_original = [544, 640,
            448, 544, 640, 736,
            352, 448, 544, 640, 736, 832,
            352, 448, 544, 640, 736, 832,
            448, 544, 640, 736,
            544, 640]
bricks_y_original = [100, 100,
            132, 132, 132, 132,
            164, 164, 164, 164, 164, 164,
            196, 196, 196, 196, 196, 196,
            228, 228, 228, 228,
            260, 260]

# Meerdere kleuren
bricks_color_original = ["green","lightgreen",
    "purple","blue","orange","lightblue",
    "yellow","grey","green","brown","yellow","blue",
    "purple","red","red","red","red","red",
    "green","lightgreen","green","lightblue",
    "brown","purple"]

bricks_x = bricks_x_original.copy()
bricks_y = bricks_y_original.copy()
bricks_color = bricks_color_original.copy()
bricks_hp_original = [2] * len(bricks_x_original)
bricks_hp = bricks_hp_original.copy()

# define global variables
game_status = "naam_invoer"

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x, bricks_x, bricks_y, bricks_hp, bricks_color
    global score, combo, last_hit_time, multiplier, score_saved
    
    ball_x = (SCREEN_WIDTH - BALL_WIDTH) / 2
    ball_y = 300
    ball_speed_x = 6
    ball_speed_y = 10
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) / 2
    bricks_x = bricks_x_original.copy()
    bricks_y = bricks_y_original.copy()
    bricks_color = bricks_color_original.copy()
    random.shuffle(bricks_color)  # Random kleurschikking
    bricks_hp = bricks_hp_original.copy()
    score = 0
    combo = 1
    last_hit_time = 0.0
    multiplier = 1
    score_saved = False
    global ball_locked
    ball_locked = True
    global lives
    lives = 3




# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

# read spritesheet
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() 

# heart image
heart_img = spritesheet.subsurface(pygame.Rect(1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (32, 29))


# ball image
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) 
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64)) 
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) 

# paddle image
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

def load_brick(x, y):
    img = pygame.Surface((384,128), pygame.SRCALPHA)
    img.blit(spritesheet, (0,0), (x,y,384,128))
    return pygame.transform.scale(img, (BRICK_WIDTH, BRICK_HEIGHT))

brick_full = {
    "blue":       load_brick(772,390),
    "lightgreen": load_brick(0,130),
    "purple":     load_brick(0,390),
    "red":        load_brick(772,260),
    "orange":     load_brick(772,0),
    "lightblue":  load_brick(386,650),
    "yellow":     load_brick(386,390),
    "green":      load_brick(386,130),
    "grey":       load_brick(772,520),
    "brown":      load_brick(386,780)
}

brick_cracked = {
    "blue":       load_brick(0,0),
    "lightgreen": load_brick(0,260),
    "purple":     load_brick(0,520),
    "red":        load_brick(772,130),
    "orange":     load_brick(772,650),
    "lightblue":  load_brick(386,520),
    "yellow":     load_brick(386,260),
    "green":      load_brick(386,0),
    "grey":       load_brick(0,650),
    "brown":      load_brick(0,780)
}


# --- Sprite loading helpers and dictionaries (no old brick variables needed) ---
# All sprites are loaded in brick_full and brick_cracked dictionaries above

print('mygame is running')
running = True
reset_game()  # reset game state at the start
while running:
    # EVENTS
    for event in pygame.event.get(): # read all events
        if event.type == pygame.QUIT: # GUI is closed 
            running = False # end programm
        if game_status == "naam_invoer" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.key == pygame.K_RETURN and player_name:
                game_status = "uitleg"
            elif len(player_name) < 2 and event.unicode.isprintable():
                player_name += event.unicode
        elif game_status == "uitleg" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_status = "spelen"
        elif game_status in ("gewonnen", "verloren") and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                game_status = "uitleg"

    keys = pygame.key.get_pressed() # read which keys are down
    if game_status == "naam_invoer":
       screen.fill("black")

       title = font.render("Vul je initialen in:", True, "white")
       name_text = font.render(player_name if player_name else "_", True, "green")
       hint = font.render("ENTER om verder te gaan | BACKSPACE om te wissen", True, "green")

       screen.blit(title, ((SCREEN_WIDTH - title.get_width()) / 2, 220))
       screen.blit(name_text, ((SCREEN_WIDTH - name_text.get_width()) / 2, 300))
       screen.blit(hint, ((SCREEN_WIDTH - hint.get_width()) / 2, 360))
       
       pygame.display.flip()
       fps_clock.tick(FPS)
       continue
    # UITLEG SCHERM
    if game_status == "uitleg":
       screen.fill("black")

       title = font.render("BREAKOUT", True, "white")
       makers = font.render("Gemaakt door Thomas en Abel", True, "grey")
       uitleg1 = font.render("Beweeg met [A][D] of [J][L]", True, "green")
       uitleg2 = font.render("Druk op [SPATIE] om te starten", True, "green")

       screen.blit(title, ((SCREEN_WIDTH - title.get_width()) / 2, 360))
       screen.blit(makers, ((SCREEN_WIDTH - makers.get_width()) / 2, 100))
       screen.blit(uitleg1, ((SCREEN_WIDTH - uitleg1.get_width()) / 2, 540))
       screen.blit(uitleg2, ((SCREEN_WIDTH - uitleg2.get_width()) / 2, 580))
       
       if keys[pygame.K_SPACE]:
          game_status = "spelen"
       
       pygame.display.flip()
       fps_clock.tick(FPS)
       continue

    if game_status == "spelen":

      # move ball
      if ball_locked:
         # Bal ligt op paddle
         ball_x = paddle_x + PADDLE_WIDTH/2 - BALL_WIDTH/2
         ball_y = paddle_y - BALL_HEIGHT
      else:
         # Normale beweging
         ball_x += ball_speed_x
         ball_y += ball_speed_y  

      if ball_x < 0:
        ball_speed_x = abs(ball_speed_x)
      if ball_x + BALL_WIDTH > SCREEN_WIDTH:
        ball_speed_x = abs(ball_speed_x) * -1 
      
      if ball_y < 0:
        ball_speed_y = abs(ball_speed_y)

      # move paddle
      moved = False

      if keys[pygame.K_l] or keys[pygame.K_d]:
         paddle_x += 10
         moved = True

      if keys[pygame.K_j] or keys[pygame.K_a]:
         paddle_x -= 10
         moved = True

      # Bal loslaten zodra speler beweegt
      if ball_locked and moved:
         ball_locked = False
         ball_speed_y = -abs(ball_speed_y)


      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle_x < 0:
        paddle_x = 0

      # collision dingen
      rechterkant_bal = ball_x + BALL_WIDTH
      linkerkant_bal = ball_x
      bovenkant_bal = ball_y
      onderkant_bal = ball_y + BALL_HEIGHT
      
      rechterkant_paddle = paddle_x + PADDLE_WIDTH
      linkerkant_paddle = paddle_x
      bovenkant_paddle = paddle_y
      onderkant_paddle = paddle_y + PADDLE_HEIGHT
      
      #ball met paddle collisions
      if (rechterkant_bal > linkerkant_paddle and
        linkerkant_bal < rechterkant_paddle and
        onderkant_bal > bovenkant_paddle and
        bovenkant_bal < onderkant_paddle):
        
        midden_bal = ball_x + BALL_WIDTH / 2
        midden_paddle = paddle_x + PADDLE_WIDTH / 2
        afstand = midden_bal - midden_paddle
        ball_speed_x = afstand / 8
        ball_speed_y = -abs(ball_speed_y)
        ball_y = paddle_y - BALL_HEIGHT

      # ball met brick collisions
      for i in range(len(bricks_x)) :
        rechterkant_brick = bricks_x[i] + BRICK_WIDTH
        linkerkant_brick = bricks_x[i]
        bovenkant_brick = bricks_y[i]
        onderkant_brick = bricks_y[i] + BRICK_HEIGHT

        if (rechterkant_bal > linkerkant_brick and
          linkerkant_bal < rechterkant_brick and
          onderkant_bal > bovenkant_brick and
          bovenkant_bal < onderkant_brick):
            
            print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
            if ball_speed_y > 0 and bovenkant_bal < bovenkant_brick:
              ball_speed_y = abs(ball_speed_y) * -1
            elif ball_speed_y < 0 and (ball_y + BALL_HEIGHT) > onderkant_brick:
              ball_speed_y = abs(ball_speed_y)
            elif ball_speed_x > 0 and ball_x < linkerkant_brick:
              ball_speed_x = abs(ball_speed_x) * -1
            elif ball_speed_x < 0 and (ball_x + BALL_WIDTH) > rechterkant_brick:
              ball_speed_x = abs(ball_speed_x)
            current_time = time.time()
            if current_time - last_hit_time <= 0.8:
               combo += 1
            else:
               combo = 1
            last_hit_time = current_time

            if combo >= 10:
               multiplier = 5
            elif combo >= 6:
               multiplier = 3
            elif combo >= 3:
               multiplier = 2
            else:
               multiplier = 1

            score += combo * 20
            score += 100 * multiplier
            score += int(abs(ball_speed_x) + abs(ball_speed_y)) * 2

            bricks_hp[i] -= 1
            if bricks_hp[i] == 0:
              start_brick_effect(bricks_x[i], bricks_y[i], bricks_color[i])
              bricks_x.pop(i)
              bricks_y.pop(i)
              bricks_hp.pop(i)
              bricks_color.pop(i)


            break

      # gewonnen en verloren via game_status
      if len(bricks_x) == 0 :
        game_status = "gewonnen"

      if ball_y > SCREEN_HEIGHT:
         lives -= 1

         if lives > 0:
            ball_x = paddle_x + PADDLE_WIDTH/2 - BALL_WIDTH/2
            ball_y = paddle_y - BALL_HEIGHT
            ball_speed_x = 6
            ball_speed_y = -10
            ball_locked = True
         else:
            game_status = "verloren"


      # tekenen tijdens spelen
      screen.fill('black') 
      screen.blit(ball_img, (ball_x, ball_y))
      screen.blit(paddle_img, (paddle_x, paddle_y))
      score_text = font.render(f"SCORE: {score}", True, "white")
      screen.blit(score_text, (20, 20))
      # Levens tekenen met hartjes
      for i in range(lives):
         screen.blit(heart_img, (20 + i * 40, 60))
      for i in range(len(bricks_x)):
        color = bricks_color[i]
        if bricks_hp[i] == 2:
          screen.blit(brick_full[color], (bricks_x[i], bricks_y[i]))
        elif bricks_hp[i] == 1:
          screen.blit(brick_cracked[color], (bricks_x[i], bricks_y[i]))

      # --- ANIMATIES VAN VERDWENEN BRICKS ---
      for effect in brick_effects[:]:
          effect["y"] += effect["vy"]
          effect["alpha"] -= 10

          img = brick_full[effect["color"]].copy()
          img.set_alpha(effect["alpha"])

          screen.blit(img, (effect["x"], effect["y"]))

          if effect["alpha"] <= 0:
              brick_effects.remove(effect)


      
      pygame.display.flip()
      fps_clock.tick(FPS)
      continue

    if game_status == "gewonnen":
      if not score_saved:
        save_highscore(player_name or "Anon", score)
        score_saved = True

      screen.fill("black")
      msg = font.render("Level uitgespeeld!", True, "green")
      score_msg = font.render(f"Score: {score}", True, "white")
      screen.blit(msg, ((SCREEN_WIDTH - msg.get_width()) / 2, 100))
      screen.blit(score_msg, ((SCREEN_WIDTH - score_msg.get_width()) / 2, 160))

      scores = load_highscores()
      y = 240
      for entry in scores[:10]:
         line = font.render(f"{entry['name']} - {entry['score']}", True, "white")
         screen.blit(line, (530, y))
         y += 30

      restart = font.render("Druk op [R] om opnieuw te spelen", True, "white")
      screen.blit(restart, ((SCREEN_WIDTH - restart.get_width()) / 2, 600))

      pygame.display.flip()
      fps_clock.tick(FPS)
      continue
    
    if game_status == "verloren":
      if not score_saved:
        save_highscore(player_name or "Anon", score)
        score_saved = True

      screen.fill("black")
      msg = font.render("You lost!", True, "red")
      score_msg = font.render(f"Score: {score}", True, "white")
      screen.blit(msg, ((SCREEN_WIDTH - msg.get_width()) / 2, 100))
      screen.blit(score_msg, ((SCREEN_WIDTH - score_msg.get_width()) / 2, 160))

      scores = load_highscores()
      y = 240
      for entry in scores[:10]:
         line = font.render(f"{entry['name']} - {entry['score']}", True, "white")
         screen.blit(line, (530, y))
         y += 30

      restart = font.render("Druk op [R] om opnieuw te spelen", True, "white")
      screen.blit(restart, ((SCREEN_WIDTH - restart.get_width()) / 2, 600))

      pygame.display.flip()
      fps_clock.tick(FPS)
      continue

print('mygame stopt running')
