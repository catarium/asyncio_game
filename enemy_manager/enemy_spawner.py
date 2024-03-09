import asyncio
from random import shuffle, randrange


async def enemy_spawner(enemies, screen):
    """
    constantly spawns enemies
    :param enemies: list of enemies which get random.shuffled every time
    :param screen: screen
    """
    while True:
        shuffle(enemies)
        for enemy_class in enemies:
            cords = (randrange(1, screen.width - 1), 1)
            enemy = enemy_class(screen, *cords)
            asyncio.create_task(enemy.start_acting())
            screen.set_obj(cords[0], cords[1], enemy)
            await asyncio.sleep(0.02)
        await asyncio.sleep(10)
