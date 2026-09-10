import test from 'node:test';
import assert from 'node:assert/strict';

import { canonicalPermalink, extractAssignedJson, extractReviewSnippet, isAllowedUrl, parsePublicMetrics } from '../scripts/update_catalog.mjs';


test('solo permite enlaces HTTPS oficiales', () => {
  assert.equal(isAllowedUrl('https://meli.la/abc123'), true);
  assert.equal(isAllowedUrl('https://www.mercadolibre.com.mx/p/MLM1'), true);
  assert.equal(isAllowedUrl('http://meli.la/abc123'), false);
  assert.equal(isAllowedUrl('https://meli.la.evil.example/x'), false);
});

test('extrae el objeto asignado sin consumir el JavaScript posterior', () => {
  const html = '<script>_n.ctx.r={"text":"llave } segura","ok":true};otra.cosa=1;</script>';
  assert.deepEqual(extractAssignedJson(html), { text: 'llave } segura', ok: true });
});

test('extrae calificación, opiniones y ventas del texto público', () => {
  const text = 'Nuevo | +10 mil vendidos\nCalificación 4.9 de 5. 59,576 opiniones.';
  assert.deepEqual(parsePublicMetrics(text), { rating: 4.9, reviews: 59576, sold: '+10 mil vendidos' });
});

test('elimina metadatos y limita el comentario público', () => {
  const text = 'Calificación 5 de 5\nMéxico\nHace 2 meses\nExcelente producto, funciona muy bien y llegó en perfectas condiciones.';
  assert.equal(extractReviewSnippet(text), 'Excelente producto, funciona muy bien y llegó en perfectas condiciones.');
});

test('normaliza permalinks alternos al producto oficial', () => {
  const fallback = 'https://www.mercadolibre.com.mx/p/MLM48590241';
  assert.equal(
    canonicalPermalink({ url: 'articulo.mercadolibre.com.mx/MLM-123-producto-_JM', product_id: 'MLM48590241' }, fallback),
    fallback,
  );
  assert.equal(
    canonicalPermalink({ url: 'www.mercadolibre.com.mx/producto/p/MLM123', product_id: 'MLM123' }, fallback),
    'https://www.mercadolibre.com.mx/producto/p/MLM123',
  );
});
