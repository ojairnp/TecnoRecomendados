const menuButton = document.querySelector('.menu-button');
const menu = document.querySelector('.nav');
const searchForm = document.querySelector('#busqueda-form');
const searchInput = document.querySelector('#busqueda');
const grid = document.querySelector('#product-grid');
const counter = document.querySelector('#contador-productos');
const updatedAt = document.querySelector('#fecha-actualizacion');

if (menuButton && menu) {
  menuButton.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
  });
}

document.querySelectorAll('[data-search]').forEach((button) => {
  button.addEventListener('click', () => {
    searchInput.value = button.dataset.search;
    filterProducts(button.dataset.search);
    document.querySelector('#recomendados').scrollIntoView({ behavior: 'smooth' });
  });
});

document.querySelectorAll('[data-category]').forEach((link) => {
  link.addEventListener('click', () => filterProducts(link.dataset.category));
});

document.querySelectorAll('[data-offer-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-offer-filter]').forEach((item) => item.classList.remove('is-active'));
    button.classList.add('is-active');
    filterProducts(button.dataset.offerFilter);
  });
});

if (searchForm) {
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    filterProducts(searchInput.value);
    document.querySelector('#recomendados').scrollIntoView({ behavior: 'smooth' });
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function normalize(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function money(value, currency = 'MXN') {
  return new Intl.NumberFormat('es-MX', {
    style: 'currency', currency, maximumFractionDigits: 2
  }).format(value);
}

function productCard(product) {
  const title = escapeHtml(product.title);
  const image = escapeHtml(product.image);
  const url = escapeHtml(product.affiliate_url);
  const category = escapeHtml(product.category || 'Tecnología');
  const seller = escapeHtml(product.seller || 'Vendedor con reputación pública');
  const reason = escapeHtml(product.reason || 'Producto seleccionado por su utilidad y reputación.');
  const signal = escapeHtml(product.price_signal || 'Precio destacado');
  const price = money(product.price, product.currency);
  const previous = product.previous_price
    ? `<span class="previous-price">Antes ${money(product.previous_price, product.currency)}</span>`
    : '';
  const discount = product.discount
    ? `<span class="discount-badge">-${Number(product.discount)}%</span>`
    : '';
  const official = product.official_store
    ? '<span class="official-badge">Tienda verificada</span>'
    : '';
  const reviews = new Intl.NumberFormat('es-MX').format(product.reviews || 0);
  const searchable = normalize(`${product.title} ${product.category} ${product.seller} ${product.price_signal}`);
  return `<article class="product-card" data-product="${escapeHtml(searchable)}" data-best="${signal.includes('Mejor')}">
    <div class="product-image-wrap">
      <img src="${image}" alt="${title}" loading="lazy" width="480" height="480">
      <div class="product-badges"><span class="signal-badge">${signal}</span>${discount}</div>
    </div>
    <div class="product-body">
      <div class="product-meta"><p class="product-category">${category}</p>${official}</div>
      <h3>${title}</h3>
      <p class="product-rating" aria-label="Calificación ${product.rating} de 5 con ${reviews} opiniones"><span>★ ${product.rating}</span><b>${reviews} opiniones</b><i>· ${escapeHtml(product.sold || '')}</i></p>
      <p class="product-reason">${reason}</p>
      <p class="product-seller">${seller}</p>
      <div class="price-row"><p class="product-price">${price}</p>${previous}</div>
      <a class="product-button" href="${url}" target="_blank" rel="noopener sponsored">Ver oferta en Mercado Libre <span>→</span></a>
      <small>Precio y disponibilidad pueden cambiar al abrir la oferta.</small>
    </div>
  </article>`;
}

function filterProducts(query) {
  const term = normalize(query).trim();
  const cards = [...document.querySelectorAll('[data-product]')];
  if (!cards.length) {
    counter.textContent = term ? `La búsqueda “${query}” estará disponible al agregar productos verificados.` : 'Preparando las primeras recomendaciones verificadas.';
    return;
  }
  let visible = 0;
  cards.forEach((card) => {
    const match = !term || term === 'todos' ||
      (term === 'mejor-precio' ? card.dataset.best === 'true' : card.dataset.product.includes(term));
    card.classList.toggle('is-hidden', !match);
    if (match) visible += 1;
  });
  counter.textContent = `${visible} producto${visible === 1 ? '' : 's'} encontrado${visible === 1 ? '' : 's'}.`;
}

function addProductStructuredData(products) {
  const existing = document.querySelector('#product-structured-data');
  if (existing) existing.remove();
  const script = document.createElement('script');
  script.id = 'product-structured-data';
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    itemListElement: products.map((product, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      item: {
        '@type': 'Product',
        name: product.title,
        image: product.image,
        description: product.reason,
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: product.rating,
          reviewCount: product.reviews
        },
        offers: {
          '@type': 'Offer',
          url: product.affiliate_url,
          priceCurrency: product.currency || 'MXN',
          price: product.price,
          availability: 'https://schema.org/InStock'
        }
      }
    }))
  });
  document.head.appendChild(script);
}

async function loadProducts() {
  try {
    const response = await fetch('/data/products.json', { cache: 'no-store' });
    if (!response.ok) return;
    const payload = await response.json();
    const products = Array.isArray(payload.products)
      ? payload.products.filter((product) => product.available && product.affiliate_url)
      : [];
    if (!products.length) return;
    grid.innerHTML = products.map(productCard).join('');
    counter.textContent = `${products.length} oportunidades con reputación comprobada.`;
    if (updatedAt && payload.generated_at) {
      updatedAt.textContent = new Intl.DateTimeFormat('es-MX', {
        dateStyle: 'long', timeZone: 'America/Cancun'
      }).format(new Date(payload.generated_at));
    }
    addProductStructuredData(products);
  } catch (_) {
    counter.textContent = 'El catálogo se actualizará próximamente.';
  }
}

loadProducts();
