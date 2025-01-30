import asyncio
import inspect
import typing
import pynput
from typing import Union
import platform


class KeyboardInputHandler:
    """
    Asynchronously handles keyboard events
    """
    def __init__(self, handlers: dict = {}):
        self.handlers = handlers

    def add_handler(self, key: str,
                    handler: Union[typing.Callable, typing.Awaitable],
                    args: typing.Union[tuple, list]) -> None:
        """
        Adds new keyboard event handler
        :param key: keyboard key, either string or keyboard library Event
        :param handler: function that calls or awaits when the key is pressed
        :param args: handler's arguments
        """
        self.handlers[key] = (handler, args)

    async def linux_listener(self):
        """
        Starts checking if the keys are pressed. If so, calls or awaits handler function.
        Awaits sleep after every check.
        """
        with pynput.keyboard.Events() as events:
            while True:
                event = events.get(0.01)
                for k in self.handlers:
                    data = self.handlers[k]
                    if event and k in str(event.key) and isinstance(event, pynput.keyboard.Events.Press):
                        if inspect.iscoroutinefunction(data[0]):
                            await data[0](*data[1])
                        else:
                            data[0](*data[1])
                    await asyncio.sleep(0.01)

    async def windows_listener(self):
        """
        Starts checking if the keys are pressed. If so, calls or awaits handler function.
        Awaits sleep after every check.
        """
        import keyboard
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


    async def start_listening(self) -> None:
        """
        Runs a listener according to os
        """

        # Using special version of listener for winodws bc keyboard module works better, but requires root on linux
        if platform.system == 'Windows':
            await self.windows_listener()
            return
        await self.linux_listener()
        
