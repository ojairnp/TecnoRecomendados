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
]


def main() -> None:
    research = json.loads(RESEARCH.read_text(encoding="utf-8"))
    by_link = {product["affiliate_url"]: product for product in research["products"]}
    products = []
    for entry in CURATION:
        link, title, category, rating, reviews, sold, seller, official, signal, reason = entry
        source = by_link[link]
        discount_match = re.search(r"(\d+)%", source.get("discount_label") or "")
        products.append({
            "id": source["item_id"],
            "title": title,
            "category": category,
            "price": source["price"],
            "previous_price": source.get("previous_price"),
            "currency": source.get("currency") or "MXN",
            "discount": int(discount_match.group(1)) if discount_match else None,
            "rating": rating,
            "reviews": reviews,
            "sold": sold,
            "seller": seller,
            "official_store": official,
            "price_signal": signal,
            "reason": reason,
            "image": source["image"],
            "affiliate_url": link,
            "available": True,
        })
    output = {
        "schema_version": 2,
        "generated_at": research["generated_at"],
        "source_note": "Precios, disponibilidad, ventas y opiniones observados en Mercado Libre México; pueden cambiar.",
        "products": products,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Catálogo público generado con {len(products)} productos.")


if __name__ == "__main__":
    main()
