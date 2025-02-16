import os
from typing import Type, TypeVar, Optional

T = TypeVar('T', str, int, bool)


def get_config(
        env_var: str,
        required: bool = True,
        default_val: Optional[T] = None,
        cast_var: Type[T] = str) -> T:
    val = os.environ.get(env_var, default_val)
    if not val and required:
        raise AttributeError(f"Environment variable {env_var} not set!")
    return cast_var(val)
