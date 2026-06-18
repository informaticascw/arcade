bricks_x = [100, 200, 300, 400]
print(bricks_x)
#bricks_x_copy = bricks_x
bricks_x_copy =[]
for i in range(0,len(bricks_x)):
    bricks_x_copy.append(bricks_x[i])
print(bricks_x_copy)
bricks_x.pop(1)
print(bricks_x_copy)
print(bricks_x)

# voorbeeld met lijsten kopiëren
# handig voor restart knop met game_init(): functie