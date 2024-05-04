from .borb import *
from .dalle import *
from .moderation import *
from .uptime import *

cogs = [Borb, Uptime, Moderation, Dalle]

__all__ = [Borb, Uptime, Moderation, cogs]