import asyncio
import inspect
import keyboard
import typing
from typing import Union


class KeyboardInputHandler:
    """
    Asynchronously handles keyboard events
    """
    def __init__(self, handlers: dict = {}):
        self.handlers = handlers

    def add_handler(self, key: Union[str, keyboard.KeyboardEvent],
                    handler: Union[typing.Callable, typing.Awaitable],
                    args: typing.Union[tuple, list]) -> None:
        """
        Adds new keyboard event handler
        :param key: keyboard key, either string or keyboard library Event
        :param handler: function that calls or awaits when the key is pressed
        :param args: handler's arguments
        """
        self.handlers[key] = (handler, args)

    async def start_listening(self) -> None:
        """
        Starts checking if the keys are pressed. If so, calls or awaits handler function.
        Awaits sleep after every check.
        """
        while True:
            for k in self.handlers:
                data = self.handlers[k]
                if keyboard.is_pressed(k):
                    if inspect.iscoroutinefunction(self.handlers[k][0]):
                        await data[0](*data[1])
                    else:
                        data[0](*data[1])
                    await asyncio.sleep(0.01)
            await asyncio.sleep(0.04)
