from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base


class Store(Base):
    __tablename__ = "store"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="store")


class Product(Base):
    __tablename__ = "product"

    __table_args__ = (UniqueConstraint("name", "store_id"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)

    store_id = Column(Integer, ForeignKey("store.id", ondelete="CASCADE"))

    store = relationship("Store", back_populates="products")

    price_history = relationship("PriceHistory", back_populates="product")
    categories = relationship(
        "Category", secondary="product_category", back_populates="products"
    )


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    products = relationship(
        "Product", secondary="product_category", back_populates="categories"
    )


class ProductCategory(Base):
    __tablename__ = "product_category"

    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True
    )
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), primary_key=True
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False)

    settings = relationship("UserSettings", back_populates="user", uselist=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    alert_threshold = Column(Float, default=0.10)

    user = relationship("User", back_populates="settings")
