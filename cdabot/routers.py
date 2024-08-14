from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message

menu_router = Router()
func_router = Router()

class msgEq(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
    
    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text