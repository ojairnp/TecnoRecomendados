# TecnoRecomendados MX

Sitio estático de oportunidades tecnológicas para México. La portada prioriza productos con precio revisado, reputación pública, contexto editorial y enlaces de compra proporcionados por el propietario.

## Probar localmente

```bash
python -m http.server 8770
```

Abrir `http://127.0.0.1:8770/`.

## Validar

```bash
python -m unittest discover -s tests -v
```

## Agregar productos

1. Agregar enlaces únicos a `config/candidate-links.json`.
2. Ejecutar `scripts/research_products.py` para resolver y recopilar la ficha pública.
3. Revisar precio, alternativas del mismo producto, tienda, ventas y opiniones.
4. Incorporar únicamente los seleccionados en `scripts/build_catalog.py` y generar `data/products.json`.

Cada ficha conserva literalmente el enlace corto recibido. “Mejor precio visible” solo se usa cuando la oferta coincide con el menor precio observado entre las opciones nuevas del mismo producto durante la revisión; no significa el menor precio de todo el mercado.
