import typing

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor
from hashlib import sha256

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        # TODO: создать админа по данным в config.yml здесь
        admin_cfg = app.config.admin
        h_password = sha256(admin_cfg.password.encode()).hexdigest()

        admin = Admin(id=1, email=admin_cfg.email, password=h_password)

        app.database.admins.append(admin)

    async def get_by_email(self, email: str) -> Admin | None:
        for admin in self.app.database.admins:
            if admin.email == email:
                return admin

        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        raise NotImplementedError
