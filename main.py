import asyncio

from enemy_manager.enemy_spawner import enemy_spawner
from objects.enemy_object import EnemyObject
from objects.player_object import PlayerObject
from objects.self_guided_missile_object import SelfGuidedMissileObject
from screen.screen import Screen
from user_input.keyboard_input_handler import KeyboardInputHandler


# initializing a screen, input handler and player
screen = Screen(21, 21)
keyboard_input_handler = KeyboardInputHandler()
player = PlayerObject(screen, 10, 18)

# binding key pressing events
keyboard_input_handler.add_handler('up', player.move_up, [])
keyboard_input_handler.add_handler('down', player.move_down, [])
keyboard_input_handler.add_handler('right', player.move_right, [])
keyboard_input_handler.add_handler('left', player.move_left, [])
keyboard_input_handler.add_handler('space', player.shoot, [])


async def main():
    await asyncio.gather(
        screen.start_show(player),
        keyboard_input_handler.start_listening(),
        enemy_spawner([(EnemyObject, []), (EnemyObject, []), (SelfGuidedMissileObject, (player,))], screen)
    )


if __name__ == '__main__':
    asyncio.run(main())
