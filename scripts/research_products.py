#!/usr/bin/env python3
"""Resolve affiliate links and extract the public featured product card."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import re
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


ALLOWED_SHORT_HOSTS = {"meli.la", "mercado.li"}
ALLOWED_MARKET_HOSTS = {"mercadolibre.com.mx", "www.mercadolibre.com.mx"}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36"
)


def is_allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() in (
        ALLOWED_SHORT_HOSTS | ALLOWED_MARKET_HOSTS
    )


class OfficialRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urljoin(req.full_url, newurl)
        if not is_allowed_url(target):
            raise ValueError(f"Redirección rechazada hacia dominio no oficial: {target}")
        return super().redirect_request(req, fp, code, msg, headers, target)


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def component(card: dict[str, Any], kind: str) -> dict[str, Any]:
    for entry in card.get("components", []):
        if entry.get("type") == kind:
            return entry.get(kind, {})
    return {}


def extract_render_context(html: str) -> dict[str, Any]:
    marker = "_n.ctx.r="
    start = html.find(marker)
    if start < 0:
        raise ValueError("La página no contiene datos estructurados de producto")
    payload, _ = json.JSONDecoder().raw_decode(html[start + len(marker) :])
    return payload


def extract_card(context: dict[str, Any]) -> dict[str, Any]:
    recommendation_blocks = [
        node
        for node in walk(context)
        if isinstance(node.get("recommendation_info"), dict)
        and node["recommendation_info"].get("polycards")
    ]
    if not recommendation_blocks:
        raise ValueError("No se encontró la ficha destacada del producto")
    block = recommendation_blocks[0]
    return block["recommendation_info"]["polycards"][0]


def image_url(card: dict[str, Any]) -> str | None:
    pictures = card.get("pictures", {}).get("pictures", [])
    if not pictures:
        return None
    picture_id = pictures[0].get("id")
    if not picture_id:
        return None
    return f"https://http2.mlstatic.com/D_NQ_NP_2X_{picture_id}-F.webp"


def extract_product(link: str, timeout: int) -> dict[str, Any]:
    if not is_allowed_url(link) or urlparse(link).hostname not in ALLOWED_SHORT_HOSTS:
        raise ValueError("El enlace inicial no es meli.la o mercado.li con HTTPS")

    request = Request(
        link,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "es-MX,es;q=0.9"},
    )
    opener = build_opener(OfficialRedirectHandler())
    with opener.open(request, timeout=timeout) as response:
        final_url = response.geturl()
        if not is_allowed_url(final_url):
            raise ValueError(f"Destino final no permitido: {final_url}")
        html = response.read().decode("utf-8", errors="replace")

    context = extract_render_context(html)
    card = extract_card(context)
    metadata = card.get("metadata", {})
    title = component(card, "title")
    seller = component(card, "seller")
    price = component(card, "price")
    reviews = component(card, "reviews")
    highlight = component(card, "highlight")
    shipping = component(card, "shipping")
    current = price.get("current_price", {})
    previous = price.get("previous_price", {}) or {}
    discount = price.get("discount_label", {}) or {}

    return {
        "affiliate_url": link,
        "item_id": metadata.get("id"),
        "catalog_product_id": metadata.get("product_id"),
        "title": title.get("text"),
        "seller": seller.get("text"),
        "price": current.get("value"),
        "currency": current.get("currency"),
        "previous_price": previous.get("value"),
        "discount_label": discount.get("text"),
        "highlight": highlight.get("text"),
        "reviews": reviews,
        "shipping": shipping.get("text"),
        "image": image_url(card),
        "permalink": f"https://{metadata.get('url')}" if metadata.get("url") else None,
        "available": bool(metadata.get("id") and title.get("text") and current.get("value")),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=35)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()

    links = json.loads(args.config.read_text(encoding="utf-8")).get("links", [])
    products: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    unique_links = list(dict.fromkeys(links))
    completed: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as pool:
        futures = {
            pool.submit(extract_product, link, args.timeout): link for link in unique_links
        }
        for index, future in enumerate(as_completed(futures), start=1):
            link = futures[future]
            print(f"[{index}/{len(unique_links)}] {link}", flush=True)
            try:
                completed[link] = future.result()
            except Exception as exc:  # keep researching remaining user-provided links
                errors.append({"affiliate_url": link, "error": str(exc)})
    products = [completed[link] for link in unique_links if link in completed]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "products": products,
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Productos: {len(products)}; errores: {len(errors)}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
