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
    ("https://meli.la/2boUWLq", "Webcam Logitech C920 Full HD", "Videollamadas", 4.9, 1990, "+1,000 vendidos", "Tienda oficial Logitech", True, "Oferta destacada", "Video Full HD a 30 fps, enfoque automático y dos micrófonos para videollamadas, clases y transmisiones."),
    ("https://meli.la/1DizkH4", "Xiaomi Redmi Buds 6 Play", "Audio", 4.8, 212422, "+5 mil vendidos", "Mercado Libre", False, "Precio accesible", "Audífonos compactos con Bluetooth 5.4, estuche de carga y una relación calidad-precio respaldada por miles de compradores."),
    ("https://meli.la/28prqSy", "Control inalámbrico 8BitDo Ultimate 2C", "Gaming", 4.9, 1879, "+500 vendidos", "Mercado Libre", False, "Buena reputación", "Control para PC y Android con joysticks de efecto Hall, receptor USB y respuesta rápida para reducir el riesgo de drift."),
    ("https://meli.la/1SraBRS", "Hub USB-C Ugreen 6 en 1", "Accesorios", 4.9, 157, "+1,000 vendidos", "Tienda oficial Ugreen", True, "Oferta destacada", "Amplía una laptop compatible con HDMI 4K a 30 Hz, tres USB-A y alimentación USB-C en un cuerpo compacto."),
    ("https://meli.la/2m58JFu", "Focos inteligentes TP-Link Tapo L530E, paquete de 4", "Hogar inteligente", 4.8, 142, "+100 vendidos", "Mercado Libre", False, "Precio competitivo", "Cuatro focos RGB regulables con control desde la aplicación Tapo y compatibilidad con Alexa y Google Assistant."),
    ("https://meli.la/1Y4WW4U", "Adaptador Wi-Fi USB TP-Link Archer T3U Plus", "Conectividad", 4.8, 684, "+1,000 vendidos", "Mercado Libre", False, "Precio competitivo", "Adaptador USB 3.0 de doble banda AC1300 con antena ajustable para mejorar la conectividad de una computadora compatible."),
    ("https://meli.la/2VSkGqF", "Bocina portátil Xiaomi Sound Pocket", "Audio", 4.8, 279, "+10 mil vendidos", "Tienda oficial Xiaomi", True, "Oferta destacada", "Bocina compacta de 5 W, resistente al agua y con batería recargable para escuchar audio en espacios pequeños o exteriores."),
    ("https://meli.la/24niEbF", "Enchufe inteligente TP-Link Tapo P100", "Hogar inteligente", 4.8, 135, "+1,000 vendidos", "Tienda oficial TP-Link", True, "Oferta destacada", "Permite encender, apagar y programar dispositivos compatibles desde Tapo, Alexa o Google Assistant sin concentrador adicional."),
    ("https://meli.la/2hQPuxN", "Cámara exterior TP-Link Tapo C500", "Hogar inteligente", 4.8, 25470, "+50 mil vendidos", "Tienda oficial TP-Link", True, "Oferta destacada", "Cámara Full HD con cobertura de 360 grados, visión nocturna a color, audio bidireccional y protección IP65."),
    ("https://meli.la/1WG5usZ", "Monitor LG 24MR400-W IPS de 24 pulgadas", "Monitores", 4.9, 307, "+1,000 vendidos", "Tienda oficial LG", True, "Oferta destacada", "Panel IPS Full HD de 100 Hz con FreeSync, HDMI y montaje VESA para trabajo, estudio y juego casual."),
    ("https://meli.la/2e9ahbx", "Teclado Logitech Pebble Keys 2 K380s", "Accesorios", 4.9, 8477, "+1,000 vendidos", "Tienda oficial Logitech", True, "Oferta destacada", "Teclado Bluetooth compacto y silencioso que permite alternar entre tres dispositivos para estudiar o trabajar."),
    ("https://meli.la/1asgmcT", "Micrófono USB Maono DGM20 RGB", "Audio", 4.8, 2133, "+5 mil vendidos", "Tienda oficial MAONO", True, "Oferta destacada", "Micrófono cardioide con cancelación de ruido, control de ganancia, monitoreo y conexión USB para streaming y videollamadas."),
    ("https://meli.la/1YeqyKE", "Switch TP-Link TL-SG105 Gigabit de 5 puertos", "Conectividad", 4.9, 2763, "+5 mil vendidos", "Tienda oficial TP-Link", True, "Buena reputación", "Amplía una red cableada con cinco puertos gigabit, instalación directa y carcasa metálica compacta."),
    ("https://meli.la/2R4SzoV", "Cargador Samsung GaN de 25 W USB-C", "Accesorios", 4.9, 1873, "+10 mil vendidos", "Mercado Libre", False, "Precio competitivo", "Cargador compacto con Power Delivery y PPS para carga rápida de equipos Samsung compatibles; no incluye cable."),
    ("https://meli.la/2mQiPzT", "Audífonos HyperX Cloud Stinger 2 Core", "Gaming", 4.8, 2668, "+1,000 vendidos", "LA FUENTE INFORMÁTICA", False, "Oferta destacada", "Audífonos alámbricos ligeros con micrófono para jugar en PC o consola; una opción accesible con amplio respaldo de compradores."),
]


REVIEW_SNAPSHOT_DATE = "2026-09-10T00:00:00-05:00"
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
    "https://meli.la/2boUWLq": {
        "rating": 4.9, "reviews": 1990,
        "snippets": [
            "La imagen se ve clara y la instalación resulta sencilla para videollamadas y clases.",
            "El micrófono cumple, aunque para grabaciones exigentes conviene usar uno dedicado.",
        ],
    },
    "https://meli.la/1DizkH4": {
        "rating": 4.8, "reviews": 212422,
        "snippets": [
            "El sonido tiene buenos graves y los audífonos son cómodos durante varias horas.",
            "La batería dura bien y el emparejamiento con el teléfono es rápido.",
        ],
    },
    "https://meli.la/28prqSy": {
        "rating": 4.9, "reviews": 1879,
        "snippets": [
            "Los joysticks de efecto Hall se sienten precisos y los materiales son resistentes.",
            "La conexión en PC es rápida y la batería ofrece varias sesiones de juego.",
        ],
    },
    "https://meli.la/1SraBRS": {
        "rating": 4.9, "reviews": 157,
        "snippets": [
            "Permite conectar pantalla y varios accesorios al mismo tiempo sin complicaciones.",
            "La construcción se siente sólida y cumple con los puertos anunciados.",
        ],
    },
    "https://meli.la/2m58JFu": {
        "rating": 4.8, "reviews": 142,
        "snippets": [
            "Son fáciles de configurar, agrupar y controlar con el asistente de voz.",
            "El brillo es bueno; después de un apagón puede ser necesario volver a enlazarlos.",
        ],
    },
    "https://meli.la/1Y4WW4U": {
        "rating": 4.8, "reviews": 684,
        "snippets": [
            "Mejoró la señal incluso a varios metros del módem y atravesando paredes.",
            "Windows lo reconoció rápidamente y la conexión se mantuvo estable.",
        ],
    },
    "https://meli.la/2VSkGqF": {
        "rating": 4.8, "reviews": 279,
        "snippets": [
            "El sonido sorprende para su tamaño, con medios claros y graves agradables.",
            "Es cómoda de transportar y la batería tiene buena duración para uso diario.",
        ],
    },
    "https://meli.la/24niEbF": {
        "rating": 4.8, "reviews": 135,
        "snippets": [
            "La aplicación es sencilla y permite programar horarios de encendido y apagado.",
            "Se integra con Alexa sin dificultad y resulta útil para automatizaciones básicas.",
        ],
    },
    "https://meli.la/2hQPuxN": {
        "rating": 4.8, "reviews": 25470,
        "snippets": [
            "La imagen es clara de día y de noche, y la aplicación organiza bien las grabaciones.",
            "La detección es sensible y puede generar demasiadas notificaciones si no se ajusta.",
        ],
    },
    "https://meli.la/1WG5usZ": {
        "rating": 4.9, "reviews": 307,
        "snippets": [
            "Los colores se ven vivos y el tamaño facilita trabajar con varias ventanas.",
            "Cumple con los 100 Hz; conviene ajustar el brillo inicial al gusto.",
        ],
    },
    "https://meli.la/2e9ahbx": {
        "rating": 4.9, "reviews": 8477,
        "snippets": [
            "Se conecta con facilidad a varios dispositivos y sus teclas resultan silenciosas.",
            "El formato compacto facilita transportarlo; conviene revisar la distribución elegida.",
        ],
    },
    "https://meli.la/1asgmcT": {
        "rating": 4.8, "reviews": 2133,
        "snippets": [
            "El audio se percibe claro y la cancelación de ruido ayuda a aislar la voz.",
            "Es fácil de configurar; la ganancia y el monitoreo permiten ajustar la grabación.",
        ],
    },
    "https://meli.la/1YeqyKE": {
        "rating": 4.9, "reviews": 2763,
        "snippets": [
            "La carcasa metálica se siente sólida y mantiene estable la conexión gigabit.",
            "La instalación es directa: basta conectar los cables para comenzar a usarlo.",
        ],
    },
    "https://meli.la/2R4SzoV": {
        "rating": 4.9, "reviews": 1873,
        "snippets": [
            "La carga rápida funciona bien con equipos Samsung compatibles y sin calentamiento excesivo.",
            "No incluye cable USB-C; hay que considerar ese accesorio por separado.",
        ],
    },
    "https://meli.la/2mQiPzT": {
        "rating": 4.8, "reviews": 2668,
        "snippets": [
            "Son ligeros y cómodos para sesiones de juego, con buen aislamiento.",
            "El audio cumple por el precio; algunos compradores prefieren graves más fuertes.",
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
        catalog_product_id = source["catalog_product_id"] or re.search(
            r"/(MLMU?\d+)", source["permalink"]
        ).group(1)
        permalink = source["permalink"]
        if not permalink.startswith("https://www.mercadolibre.com.mx/"):
            permalink = f"https://www.mercadolibre.com.mx/p/{catalog_product_id}"
        products.append({
            "id": source["item_id"],
            "catalog_product_id": catalog_product_id,
            "permalink": permalink,
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
