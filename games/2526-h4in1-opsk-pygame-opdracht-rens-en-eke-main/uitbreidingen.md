# Uitbereidingen 

Wij hebben deze uitbreidingen gemaakt:
UITBREIDING 1:
elif keys[pygame.K_r] : 
     ball_x = SCREEN_WIDTH / 2 
     ball_y = 0
     ball_speed_x = 5
     ball_speed_y = 6
     paddle_x = SCREEN_WIDTH / 2 - (PADDLE_WIDTH / 2)
     game_status_msg = 'Speel met [A] en [D]'
     bricks_x = [96, 192, 288, 96, 192, 288, 96, 192, 288, 96, 192, 288, 892, 988, 1084, 892, 988, 1084, 892, 988, 1084, 892, 988, 1084] 
     bricks_y = [100, 100, 100, 132, 132, 132, 164, 164, 164, 196, 196, 196, 100, 100, 100, 132, 132, 132, 164, 164, 164, 196, 196, 196]    

     <als je op de r klikt op het toetsen bord dan reset de game en dan begin je opnieuw>


UITBREIDING 2: 
 background_img = pygame.image.load('achtergrond.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_img, (0,0))

    <we hebben de achtergrond vervangen met een plaatje>

UITBREIDING 3:
 game_status_msg1 = "Druk op [R] om te resetten"

 game_status_img = font.render(game_status_msg , True, 'yellow')
    screen.blit(game_status_img, (SCREEN_WIDTH / 2 - game_status_img.get_width() / 2, SCREEN_HEIGHT - game_status_img.get_width() / 2))
 game_status_img1 = font.render(game_status_msg1 , True, 'yellow')
    screen.blit(game_status_img1, (SCREEN_WIDTH / 2 - game_status_img1.get_width() / 2, SCREEN_HEIGHT / 2   - game_status_img1.get_width() / 2))

    <de tekst is nu geel en er is ook een tekst voor de reset>

UITBREIDING 4:
bricks_x =[0,0,0,0,0,192,192,192,192,192,96,350,446,542,350,542,350,446,542,350,542,350,542,700,700,700,700,700,850,850,850,850,850,1000,1096,1192,1000,1192,1000,1192,1000,1192,1000,1096,1192]
bricks_y =[100,132,164,196,228,100,132,164,196,228,164,100,100,100,132,132,164,164,164,196,196,228,228,100,132,164,196,228,100,132,164,196,228,100,100,100,132,132,164,164,196,196,228,228,228]   

<Nu staan de blokken zo dat het woord HALLO er staat. Ze staan ook zo als je op de reset knop drukt>

UITBREIDING 5: 
ball_y = SCREEN_HEIGHT - 100 - PADDLE_HEIGHT



<De bal begint nu op de plank zodat het makkelijker is om te beginnen en je begint vanuit onder dus dan wordt het level moeilijker>




 <vul hier je uitbreiding in>
- <vul hier je volgende uitbreiding in>
- enzovoort
