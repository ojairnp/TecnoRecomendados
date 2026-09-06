const menuButton = document.querySelector('.menu-button');
const menu = document.querySelector('.nav');
const searchForm = document.querySelector('#busqueda-form');
const searchInput = document.querySelector('#busqueda');
const grid = document.querySelector('#product-grid');
const counter = document.querySelector('#contador-productos');

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

function productCard(product) {
  const title = escapeHtml(product.title);
  const image = escapeHtml(product.image);
  const url = escapeHtml(product.affiliate_url);
  const category = escapeHtml(product.category || 'Tecnología');
  const price = new Intl.NumberFormat('es-MX', {
    style: 'currency', currency: product.currency || 'MXN'
  }).format(product.price);
  return `<article class="product-card" data-product="${title.toLowerCase()} ${category.toLowerCase()}">
    <img src="${image}" alt="${title}" loading="lazy">
    <div class="product-body"><p class="product-category">${category}</p><h3>${title}</h3>
    <p class="product-price">${price}</p><a class="product-button" href="${url}" target="_blank" rel="noopener sponsored">Ver en Mercado Libre</a></div>
  </article>`;
}

function filterProducts(query) {
  const term = String(query || '').trim().toLowerCase();
  const cards = [...document.querySelectorAll('[data-product]')];
  if (!cards.length) {
    counter.textContent = term ? `La búsqueda “${query}” estará disponible al agregar productos verificados.` : 'Preparando las primeras recomendaciones verificadas.';
    return;
  }
  let visible = 0;
  cards.forEach((card) => {
    const match = !term || card.dataset.product.includes(term);
    card.classList.toggle('is-hidden', !match);
    if (match) visible += 1;
  });
  counter.textContent = `${visible} producto${visible === 1 ? '' : 's'} encontrado${visible === 1 ? '' : 's'}.`;
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
    counter.textContent = `${products.length} productos verificados disponibles.`;
  } catch (_) {
    counter.textContent = 'El catálogo se actualizará próximamente.';
  }
}

loadProducts();
