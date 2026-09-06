# TecnoRecomendados MX

Sitio estático de recomendaciones de tecnología para México. La primera versión incluye estructura de tienda, categorías, contenido editorial, SEO técnico, transparencia de afiliados y una ruta preparada para el retorno OAuth de Mercado Libre.

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

Los productos reales se incorporan en `data/products.json`. Cada ficha debe conservar el enlace afiliado recibido y usar datos verificados; no se deben inventar precios, valoraciones ni disponibilidad.
