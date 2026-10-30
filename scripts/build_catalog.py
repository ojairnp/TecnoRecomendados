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
    ("https://meli.la/26bsPra", "Webcam Logitech Brio 100 Full HD", "Videollamadas", 4.8, 6655, "+5 mil vendidos", "Tienda oficial Logitech", True, "Oferta destacada", "Webcam 1080p con corrección automática de luz, micrófono y tapa de privacidad para clases y reuniones."),
    ("https://meli.la/1FmDSVB", "Bocina Soundcore Select 4 Go", "Audio", 4.9, 4602, "+5 mil vendidos", "Tienda oficial Soundcore", True, "Oferta destacada", "Bocina compacta de 5 W con protección IP67, hasta 20 horas de batería y sonido configurable desde la aplicación."),
    ("https://meli.la/12nCyhu", "Cargador Ugreen Nexode GaN de 65 W", "Accesorios", 4.9, 3145, "+10 mil vendidos", "Home Security", False, "Oferta destacada", "Cargador compacto con dos puertos USB-C y uno USB-A para equipos compatibles; la potencia se distribuye al conectar varios dispositivos."),
    ("https://meli.la/1syad5R", "Amazon Echo Pop con Alexa", "Hogar inteligente", 4.9, 108879, "+100 mil vendidos", "Tienda oficial Coolbox", True, "Oferta destacada", "Asistente compacto para música, recordatorios y control por voz de dispositivos inteligentes compatibles."),
    ("https://meli.la/2QUUKCK", "Xiaomi Smart Band 9 Active", "Wearables", 4.8, 20417, "+10 mil vendidos", "Tienda oficial Xiaomi", True, "Precio destacado", "Banda ligera con seguimiento de actividad, resistencia al agua y batería de larga duración para uso cotidiano."),
    ("https://meli.la/1PGh198", "Cable Ugreen USB-C de 240 W y 2 metros", "Accesorios", 4.9, 428, "+1,000 vendidos", "Tienda oficial Ugreen", True, "Oferta destacada", "Cable USB-C reforzado con Power Delivery 3.1 para cargar equipos compatibles; sus 240 W requieren un cargador y dispositivo adecuados."),
    ("https://meli.la/18Ymczo", "Panel LED Neewer 660 Pro RGB", "Creación de contenido", 4.9, 123, "+1,000 vendidos", "NEEWERPHOTOMX", False, "Oferta destacada", "Panel RGB de 50 W con control por aplicación, temperatura ajustable y alto CRI para fotografía, video y streaming."),
    ("https://meli.la/2kSnh5A", "Audífonos inalámbricos AIWA AWK17U", "Audio", 4.8, 2012, "+1,000 vendidos", "Tienda oficial AIWA", True, "Oferta destacada", "Audífonos Bluetooth 5.3 ligeros con micrófono y hasta diez horas de reproducción a un precio accesible."),
    ("https://meli.la/2nAfn5A", "Mouse Logitech M196 Bluetooth", "Accesorios", 4.9, 6635, "+1,000 vendidos", "Mercado Libre", True, "Oferta destacada", "Mouse Bluetooth compacto y económico que libera el puerto USB y funciona con computadoras o tabletas compatibles."),
    ("https://meli.la/1qyJsH3", "Mouse ergonómico Logitech MX Vertical", "Accesorios", 4.9, 1285, "+1,000 vendidos", "Tienda oficial Logitech", True, "Ergonomía destacada", "Mouse vertical recargable para diestros, pensado para una postura menos forzada durante jornadas prolongadas."),
    ("https://meli.la/2xWUnzh", "Teclado mecánico Redragon Kumara K552", "Gaming", 4.9, 30036, "+1,000 vendidos", "Tienda oficial Redragon", True, "Precio destacado", "Teclado mecánico compacto en español latinoamericano, con estructura firme, iluminación y amplio respaldo de compradores."),
    ("https://meli.la/2QREFW9", "Memoria SanDisk Extreme Pro SDXC de 64 GB", "Almacenamiento", 4.9, 2482, "+10 mil vendidos", "SanDisk", True, "Alta velocidad", "Tarjeta SDXC UHS-I para fotografía y video 4K, con lectura de hasta 200 MB/s y una reputación sobresaliente."),
    ("https://meli.la/1Gptf9P", "Xiaomi Robot Vacuum X20+", "Hogar inteligente", 4.8, 2777, "+1,000 vendidos", "Tienda oficial Xiaomi", True, "Oferta destacada", "Aspiradora y trapeadora con navegación láser, estación automática y 6,000 Pa para reducir el trabajo de limpieza diaria."),
    ("https://meli.la/1oQ5HSb", "Proyector Wanbo X5 Pro Full HD", "Proyectores", 4.8, 334, "+1,000 vendidos", "Tienda oficial Wanbo", True, "Oferta destacada", "Proyector Full HD nativo de 1,100 lúmenes ANSI con Google TV, HDR10 y buenas referencias para cine en casa."),
    ("https://meli.la/2Fzig3F", "Bocina Sony ULT Field 3", "Audio", 4.9, 394, "+100 vendidos", "Tienda oficial Sony", True, "Oferta destacada", "Bocina portátil con graves potentes, conectividad Bluetooth y batería de larga duración, respaldada por la tienda oficial."),
    ("https://meli.la/1nCcKCX", "Audífonos profesionales Sony MDR-7506", "Audio", 4.9, 1621, "+5 mil vendidos", "Tienda oficial Sony", True, "Oferta destacada", "Audífonos de monitoreo con sonido detallado, cable largo y amplio respaldo de compradores para producción, edición y escucha crítica."),
    ("https://meli.la/2RsMc3Q", "Router Tenda RX2 Pro Wi-Fi 6 AX1500", "Conectividad", 4.7, 1236, "+1,000 vendidos", "Tienda oficial Tenda", True, "Oferta destacada", "Router Wi-Fi 6 de doble banda con puertos Gigabit, cinco antenas, WPA3, OFDMA y MU-MIMO para hogares con varios dispositivos."),
    ("https://meli.la/13AyJLh", "Hub ORICO USB 3.0 de 4 puertos con clip", "Accesorios", 4.8, 114, "+1,000 vendidos", "Tienda oficial ORICO", True, "Oferta destacada", "Hub de aluminio que acerca cuatro puertos USB 3.0 al borde de un monitor o escritorio y ayuda a ordenar el espacio de trabajo."),
    ("https://meli.la/1kkqWcx", "Paquete de 2 cámaras exteriores YUTUCAM de 3 MP", "Hogar inteligente", 4.8, 189, "+1,000 vendidos", "Tienda oficial YUTUCAM", True, "Oferta destacada", "Dos cámaras PTZ para exterior con visión nocturna, audio bidireccional, alertas de movimiento y almacenamiento microSD opcional."),
    ("https://meli.la/1khYKtN", "Audífonos Soundcore Space One con cancelación de ruido", "Audio", 4.8, 4508, "+1,000 vendidos", "Tienda oficial Soundcore", True, "Oferta destacada", "Audífonos over-ear con cancelación activa, audio LDAC y hasta 40 horas de batería con ANC a un precio competitivo."),
    ("https://meli.la/2EiJLM7", "Xiaomi TV Stick 4K de segunda generación", "Streaming", 4.9, 3698, "+1,000 vendidos", "iMPORTS77", False, "Oferta destacada", "Convierte una pantalla compatible en un centro de streaming 4K con Google TV, Wi-Fi 6, Dolby Vision y control por voz."),
    ("https://meli.la/2zSpgRx", "Impresora Epson EcoTank L3250 con Wi-Fi", "Cómputo", 4.8, 3078, "+1,000 vendidos", "COMPUNEZA_468", False, "Costo por página", "Impresora, escáner y copiadora con tanque de tinta recargable y Wi-Fi Direct para hogar, estudio o una oficina pequeña."),
    ("https://meli.la/1E2fxqR", "Monitor portátil ARZOPA A1 Full HD de 15.6 pulgadas", "Monitores", 4.8, 64, "+1,000 vendidos", "ARZOPA", False, "Oferta destacada", "Segunda pantalla IPS ligera para trabajo, programación, viajes y consolas compatibles mediante HDMI o USB-C."),
    ("https://meli.la/11wa2qw", "Roku Streaming Stick 3840 con control de voz", "Streaming", 4.9, 73240, "+100 mil vendidos", "EMTECH, vendido por Mercado Libre", False, "Más vendido", "Reproductor Full HD compacto con control por voz, Wi-Fi de doble banda y una reputación sobresaliente para actualizar televisores compatibles."),
    ("https://meli.la/2vCWcJL", "Bocina Soundcore Boom 2 de 80 W", "Audio", 4.9, 2163, "+1,000 vendidos", "Tienda oficial Soundcore", True, "Oferta destacada", "Bocina potente con BassUp 2.0, protección IPX7, batería prolongada y función de power bank para reuniones y exteriores."),
    ("https://meli.la/2y85nNX", "Power bank Anker MagGo Qi2 de 10,000 mAh", "Accesorios", 4.8, 3005, "+1,000 vendidos", "Tienda oficial ANKER", True, "Oferta destacada", "Batería ultradelgada con carga magnética Qi2 de 15 W y USB-C de 30 W para mantener equipos compatibles cargados fuera de casa."),
    ("https://meli.la/2trZ1yK", "Teclado mecánico Terport Z11 inalámbrico 60%", "Gaming", 4.8, 886, "+1,000 vendidos", "Tienda oficial Terport", True, "Oferta destacada", "Teclado compacto en español latinoamericano con switches rojos, Bluetooth, receptor 2.4 GHz, cable USB-C y retroiluminación RGB."),
    ("https://meli.la/2RGVSq1", "DJI Mic Mini 2 con dos transmisores y estuche", "Creación de contenido", 4.9, 232, "+5 mil vendidos", "Tienda oficial DJI", True, "Oferta destacada", "Kit de micrófonos inalámbricos compacto con dos transmisores, receptor móvil y estuche de carga para video, entrevistas y contenido móvil."),
    ("https://meli.la/1Tq5dQ7", "Xiaomi Redmi Watch 5 Active", "Wearables", 4.8, 58197, "+100 mil vendidos", "Tienda oficial Compupaz", True, "Precio destacado", "Reloj inteligente con llamadas Bluetooth, pantalla de 2 pulgadas, seguimiento de actividad y batería de larga duración a un precio accesible."),
    ("https://meli.la/2Fk2XBv", "TP-Link Deco X50 Wi-Fi 6 Mesh, paquete de 3", "Conectividad", 4.9, 6109, "+100 vendidos", "Tienda oficial TP-Link", True, "Oferta destacada", "Tres nodos Wi-Fi 6 AX3000 con WPA3, control parental y puertos Gigabit para mejorar la cobertura y estabilidad de redes domésticas."),
    ("https://meli.la/1LTj4GW", "Mouse Logitech Signature M650 L", "Accesorios", 4.9, 1490, "+100 vendidos", "Tienda oficial IQTECH MX", True, "Precio destacado", "Mouse silencioso de tamaño completo con Bluetooth, receptor Logi Bolt, rueda SmartWheel y botones laterales configurables."),
    ("https://meli.la/2Yk8AMX", "APC Back-UPS BE600 de 600 VA", "Energía", 4.8, 188, "+1,000 vendidos", "Tienda oficial PCEL", True, "Precio destacado", "UPS de 600 VA y 330 W con siete contactos y puerto USB para proteger módems, computadoras y equipos de red durante cortes breves."),
    ("https://meli.la/1oNwFo1", "Consola portátil ASUS ROG Xbox Ally, Ryzen Z2 A", "Gaming", 4.8, 648, "+1,000 vendidos", "Tienda oficial ASUS", True, "Oferta destacada", "Consola portátil con Ryzen Z2 A, 16 GB de RAM, SSD de 512 GB y pantalla Full HD de 7 pulgadas para jugar en Windows dentro y fuera de casa."),
]


REVIEW_SNAPSHOT_DATE = "2026-09-11T00:00:00-05:00"
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
    "https://meli.la/26bsPra": {
        "rating": 4.8, "reviews": 6655,
        "snippets": [
            "La imagen es clara para videollamadas y la instalación resulta sencilla.",
            "La tapa de privacidad es práctica; el video está limitado a 30 cuadros por segundo.",
        ],
    },
    "https://meli.la/1FmDSVB": {
        "rating": 4.9, "reviews": 4602,
        "snippets": [
            "El sonido conserva buena claridad incluso a volumen alto y la batería dura bastante.",
            "Es ligera y resistente al agua; sus 5 W están pensados para espacios pequeños.",
        ],
    },
    "https://meli.la/12nCyhu": {
        "rating": 4.9, "reviews": 3145,
        "snippets": [
            "Se siente compacto y sólido, y permite cargar teléfonos y computadoras compatibles.",
            "Al utilizar varios puertos se divide la potencia y algunos compradores reportan calentamiento.",
        ],
    },
    "https://meli.la/1syad5R": {
        "rating": 4.9, "reviews": 108879,
        "snippets": [
            "La configuración es sencilla y los micrófonos responden bien en una habitación.",
            "Necesita permanecer conectado a corriente y su sonido es menos potente que un Echo Dot.",
        ],
    },
    "https://meli.la/2QUUKCK": {
        "rating": 4.8, "reviews": 20417,
        "snippets": [
            "La correa resulta cómoda y la batería tiene buena duración para el uso diario.",
            "No incluye GPS y la autonomía real depende de las funciones activadas.",
        ],
    },
    "https://meli.la/1PGh198": {
        "rating": 4.9, "reviews": 428, "checked_at": "2026-09-15T00:00:00-05:00",
        "snippets": [
            "La conexión se siente firme y los dos metros de longitud resultan cómodos para el uso diario.",
            "Carga dispositivos compatibles con rapidez; la transferencia de datos está limitada a velocidad USB 2.0.",
        ],
    },
    "https://meli.la/18Ymczo": {
        "rating": 4.9, "reviews": 123, "checked_at": "2026-09-15T00:00:00-05:00",
        "snippets": [
            "La luz tiene buena potencia, materiales sólidos y muchas opciones de color desde la aplicación.",
            "La publicación incluye un panel y maleta; el trípode y las baterías recargables se compran por separado.",
        ],
    },
    "https://meli.la/2kSnh5A": {
        "rating": 4.8, "reviews": 2012, "checked_at": "2026-09-15T00:00:00-05:00",
        "snippets": [
            "El sonido y los graves cumplen bien por el precio, y el diseño ligero resulta cómodo.",
            "No tienen cancelación activa de ruido y las letras laterales se iluminan durante el uso.",
        ],
    },
    "https://meli.la/2nAfn5A": {
        "rating": 4.9, "reviews": 6635, "checked_at": "2026-09-15T00:00:00-05:00",
        "snippets": [
            "La conexión Bluetooth es rápida, estable y ahorra un puerto USB en la computadora.",
            "Su tamaño compacto facilita transportarlo, aunque puede sentirse pequeño en manos grandes.",
        ],
    },
    "https://meli.la/1qyJsH3": {
        "rating": 4.9, "reviews": 1285, "checked_at": "2026-09-15T00:00:00-05:00",
        "snippets": [
            "La forma vertical mejora la comodidad de la muñeca durante jornadas largas de trabajo.",
            "Está diseñado para diestros y requiere un periodo de adaptación frente a un mouse convencional.",
        ],
    },
    "https://meli.la/2xWUnzh": {
        "rating": 4.9, "reviews": 30036, "checked_at": "2026-09-19T00:00:00-05:00",
        "snippets": [
            "Se siente firme, compacto y cómodo tanto para jugar como para escribir.",
            "Las teclas mecánicas pueden resultar ruidosas si se usa de noche o en un espacio compartido.",
        ],
    },
    "https://meli.la/2QREFW9": {
        "rating": 4.9, "reviews": 2482, "checked_at": "2026-09-19T00:00:00-05:00",
        "snippets": [
            "Compradores destacan su velocidad y estabilidad al grabar fotografía y video en alta resolución.",
            "Conviene verificar la compatibilidad SDXC y la capacidad máxima admitida por el dispositivo.",
        ],
    },
    "https://meli.la/1Gptf9P": {
        "rating": 4.8, "reviews": 2777, "checked_at": "2026-09-19T00:00:00-05:00",
        "snippets": [
            "El mapeo por habitaciones y el control desde la aplicación ahorran tiempo en la limpieza cotidiana.",
            "No sustituye una limpieza profunda porque puede dejar rincones o zonas bajo ciertos muebles.",
        ],
    },
    "https://meli.la/1oQ5HSb": {
        "rating": 4.8, "reviews": 334, "checked_at": "2026-09-19T00:00:00-05:00",
        "snippets": [
            "La imagen y el brillo tienen buena relación calidad-precio en espacios oscuros o con luz moderada.",
            "El sistema integrado es práctico, aunque puede sentirse menos fluido que un reproductor externo.",
        ],
    },
    "https://meli.la/2Fzig3F": {
        "rating": 4.9, "reviews": 394, "checked_at": "2026-09-19T00:00:00-05:00",
        "snippets": [
            "El sonido es potente y envolvente, con graves notorios sin distorsión a volumen alto.",
            "Su construcción es sólida y la batería dura bien, aunque no es la bocina más compacta de la categoría.",
        ],
    },
    "https://meli.la/1nCcKCX": {
        "rating": 4.9, "reviews": 1621, "checked_at": "2026-10-11T08:30:00-05:00",
        "snippets": [
            "El sonido detallado y balanceado funciona bien para monitoreo, edición y grabación.",
            "El cable largo es útil en estudio, pero el formato alámbrico puede resultar estorboso fuera de casa.",
        ],
    },
    "https://meli.la/2RsMc3Q": {
        "rating": 4.7, "reviews": 1236, "checked_at": "2026-10-11T08:30:00-05:00",
        "snippets": [
            "Compradores destacan la estabilidad, el alcance y la facilidad de configuración para aprovechar conexiones rápidas.",
            "El modo repetidor puede requerir configuración adicional y la banda de 5 GHz pierde alcance al atravesar paredes.",
        ],
    },
    "https://meli.la/13AyJLh": {
        "rating": 4.8, "reviews": 114, "checked_at": "2026-10-11T08:30:00-05:00",
        "snippets": [
            "El cuerpo de aluminio y el clip permiten dejar los puertos firmes y al alcance en escritorios compatibles.",
            "La pinza no se ajusta bien a todas las superficies y el ancho de banda se comparte entre los cuatro puertos.",
        ],
    },
    "https://meli.la/1kkqWcx": {
        "rating": 4.8, "reviews": 189, "checked_at": "2026-10-11T08:30:00-05:00",
        "snippets": [
            "La instalación resulta sencilla y la imagen diurna y nocturna permite reconocer personas y objetos.",
            "Solo admite Wi-Fi de 2.4 GHz, necesita alimentación eléctrica y conviene revisar los permisos de la aplicación.",
        ],
    },
    "https://meli.la/1khYKtN": {
        "rating": 4.8, "reviews": 4508, "checked_at": "2026-10-17T09:02:15-05:00",
        "snippets": [
            "El sonido, la comodidad y la duración de la batería ofrecen una relación calidad-precio sobresaliente.",
            "La cancelación funciona mejor con ruidos constantes; sonidos repentinos siguen siendo perceptibles y no tiene baja latencia para jugar.",
        ],
    },
    "https://meli.la/2EiJLM7": {
        "rating": 4.9, "reviews": 3698, "checked_at": "2026-10-17T09:02:15-05:00",
        "snippets": [
            "Las aplicaciones funcionan de forma rápida y la reproducción 4K ofrece una imagen nítida por su precio.",
            "Solo dispone de 8 GB y conviene configurar el apagado para que el dispositivo no permanezca encendido con la televisión apagada.",
        ],
    },
    "https://meli.la/2zSpgRx": {
        "rating": 4.8, "reviews": 3078, "checked_at": "2026-10-17T09:02:15-05:00",
        "snippets": [
            "La tinta rinde mucho, la impresión es clara y la conexión por Wi-Fi resulta práctica para el uso diario.",
            "La impresión a doble cara es manual y algunos compradores señalan que la configuración inicial puede requerir atención.",
        ],
    },
    "https://meli.la/1E2fxqR": {
        "rating": 4.8, "reviews": 64, "checked_at": "2026-10-17T09:02:15-05:00",
        "snippets": [
            "La pantalla es ligera, fácil de conectar y útil como segundo monitor para trabajo o viajes.",
            "Los altavoces tienen volumen limitado y algunos equipos requieren alimentación adicional cuando se usa HDMI.",
        ],
    },
    "https://meli.la/11wa2qw": {
        "rating": 4.9, "reviews": 73240, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "Compradores destacan la instalación sencilla, la interfaz fluida y la comodidad del control por voz.",
            "La resolución máxima es Full HD, no 4K, y el alcance del control puede variar según la ubicación del equipo.",
        ],
    },
    "https://meli.la/2vCWcJL": {
        "rating": 4.9, "reviews": 2163, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "El sonido potente, los bajos presentes y la conexión sencilla reciben buenos comentarios para uso dentro y fuera de casa.",
            "La autonomía anunciada depende del volumen y de funciones como BassUp y las luces, por lo que puede reducirse con uso intensivo.",
        ],
    },
    "https://meli.la/2y85nNX": {
        "rating": 4.8, "reviews": 3005, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "El diseño delgado, los materiales y la carga por USB-C ofrecen una solución práctica para llevar energía adicional.",
            "La carga inalámbrica es más lenta que por cable y la fijación magnética en Android puede requerir una funda o aro compatible.",
        ],
    },
    "https://meli.la/2trZ1yK": {
        "rating": 4.8, "reviews": 886, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "El formato compacto, los colores y la construcción reciben buenos comentarios por su relación calidad-precio.",
            "El diseño de 60% elimina teclas dedicadas y algunos compradores consideran mejorables los switches incluidos para jugar en PC.",
        ],
    },
    "https://meli.la/2RGVSq1": {
        "rating": 4.9, "reviews": 232, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "El audio claro, el tamaño compacto y los protectores contra viento destacan para grabaciones y contenido móvil.",
            "Conviene confirmar el conector del receptor antes de comprar; algunos usuarios reportan que el adaptador esperado para iPhone no venía incluido.",
        ],
    },
    "https://meli.la/1Tq5dQ7": {
        "rating": 4.8, "reviews": 58197, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "Las llamadas desde la muñeca, la función para localizar el teléfono y la relación calidad-precio reciben buenos comentarios.",
            "La duración real de la batería depende del uso y sus mediciones de bienestar son orientativas, no sustituyen equipo médico.",
        ],
    },
    "https://meli.la/2Fk2XBv": {
        "rating": 4.9, "reviews": 6109, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "Compradores destacan la mejora de cobertura, la estabilidad y la configuración sencilla desde la aplicación Deco.",
            "La cobertura final depende de paredes y ubicación; conviene distribuir los nodos y usar backhaul cableado cuando sea posible.",
        ],
    },
    "https://meli.la/1LTj4GW": {
        "rating": 4.9, "reviews": 1490, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "La precisión, los clics silenciosos y la comodidad para jornadas largas son los aspectos más valorados.",
            "Es la versión grande para diestros; algunos compradores consideran más ruidoso el clic de la rueda y algo flojos los botones laterales.",
        ],
    },
    "https://meli.la/2Yk8AMX": {
        "rating": 4.8, "reviews": 188, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "Su funcionamiento silencioso y el respaldo para módems o equipos esenciales reciben buenas referencias en cortes breves.",
            "La autonomía depende de la carga conectada; un comprador obtuvo cerca de veinte minutos con Starlink y el límite es de 330 W.",
        ],
    },
    "https://meli.la/1oNwFo1": {
        "rating": 4.8, "reviews": 648, "checked_at": "2026-10-30T00:00:00-05:00",
        "snippets": [
            "La portabilidad, la pantalla Full HD y la posibilidad de usar juegos y aplicaciones de Windows son sus principales atractivos.",
            "La autonomía depende del juego, el brillo y el modo de rendimiento; para sesiones largas conviene tener el cargador cerca.",
        ],
    },
}


def resolve_catalog_product_id(source: dict, cached: dict | None = None) -> str:
    """Return a stable Mercado Libre identity for catalog and non-catalog listings."""
    candidates = [
        source.get("catalog_product_id"),
        (cached or {}).get("catalog_product_id"),
    ]
    permalink_match = re.search(r"/(MLMU?\d+)", source.get("permalink") or "")
    if permalink_match:
        candidates.append(permalink_match.group(1))
    candidates.append(source.get("item_id"))
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.startswith("MLM"):
            return candidate
    raise ValueError(f"No se pudo determinar un identificador oficial para {source.get('permalink')}")


def canonical_product_permalink(source: dict, catalog_product_id: str, cached: dict | None = None) -> str:
    """Prefer a public www permalink and reuse the last verified one when needed."""
    source_permalink = source.get("permalink") or ""
    if source_permalink.startswith("https://www.mercadolibre.com.mx/"):
        return source_permalink
    cached_permalink = (cached or {}).get("permalink") or ""
    if cached_permalink.startswith("https://www.mercadolibre.com.mx/"):
        return cached_permalink
    return f"https://www.mercadolibre.com.mx/p/{catalog_product_id}"


def main() -> None:
    research = json.loads(RESEARCH.read_text(encoding="utf-8"))
    by_link = {product["affiliate_url"]: product for product in research["products"]}
    existing = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {"products": []}
    existing_by_link = {product["affiliate_url"]: product for product in existing["products"]}
    products = []
    for entry in CURATION:
        link, title, category, rating, reviews, sold, seller, official, signal, reason = entry
        source = by_link.get(link)
        if source is None:
            cached = existing_by_link.get(link)
            if cached is None:
                raise KeyError(f"No hay investigación vigente ni ficha previa para {link}")
            source = {
                "item_id": cached["id"],
                "catalog_product_id": cached["catalog_product_id"],
                "permalink": cached["permalink"],
                "price": cached["price"],
                "previous_price": cached.get("previous_price"),
                "currency": cached.get("currency", "MXN"),
                "discount_label": f'{cached["discount"]}% OFF' if cached.get("discount") is not None else None,
                "image": cached["image"],
                "_last_price_check": cached.get("last_price_check"),
            }
        review_snapshot = REVIEW_SNAPSHOTS[link]
        discount_match = re.search(r"(\d+)%", source.get("discount_label") or "")
        cached = existing_by_link.get(link)
        catalog_product_id = resolve_catalog_product_id(source, cached)
        permalink = canonical_product_permalink(source, catalog_product_id, cached)
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
            "last_price_check": source.get("_last_price_check") or research["generated_at"],
            "last_review_check": review_snapshot.get("checked_at", REVIEW_SNAPSHOT_DATE),
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
