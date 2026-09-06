# TecnoRecomendados MX

Sitio estático de oportunidades tecnológicas para México. La portada prioriza productos con precio revisado, reputación pública, contexto editorial y enlaces de compra proporcionados por el propietario.

El gancho y el producto principal rotan en cada apertura para mantener fresca la portada. El contenido cambia, pero siempre usa productos disponibles y datos del catálogo realmente actualizado; la fecha mostrada nunca se simula.

## Probar localmente

```bash
python -m http.server 8770
```

Abrir `http://127.0.0.1:8770/`.

## Validar

```bash
npm run test:catalog
python -m unittest discover -s tests -v
```

## Actualización diaria

El flujo `Actualizar precios diarios` se ejecuta todos los días a las 06:23, hora de Cancún, y también puede iniciarse manualmente desde GitHub Actions. Consulta únicamente las ligas oficiales guardadas, actualiza precio, descuento, disponibilidad e imagen y publica el cambio solo si las pruebas pasan.

Los extractos de opiniones se seleccionan editorialmente de comentarios públicos de compradores, sin nombres ni datos personales. Se conservan durante la actualización de precios porque Mercado Libre requiere autorización para automatizar de forma confiable el contenido escrito de las reseñas.

Para comprobar una actualización local:

```bash
npm run update-catalog
```

## Agregar productos

1. Agregar enlaces únicos a `config/candidate-links.json`.
2. Ejecutar `scripts/research_products.py` para resolver y recopilar la ficha pública.
3. Revisar precio, alternativas del mismo producto, tienda, ventas y opiniones.
4. Incorporar únicamente los seleccionados y sus extractos de opiniones en `scripts/build_catalog.py`.
5. Generar `data/products.json` y ejecutar todas las validaciones.

Cada ficha conserva literalmente el enlace corto recibido. “Mejor precio visible” solo se usa cuando la oferta coincide con el menor precio observado entre las opciones nuevas del mismo producto durante la revisión; no significa el menor precio de todo el mercado.
