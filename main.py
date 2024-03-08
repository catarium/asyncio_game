import asyncio
from objects.player_object import PlayerObject
from screen.screen import Screen
from user_input.keyboard_input_handler import KeyboardInputHandler


# initializing a screen, input handler and player
screen = Screen(21, 21)
keyboard_input_handler = KeyboardInputHandler()
player = PlayerObject(screen, 10, 10)

# binding key pressing events
keyboard_input_handler.add_handler('up', player.move_up, [])
keyboard_input_handler.add_handler('down', player.move_down, [])
keyboard_input_handler.add_handler('right', player.move_right, [])
keyboard_input_handler.add_handler('left', player.move_left, [])


async def main():
    await asyncio.gather(
        screen.start_show(),
        keyboard_input_handler.start_listening()
    )


if __name__ == '__main__':
    asyncio.run(main())
