import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.research_products import is_allowed_url


ROOT = Path(__file__).resolve().parents[1]


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.products = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))["products"]

    def test_required_files_exist(self):
        for name in ["index.html", "styles.css", "app.js", "robots.txt", "sitemap.xml", "llms.txt", "vercel.json", "package.json", ".github/workflows/update-catalog.yml"]:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_spanish_mexico_language(self):
        self.assertIn('lang="es-MX"', self.home)

    def test_unique_primary_heading(self):
        self.assertEqual(self.home.count("<h1>"), 1)

    def test_seo_metadata(self):
        for marker in ['name="description"', 'rel="canonical"', 'name="robots"', 'application/ld+json']:
            self.assertIn(marker, self.home)

    def test_real_navigation_links(self):
        for marker in ['href="#categorias"', 'href="#recomendados"', 'href="#metodo"', 'href="#guias"']:
            self.assertIn(marker, self.home)

    def test_affiliate_disclosure_remains_available(self):
        disclosure = (ROOT / "aviso-afiliados.html").read_text(encoding="utf-8")
        self.assertIn("enlaces de afiliado", disclosure)
        self.assertIn('href="/aviso-afiliados.html"', self.home)

    def test_price_claim_is_limited_and_explained(self):
        self.assertIn("no representa todo el mercado", self.home)
        self.assertIn("Una cifra tachada nunca basta", self.home)
        self.assertIn("Precio revisado diariamente", self.home)

    def test_sitemap_is_valid_xml(self):
        ET.parse(ROOT / "sitemap.xml")

    def test_curated_catalog_has_sixteen_products(self):
        self.assertEqual(len(self.products), 16)

    def test_affiliate_links_are_unique_and_preserved(self):
        links = [product["affiliate_url"] for product in self.products]
        self.assertEqual(len(links), len(set(links)))
        self.assertTrue(all(link.startswith("https://meli.la/") for link in links))

    def test_every_product_has_reputation_and_editorial_context(self):
        for product in self.products:
            self.assertGreaterEqual(product["rating"], 4.8)
            self.assertGreater(product["reviews"], 50)
            self.assertGreater(product["price"], 0)
            self.assertTrue(product["reason"])
            self.assertTrue(product["price_signal"])
            self.assertTrue(product["available"])
            self.assertTrue(product["catalog_product_id"].startswith("MLM"))
            self.assertTrue(product["permalink"].startswith("https://www.mercadolibre.com.mx/"))
            self.assertEqual(len(product["review_snippets"]), 2)
            self.assertTrue(all(snippet.strip() for snippet in product["review_snippets"]))

    def test_home_prioritizes_offers(self):
        self.assertLess(self.home.index('id="recomendados"'), self.home.index('id="categorias"'))
        self.assertIn("Productos que convienen hoy", self.home)

    def test_vercel_config_is_valid_json(self):
        data = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertTrue(data["cleanUrls"])

    def test_link_research_accepts_only_official_hosts(self):
        self.assertTrue(is_allowed_url("https://meli.la/abc123"))
        self.assertTrue(is_allowed_url("https://www.mercadolibre.com.mx/producto"))
        self.assertFalse(is_allowed_url("http://meli.la/abc123"))
        self.assertFalse(is_allowed_url("https://meli.la.evil.example/abc123"))
        self.assertFalse(is_allowed_url("https://example.com/producto"))

    def test_daily_workflow_updates_and_validates_catalog(self):
        workflow = (ROOT / ".github" / "workflows" / "update-catalog.yml").read_text(encoding="utf-8")
        self.assertIn('timezone: "America/Cancun"', workflow)
        self.assertIn("npm run update-catalog", workflow)
        self.assertIn("python3 -m unittest", workflow)
        self.assertIn("contents: write", workflow)
        self.assertNotIn("playwright", workflow.lower())

    def test_buyer_comments_have_a_visible_component(self):
        script = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("Lo que dicen compradores", script)
        self.assertIn("review_snippets", script)
        self.assertIn("updateHero(products[0], payload.generated_at)", script)


if __name__ == "__main__":
    unittest.main()
