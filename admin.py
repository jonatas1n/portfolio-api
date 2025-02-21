from fastapi import FastAPI
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import Session
from starlette.requests import Request
from passlib.context import CryptContext

from database.db import engine, SessionLocal

from skills.admin import SkillAdmin
from experiences.admin import ExperienceAdmin
from projects.admin import ProjectAdmin
from users.admin import UserAdmin

from users.models import Users

admin = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        with SessionLocal() as session:
            user = self.get_user_by_email(session, email)
            if not user or not pwd_context.verify(password, user.password_hash):
                return False

        request.session.update({"token": email})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("token"))

    def get_user_by_email(self, session: Session, email: str):
        return session.query(Users).filter(Users.email == email).first()


authentication_backend = AdminAuth(secret_key="admin")


def init_all_admins(app: FastAPI):
    global admin
    if admin is None:
        admin = Admin(app, engine, authentication_backend=authentication_backend)

    admin.add_view(UserAdmin)
    admin.add_view(SkillAdmin)
    admin.add_view(ExperienceAdmin)
    admin.add_view(ProjectAdmin)
