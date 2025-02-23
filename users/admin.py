from sqladmin import ModelView
from starlette.requests import Request

from users.models import Users


class UserAdmin(ModelView, model=Users):
    name = "User"
    name_plural = "Users"
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
