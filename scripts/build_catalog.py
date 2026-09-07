#!/usr/bin/env python3
"""Build the public catalog from researched candidates and editorial curation."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data" / "candidate-products.json"
OUTPUT = ROOT / "data" / "products.json"


CURATION = [
    ("https://meli.la/1UcWwMN", "Audífonos Sony WH-CH520", "Audio", 4.9, 59576, "+50 mil vendidos", "Tienda oficial Sony", True, "Tienda oficial", "Hasta 50 horas de batería, conexión multipunto y una reputación sobresaliente para uso diario."),
    ("https://meli.la/28hDkWy", "Audífonos Soundcore P30i con cancelación de ruido", "Audio", 4.9, 22664, "+1,000 vendidos", "Tienda oficial Soundcore", True, "Precio destacado", "Cancelación de ruido, bajos potentes y hasta 45 horas de reproducción a un precio accesible."),
    ("https://meli.la/1GKjVJE", "Samsung Galaxy Fit3 AMOLED", "Wearables", 4.9, 44745, "+10 mil vendidos", "Tienda oficial Samsung", True, "Precio destacado", "Pantalla AMOLED de 1.6 pulgadas, formato ligero y respaldo de la tienda oficial."),
    ("https://meli.la/2vBpq4U", "Audífonos JBL Tune 720BT", "Audio", 4.9, 29034, "+10 mil vendidos", "JBL", True, "Mejor precio visible", "Opción over-ear Bluetooth muy bien valorada y ofrecida al menor precio visible del mismo producto."),
    ("https://meli.la/2zo4yXE", "Cámara TP-Link Tapo TC70 360°", "Hogar inteligente", 4.9, 3713, "+5 mil vendidos", "TP-Link Tapo", False, "Mejor precio visible", "Video FHD, giro 360°, visión nocturna, detección de movimiento y audio bidireccional."),
    ("https://meli.la/2WNBEHb", "Roku Streaming Stick Plus 4K", "Streaming", 4.9, 6939, "+10 mil vendidos", "Nuvitu Electronics", True, "Mejor precio visible", "Convierte una pantalla compatible en centro de streaming 4K e incluye control por voz."),
    ("https://meli.la/2GC8Qag", "Amazon Fire TV Stick 4K", "Streaming", 4.9, 15133, "+10 mil vendidos", "Electronics México", True, "Mejor precio visible", "Reproducción 4K en un formato compacto con control remoto, adaptador, cable y HDMI incluidos."),
    ("https://meli.la/1ansJko", "Mouse gaming Logitech G203", "Gaming", 4.9, 55723, "+10 mil vendidos", "Logitech", True, "Mejor precio visible", "Un mouse de entrada confiable para jugar o trabajar, con decenas de miles de valoraciones positivas."),
    ("https://meli.la/19sGzBf", "Mouse inalámbrico Logitech M170", "Accesorios", 4.9, 43592, "+10 mil vendidos", "Tienda oficial Logitech", True, "Mejor precio visible", "Accesorio sencillo, portátil y económico, vendido por la tienda oficial con reputación comprobada."),
    ("https://meli.la/1KAq2m7", "Huawei Band 11", "Wearables", 4.9, 6024, "+10 mil vendidos", "Tienda oficial Huawei", True, "Mejor precio visible", "Pantalla de 1.62 pulgadas y funciones de sueño y bienestar con respaldo de la tienda oficial."),
    ("https://meli.la/29FaBcN", "Samsung Galaxy Tab A11 8.7 pulgadas", "Tablets", 4.9, 2469, "+10 mil vendidos", "GC Móvil", True, "Mejor precio visible", "Tablet compacta con 64 GB, 4 GB de RAM y Android 15 para entretenimiento y tareas ligeras."),
    ("https://meli.la/2JQKzNL", "SSD Kingston A400 SATA de 960 GB", "Almacenamiento", 4.9, 14776, "+10 mil vendidos", "Kingston", True, "Mejor precio visible", "Una mejora de capacidad útil para computadoras compatibles con unidades SATA de 2.5 pulgadas."),
    ("https://meli.la/247NpFP", "Super Mario Odyssey para Nintendo Switch", "Gaming", 4.9, 9858, "+50 mil vendidos", "Game Center Inc", True, "Mejor precio visible", "Uno de los títulos mejor valorados de Switch, con amplio respaldo de compradores."),
    ("https://meli.la/2QA94iZ", "Brazo para monitor North Bayou NB F80", "Accesorios", 4.9, 38296, "+10 mil vendidos", "North Bayou", True, "Mejor precio visible", "Libera espacio y mejora la posición de monitores compatibles de 17 a 30 pulgadas."),
    ("https://meli.la/2gL5jad", "Laptop HP 255R G10 Ryzen 5", "Cómputo", 4.8, 93, "+1,000 vendidos", "Coimprit", True, "Mejor precio visible", "Ryzen 5 7535U, 8 GB DDR5, SSD de 512 GB y pantalla Full HD para estudio y trabajo."),
    ("https://meli.la/1otUMb9", "Laptop ASUS Vivobook 16, 16 GB y 1 TB SSD", "Cómputo", 5.0, 112, "+1,000 vendidos", "Tienda oficial ASUS", True, "Tienda oficial", "Configuración amplia de 16 GB y 1 TB SSD, con mochila y mouse incluidos por la tienda oficial."),
    ("https://meli.la/1PZbGU9", "Bocina portátil JBL Charge 6", "Audio", 4.9, 22094, "+10 mil vendidos", "JBL", False, "Precio destacado", "Sonido potente, batería para uso prolongado y resistencia al agua en una bocina portátil con amplio respaldo de compradores."),
    ("https://meli.la/2RNmaab", "Teclado mecánico gamer AULA F99 en español", "Gaming", 4.9, 205, "+100 vendidos", "AELION", False, "Precio destacado", "Teclado mecánico compacto con pad numérico, distribución en español latinoamericano, cable removible y retroiluminación RGB."),
    ("https://meli.la/2Ewc9kx", "Router TP-Link Archer AX23 Wi-Fi 6", "Conectividad", 4.8, 650, "+100 vendidos", "Tienda oficial TP-Link", True, "Precio destacado", "Router Wi-Fi 6 de doble banda con cuatro puertos LAN, firewall y control parental para renovar una red compatible."),
    ("https://meli.la/1vYtFiv", "Sistema Wi-Fi 6 Mesh Mercusys Halo H60X, paquete de 3", "Conectividad", 4.8, 968, "+100 vendidos", "Tienda oficial Mercusys", True, "Precio destacado", "Tres nodos Wi-Fi 6 para mejorar cobertura y estabilidad en hogares donde un solo router no alcanza bien."),
    ("https://meli.la/26o3ev1", "Power bank ADATA P20000Q de 20,000 mAh", "Accesorios", 4.8, 242, "+1,000 vendidos", "SVENSKA", False, "Buena reputación", "Batería portátil de gran capacidad con USB-C y varios puertos; útil para viajes y emergencias, aunque su carga rápida depende del uso de los puertos."),
    ("https://meli.la/1GTHdWm", "Cámara exterior Wi-Fi Imou DK7 de 3 MP", "Hogar inteligente", 4.8, 973, "+10 mil vendidos", "Tienda oficial Imou", True, "Precio destacado", "Cámara motorizada para exterior con audio bidireccional, visión nocturna a color, detección inteligente y protección IP66."),
]


REVIEW_SNAPSHOT_DATE = "2026-09-07T00:00:00-05:00"
REVIEW_SNAPSHOTS = {
    "https://meli.la/1UcWwMN": {
        "rating": 4.9, "reviews": 59581,
        "snippets": [
            "Amé el producto, lo recomiendo totalmente.",
            "Están preciosos, no lastiman porque uso lentes y tienen buen sonido.",
        ],
    },
    "https://meli.la/28hDkWy": {
        "rating": 4.9, "reviews": 22664,
        "snippets": [
            "Me sorprendieron bastante; el sonido y los materiales son buenos.",
            "Valió cada centavo.",
        ],
    },
    "https://meli.la/1GKjVJE": {
        "rating": 4.9, "reviews": 44756,
        "snippets": [
            "La pantalla es de calidad y con una imagen perfecta.",
            "La batería dura ocho días.",
        ],
    },
    "https://meli.la/2vBpq4U": {
        "rating": 4.9, "reviews": 29034,
        "snippets": [
            "La calidad de sonido ya era buenísima.",
            "Decidí volver a confiar en la marca.",
        ],
    },
    "https://meli.la/2zo4yXE": {
        "rating": 4.9, "reviews": 3690,
        "snippets": [
            "Su instalación es fácil y es rápida de conectar.",
            "La calidad de imagen es excelente.",
        ],
    },
    "https://meli.la/2WNBEHb": {
        "rating": 4.9, "reviews": 6971,
        "snippets": [
            "Mejoró bastante comparado con la versión anterior.",
            "Solo necesito un control remoto en lugar de dos.",
        ],
    },
    "https://meli.la/2GC8Qag": {
        "rating": 4.9, "reviews": 15411,
        "snippets": [
            "Es compatible con la app Xbox para jugar vía nube.",
            "Este control es más cómodo y práctico.",
        ],
    },
    "https://meli.la/1ansJko": {
        "rating": 4.9, "reviews": 56185,
        "snippets": [
            "El producto es original y la app sí lo reconoce.",
            "Ahora me matan igual, pero con estilo.",
        ],
    },
    "https://meli.la/19sGzBf": {
        "rating": 4.9, "reviews": 43596,
        "snippets": [
            "Es muy cómodo y ergonómico; no cansa la muñeca.",
            "La pila que trae dura muchísimo tiempo.",
        ],
    },
    "https://meli.la/1KAq2m7": {
        "rating": 4.9, "reviews": 6028,
        "snippets": [
            "Pantalla nítida, colores correctos y brillantes.",
            "No puedes contestar llamadas; no tiene bocina ni altavoz.",
        ],
    },
    "https://meli.la/29FaBcN": {
        "rating": 4.9, "reviews": 2469,
        "snippets": [
            "Para uso básico es perfecta.",
            "Es la versión que no tiene para tarjeta SIM.",
        ],
    },
    "https://meli.la/2JQKzNL": {
        "rating": 4.9, "reviews": 14776,
        "snippets": [
            "Tiene un arranque con Windows 10 excelente.",
            "Es un cambio tremendo a comparación del HDD.",
        ],
    },
    "https://meli.la/247NpFP": {
        "rating": 4.9, "reviews": 9860,
        "snippets": [
            "Un juego lleno de detalles, muy bien hecho; vale mucho la pena.",
            "El juego vino en perfecto estado.",
        ],
    },
    "https://meli.la/2QA94iZ": {
        "rating": 4.9, "reviews": 36944,
        "snippets": [
            "Maximiza el espacio en tu escritorio para trabajar y jugar.",
            "Lo compré para un uso diferente y funcionó perfectamente.",
        ],
    },
    "https://meli.la/2gL5jad": {
        "rating": 4.8, "reviews": 93,
        "snippets": [
            "Enciende rápido. Muy útil para las tareas básicas.",
            "Buen equipo, solo se descarga muy rápido.",
        ],
    },
    "https://meli.la/1otUMb9": {
        "rating": 5.0, "reviews": 112,
        "snippets": [
            "Venía tal cual con mochila y mouse.",
            "Es una buena laptop y, aunque no es para juegos, los corre bastante bien.",
        ],
    },
    "https://meli.la/1PZbGU9": {
        "rating": 4.9, "reviews": 22094,
        "snippets": [
            "El sonido es excelente, potente y se conecta con rapidez.",
            "Funciona muy bien al aire libre y la batería tiene buena duración.",
        ],
    },
    "https://meli.la/2RNmaab": {
        "rating": 4.9, "reviews": 205,
        "snippets": [
            "Las teclas se sienten suaves y la calidad de construcción es buena.",
            "El formato compacto conserva el teclado numérico y resulta cómodo.",
        ],
    },
    "https://meli.la/2Ewc9kx": {
        "rating": 4.8, "reviews": 650,
        "snippets": [
            "La red de 5 GHz mantiene buena velocidad y estabilidad.",
            "Es fácil de configurar y permite separar las dos bandas.",
        ],
    },
    "https://meli.la/1vYtFiv": {
        "rating": 4.8, "reviews": 968,
        "snippets": [
            "La configuración es sencilla y la aplicación resulta práctica.",
            "Mejoró la cobertura, aunque la distancia entre nodos sí importa.",
        ],
    },
    "https://meli.la/26o3ev1": {
        "rating": 4.8, "reviews": 242,
        "snippets": [
            "Permite varias cargas del teléfono y es útil para viajar.",
            "Puede cargar varios dispositivos, pero compartir puertos reduce la carga rápida.",
        ],
    },
    "https://meli.la/1GTHdWm": {
        "rating": 4.8, "reviews": 973,
        "snippets": [
            "La imagen es clara de día y de noche, con buena conexión Wi-Fi.",
            "La detección de movimiento y el audio ayudan a vigilar exteriores.",
        ],
    },
}


def main() -> None:
    research = json.loads(RESEARCH.read_text(encoding="utf-8"))
    by_link = {product["affiliate_url"]: product for product in research["products"]}
    products = []
    for entry in CURATION:
        link, title, category, rating, reviews, sold, seller, official, signal, reason = entry
        source = by_link[link]
        review_snapshot = REVIEW_SNAPSHOTS[link]
        discount_match = re.search(r"(\d+)%", source.get("discount_label") or "")
        products.append({
            "id": source["item_id"],
            "catalog_product_id": source["catalog_product_id"],
            "permalink": source["permalink"],
            "title": title,
            "category": category,
            "price": source["price"],
            "previous_price": source.get("previous_price"),
            "currency": source.get("currency") or "MXN",
            "discount": int(discount_match.group(1)) if discount_match else None,
            "rating": review_snapshot["rating"],
            "reviews": review_snapshot["reviews"],
            "sold": sold,
            "seller": seller,
            "official_store": official,
            "price_signal": signal,
            "reason": reason,
            "image": source["image"],
            "affiliate_url": link,
            "available": True,
            "review_snippets": review_snapshot["snippets"],
            "last_price_check": research["generated_at"],
            "last_review_check": REVIEW_SNAPSHOT_DATE,
        })
    output = {
        "schema_version": 2,
        "generated_at": research["generated_at"],
        "source_note": "Precios y disponibilidad se verifican diariamente. Calificaciones, ventas y extractos de opiniones son una referencia editorial observada en Mercado Libre México y pueden cambiar.",
        "products": products,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catálogo público generado con {len(products)} productos.")


if __name__ == "__main__":
    main()
