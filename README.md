# Market Scraper - Monitoreo de Precios 🚀

Este es un proyecto de Web Scraping profesional diseñado para extraer, monitorear y alertar sobre cambios de precios en productos. Actualmente configurado para el sitio de prueba [Books to Scrape](https://books.toscrape.com/).

## 📋 Descripción
Market Scraper es una herramienta automatizada que recorre categorías de productos, extrae su información actual (nombre, precio, disponibilidad, rating) y la almacena en una base de datos relacional. El sistema está diseñado para detectar cambios de precio entre ejecuciones y disparar alertas cuando se detectan ofertas.

## ✨ Características Principales
- **Scraping Recursivo:** Navega por múltiples categorías y paginación de forma automática.
- **Base de Datos Relacional:** Uso de SQLAlchemy para gestionar Productos, Categorías, Tiendas e Historial de Precios.
- **Lógica de Upsert:** Evita duplicados y mantiene un historial cronológico de cambios de precio.
- **Sistema de Alertas:** Calcula el porcentaje de caída de precio y detecta oportunidades de compra.
- **Arquitectura Limpia:** Separación clara entre servicios, modelos de datos y lógica de scraping.

## 🛠️ Tecnologías Usadas
- **Python 3.x**
- **BeautifulSoup4:** Para el parseo de HTML.
- **Requests:** Para la gestión de peticiones HTTP.
- **SQLAlchemy:** ORM para la gestión de la base de datos SQLite.
- **SQLite:** Base de datos ligera y persistente.

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/ble-bot/price-tracker-scraper-v1.git
cd price-tracker-scraper-v1
```

### 2. Instalar dependencias
Se recomienda usar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar el proyecto
Para iniciar el proceso de scraping y actualización de la base de datos:
```bash
python -m app.main
```

## 📂 Estructura del Proyecto
```text
market_scraper/
├── app/
│   ├── alerts/          # Lógica de detección de ofertas
│   ├── crud/            # Operaciones básicas de base de datos
│   ├── database/        # Modelos y configuración de SQLAlchemy
│   ├── services/        # Lógica de scraping y procesamiento de productos
│   └── main.py          # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación
```

---
Desarrollado como proyecto de portafolio para demostrar habilidades en Python, Web Scraping y Modelado de Datos.
