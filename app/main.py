from app.database.connection import engine, SessionLocal
from app.database.models import Base, Store, User, UserSettings
from app.services.scraper_service import get_categories, scrape_category
from app.services.product_service import upsert_product
from sqlalchemy import select

def create_tables():
    """
    Crea todas las tablas definidas en los modelos si aún no existen.
    Usa la conexión definida en database/connection.py
    """
    Base.metadata.create_all(engine)

def get_or_create_user(session, email: str):
    """
    Busca un usuario por su email. Si no existe, lo crea junto
    con una configuración de alertas por defecto.
    """
    user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        user = User(email=email)
        session.add(user)
        session.flush() # Para obtener el ID del usuario antes del commit

        # Por defecto, alertamos si el precio baja un 10% (0.10)
        settings = UserSettings(user_id=user.id, alert_threshold=0.10)
        session.add(settings)

    return user

def get_or_create_store(session, name: str):
    """
    Busca una tienda por su nombre. Si no existe, la crea.
    """
    store = session.execute(
        select(Store).where(Store.name == name)
    ).scalar_one_or_none()

    if not store:
        store = Store(name=name)
        session.add(store)
        session.flush()

    return store

def run_books_scraper():
    """
    Función principal que ejecuta el flujo completo:
    1. Asegura que la DB existe.
    2. Configura usuario y tienda.
    3. Scrapea el sitio web 'Books to Scrape'.
    4. Guarda los datos de forma inteligente (upsert).
    """
    print("🚀 Iniciando Market Scraper - Sistema de Monitoreo de Precios")
    
    # Aseguramos que las tablas existan antes de empezar
    create_tables()
    
    session = SessionLocal()
    try:
        # 1. Preparación del entorno
        user = get_or_create_user(session, "admin@market.com")
        store = get_or_create_store(session, "BooksToScrape")

        # 2. Inicio del Scraping
        print("🔍 Extrayendo categorías...")
        categories = get_categories()

        # 3. Iteración sobre categorías y libros
        # Nota: En un entorno real, esto podría ser una tarea programada
        for category in categories:
            print(f"📂 Procesando categoría: {category['name']}")
            books = scrape_category(category)

            for book in books:
                # 4. Guardado/Actualización de cada libro
                upsert_product(
                    session=session,
                    store=store,
                    user=user,
                    name=book["name"],
                    price=book["price"],
                    category_name=book["category"]
                )
            
            # Guardamos cambios por cada categoría para no sobrecargar la memoria
            session.commit()
            print(f"   ✅ Se han procesado {len(books)} libros de esta categoría.")

        print("\n✨ ¡Proceso completado con éxito!")
        print("📊 Los datos han sido guardados en 'market.db'.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error inesperado durante la ejecución: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    # Ejecutamos el scraper si este archivo se corre directamente
    run_books_scraper()
