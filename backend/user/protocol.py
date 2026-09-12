from typing import Protocol

from user.types import User


class UserRepository(Protocol):
    def list_all(self) -> list[User]: ...

    def create(self, *, name: str, email: str) -> User: ...
