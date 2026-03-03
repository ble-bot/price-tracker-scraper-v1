from app.database.models import UserSettings
from sqlalchemy import select


def check_price_drop(session, user, old_price, new_price):
    if old_price == 0:
        return None

    settings = session.execute(
        select(UserSettings).where(UserSettings.user_id == user.id)
    ).scalar_one_or_none()

    if not settings:
        return None

    drop_percentage = (old_price - new_price) / old_price

    if drop_percentage >= settings.alert_threshold:
        return {
            "user_id": user.id,
            "drop_percebtage": drop_percentage,
            "old_price": old_price,
            "new_price": new_price,
        }

    return None
