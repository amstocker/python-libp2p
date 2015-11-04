"""
Implementation of Reactor using asyncio.
"""
import asyncio

from .base_reactor import BaseReactor


class AsyncIOReactor(BaseReactor):
    
    def __init__(self, 
