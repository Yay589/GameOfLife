def run(self):
    speedRunning = 0.5 * \
        (1 - (int(input("Input the speed running game that you want between 1% and 100% : "))/100))

    Nourriture_group = pygame.sprite.Group()
    bob_group = pygame.sprite.Group()

    for bob in range(5):
        new_bob = BOB(random.randrange(0, GRID_WIDTH) * GRID_CELL_SIZE+GRID_CELL_SIZE/2,
                      random.randrange(0, GRID_HEIGHT) * GRID_CELL_SIZE+GRID_CELL_SIZE/2)
        bob_group.add(new_bob)

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 2000)

    while True:
        time.sleep(speedRunning)
        [...]
