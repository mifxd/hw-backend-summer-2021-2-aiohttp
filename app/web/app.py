from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)

from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.admin.models import Admin
from app.store import Store, setup_store
from app.store.database.database import Database
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


class Application(AiohttpApplication):
    config: Config | None = None
    store: Store | None = None
    database: Database = Database()


class Request(AiohttpRequest):
    admin: Admin | None = None

    @property
    def app(self) -> Application:
        return super().app


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

def setup_app(config_path: str) -> Application:
    app = Application()
    setup_logging(app)
    setup_config(app, config_path)

    session_cfg = app.config.session
    if session_cfg is not None and hasattr(session_cfg, 'key'):
        raw_key = session_cfg.key
    else:
        raw_key = "key_to_generate"

    try:
        session_key = raw_key.encode().ljust(32)[:32]
        setup_session(app, EncryptedCookieStorage(session_key))
    except Exception:
        setup_session(app, EncryptedCookieStorage(b"a" * 32))

    setup_middlewares(app)
    setup_routes(app)
    setup_store(app)

    return app