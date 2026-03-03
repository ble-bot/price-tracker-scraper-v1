from sqlalchemy import select
from app.database.models import Store


def get_store_by_name(session, name: str):
    return session.execute(select(Store).where(Store.name == name)).scalar_one_or_none()


def create_stire(session, name: str):
    store = Store(name=name)
    session.add(store)
    session.flush()
    return store
