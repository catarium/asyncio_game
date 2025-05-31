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
        self.linux_pressed_keys = []

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
        Starts checking if the keys are pressed by checking list that is updated by linux_key_listener. If so, calls or awaits handler function.
        Awaits sleep after every check.
        """
        while True:
            for k in self.handlers:
                data = self.handlers[k]
                if k in self.linux_pressed_keys:
                    if inspect.iscoroutinefunction(self.handlers[k][0]):
                        await data[0](*data[1])
                    else:
                        data[0](*data[1])
                    await asyncio.sleep(0.01)
            await asyncio.sleep(0.04)

    async def linux_key_listener(self):
        """
        Handles key press and release events: if key is pressed it's name gets added to linux_pressed_keys list if released get's removed. The list is used by linux_listener
        """
        with pynput.keyboard.Events() as events:
            while True:
                event = events.get(0.01)
                if not event:
                    pass
                elif isinstance(event, pynput.keyboard.Events.Press) and (event.key not in self.linux_pressed_keys):
                    if isinstance(event.key, pynput.keyboard.Key):
                        self.linux_pressed_keys.append(event.key.name)
                    self.linux_pressed_keys.append(event.key)
                elif isinstance(event, pynput.keyboard.Events.Release) and event.key in self.linux_pressed_keys:
                    if isinstance(event.key, pynput.keyboard.Key):
                        self.linux_pressed_keys.remove(event.key.name)
                    self.linux_pressed_keys.remove(event.key)
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
        await asyncio.gather(self.linux_listener(), self.linux_key_listener())
        
