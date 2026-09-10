#!/usr/bin/env node

import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';


const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CATALOG_PATH = path.join(ROOT, 'data', 'products.json');
const USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36';
const SHORT_HOSTS = new Set(['meli.la', 'mercado.li']);
const MARKET_HOSTS = new Set(['mercadolibre.com.mx', 'www.mercadolibre.com.mx']);


export function isAllowedUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && (SHORT_HOSTS.has(url.hostname) || MARKET_HOSTS.has(url.hostname));
  } catch {
    return false;
  }
}


export function canonicalPermalink(metadata, fallback) {
  if (!metadata?.url) return fallback;
  const candidate = metadata.url.startsWith('https://')
    ? metadata.url
    : `https://${metadata.url}`;
  try {
    const parsed = new URL(candidate);
    if (parsed.protocol === 'https:' && MARKET_HOSTS.has(parsed.hostname)) return candidate;
  } catch {
    return fallback;
  }
  if (metadata.product_id) {
    return `https://www.mercadolibre.com.mx/p/${metadata.product_id}`;
  }
  return fallback;
}


export function extractAssignedJson(html, marker = '_n.ctx.r=') {
  const markerIndex = html.indexOf(marker);
  if (markerIndex < 0) throw new Error('No se encontró el bloque estructurado de Mercado Libre');
  let start = markerIndex + marker.length;
  while (/\s/.test(html[start])) start += 1;
  if (html[start] !== '{') throw new Error('El bloque estructurado no inicia con un objeto');

  let depth = 0;
  let inString = false;
  let escaped = false;
  for (let index = start; index < html.length; index += 1) {
    const character = html[index];
    if (inString) {
      if (escaped) escaped = false;
      else if (character === '\\') escaped = true;
      else if (character === '"') inString = false;
      continue;
    }
    if (character === '"') inString = true;
    else if (character === '{') depth += 1;
    else if (character === '}') {
      depth -= 1;
      if (depth === 0) return JSON.parse(html.slice(start, index + 1));
    }
  }
  throw new Error('El bloque estructurado está incompleto');
}


function* walk(value) {
  if (Array.isArray(value)) {
    for (const child of value) yield* walk(child);
  } else if (value && typeof value === 'object') {
    yield value;
    for (const child of Object.values(value)) yield* walk(child);
  }
}


function findFeaturedCard(context) {
  for (const node of walk(context)) {
    const cards = node?.recommendation_info?.polycards;
    if (Array.isArray(cards) && cards.length) return cards[0];
  }
  throw new Error('No se encontró la ficha destacada del producto');
}


function component(card, kind) {
  const entry = (card.components || []).find((candidate) => candidate.type === kind);
  return entry?.[kind] || {};
}


async function fetchOfficialPage(initialUrl, maxRedirects = 10) {
  let current = initialUrl;
  for (let count = 0; count <= maxRedirects; count += 1) {
    if (!isAllowedUrl(current)) throw new Error(`Dominio no permitido: ${current}`);
    const response = await fetch(current, {
      redirect: 'manual',
      headers: { 'user-agent': USER_AGENT, 'accept-language': 'es-MX,es;q=0.9' }
    });
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('location');
      if (!location) throw new Error(`Redirección ${response.status} sin destino`);
      current = new URL(location, current).href;
      continue;
    }
    if (!response.ok) throw new Error(`Mercado Libre respondió ${response.status}`);
    return { html: await response.text(), finalUrl: current };
  }
  throw new Error('Demasiadas redirecciones');
}


export function parsePublicMetrics(text) {
  const rating = text.match(/Calificación\s+([0-5](?:[.,]\d)?)\s+de\s+5\.\s+([\d.,]+)\s+opiniones/i);
  const sold = text.match(/Nuevo\s*\|\s*([^\n|]*vendidos)/i);
  return {
    rating: rating ? Number(rating[1].replace(',', '.')) : null,
    reviews: rating ? Number(rating[2].replace(/[.,]/g, '')) : null,
    sold: sold?.[1]?.trim() || null
  };
}


export function extractReviewSnippet(articleText, limit = 230) {
  const ignored = /^(calificación|méxico$|argentina$|hace\s|útil$|más opciones$|leer más$|\d+$)/i;
  const lines = articleText.split('\n').map((line) => line.trim()).filter((line) => line.length >= 28 && !ignored.test(line));
  if (!lines.length) return null;
  let text = lines.sort((a, b) => b.length - a.length)[0].replace(/\s+/g, ' ');
  if (text.length > limit) text = `${text.slice(0, limit - 1).replace(/\s+\S*$/, '')}…`;
  return text;
}


async function refreshPrice(product, checkedAt) {
  const { html } = await fetchOfficialPage(product.affiliate_url);
  const card = findFeaturedCard(extractAssignedJson(html));
  const metadata = card.metadata || {};
  const price = component(card, 'price');
  const current = price.current_price || {};
  const previous = price.previous_price || {};
  const discountText = price.discount_label?.text || '';
  const discount = discountText.match(/(\d+)%/);
  if (!metadata.id || !current.value) throw new Error('La ficha no contiene ID y precio vigente');
  const { last_price_error: _previousError, ...currentProduct } = product;

  return {
    ...currentProduct,
    id: metadata.id,
    catalog_product_id: metadata.product_id || product.catalog_product_id,
    permalink: canonicalPermalink(metadata, product.permalink),
    price: current.value,
    previous_price: previous.value ?? null,
    currency: current.currency || product.currency || 'MXN',
    discount: discount ? Number(discount[1]) : null,
    image: card.pictures?.pictures?.[0]?.id
      ? `https://http2.mlstatic.com/D_NQ_NP_2X_${card.pictures.pictures[0].id}-F.webp`
      : product.image,
    available: true,
    last_price_check: checkedAt
  };
}


async function mapWithLimit(items, limit, worker) {
  const output = new Array(items.length);
  let next = 0;
  async function run() {
    while (next < items.length) {
      const index = next;
      next += 1;
      output[index] = await worker(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return output;
}


async function main() {
  const catalog = JSON.parse(await readFile(CATALOG_PATH, 'utf8'));
  const checkedAt = new Date().toISOString();
  let priceSuccess = 0;
  const priceErrors = [];

  const priced = await mapWithLimit(catalog.products, 5, async (product) => {
    try {
      const refreshed = await refreshPrice(product, checkedAt);
      priceSuccess += 1;
      return refreshed;
    } catch (error) {
      priceErrors.push(`${product.id}: ${error.message}`);
      return { ...product, available: false, last_price_error: checkedAt };
    }
  });

  if (priceSuccess < Math.ceil(catalog.products.length * 0.75)) {
    throw new Error(`Actualización cancelada: solo ${priceSuccess}/${catalog.products.length} precios válidos`);
  }

  catalog.products = priced;
  catalog.generated_at = checkedAt;
  catalog.sync = {
    price_success: priceSuccess,
    price_total: catalog.products.length,
    buyer_comments: 'editorial_snapshot'
  };
  await writeFile(CATALOG_PATH, `${JSON.stringify(catalog, null, 2)}\n`, 'utf8');
  console.log(`Precios actualizados: ${priceSuccess}/${catalog.products.length}`);
  if (priceErrors.length) console.warn(priceErrors.join('\n'));
}


const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) main().catch((error) => { console.error(error.message); process.exitCode = 1; });
