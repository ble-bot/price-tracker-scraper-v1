from sqlalchemy import select
from app.database.models import Product, PriceHistory, Category
from app.alerts.alert_service import check_price_drop

def upsert_product(session, store, user, name, price, category_name=None):
    """
    Inserta o actualiza un producto en la base de datos.
    Si el producto ya existe, verifica si el precio ha cambiado y guarda el historial.
    Si el precio baja significativamente, dispara una alerta.
    
    Args:
        session: La sesión activa de SQLAlchemy.
        store: El objeto Store al que pertenece el producto.
        user: El objeto User para el que se verifican las alertas.
        name: Nombre del producto/libro.
        price: Precio actual detectado por el scraper.
        category_name: Nombre de la categoría a la que pertenece.
    """
    # 1. Buscar si el producto ya existe para esta tienda específica
    # Esto evita duplicados si el mismo nombre existe en tiendas distintas
    existing_product = session.execute(
        select(Product).where(Product.name == name, Product.store_id == store.id)
    ).scalar_one_or_none()

    # 2. Manejo de la categoría
    # Si el scraper nos da una categoría, la buscamos o creamos en la DB
    category = None
    if category_name:
        category = session.execute(
            select(Category).where(Category.name == category_name)
        ).scalar_one_or_none()
        
        if not category:
            category = Category(name=category_name)
            session.add(category)
            session.flush() # Genera el ID para poder relacionarlo luego

    if existing_product:
        # Caso: El producto ya existe. Verificamos si el precio cambió.
        old_price = existing_product.current_price

        if old_price != price:
            # Si el precio bajó, el alert_service decidirá si es una oferta relevante
            alert = check_price_drop(session, user, old_price, price)
            if alert:
                # Aquí podrías integrar un envío de email o Telegram en el futuro
                print(f"🔔 ¡OFERTA DETECTADA!: '{name}' bajó de {old_price} a {price}")

            # Actualizamos el precio actual del producto
            existing_product.current_price = price

            # Guardamos el cambio en la tabla de historial (PriceHistory)
            # Esto permite graficar la evolución del precio en el tiempo
            history = PriceHistory(product_id=existing_product.id, price=price)
            session.add(history)

        return existing_product

    else:
        # Caso: El producto es nuevo en nuestro sistema
        new_product = Product(name=name, current_price=price, store_id=store.id)
        
        # Establecemos la relación Muchos-a-Muchos con la categoría
        if category:
            new_product.categories.append(category)

        session.add(new_product)
        session.flush() # Necesitamos el ID del producto recién creado

        # Creamos su primer registro de precio en el historial
        history = PriceHistory(product_id=new_product.id, price=price)
        session.add(history)

        return new_product
