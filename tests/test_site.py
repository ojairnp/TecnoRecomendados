import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_required_files_exist(self):
        for name in ["index.html", "styles.css", "app.js", "robots.txt", "sitemap.xml", "llms.txt", "vercel.json"]:
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

    def test_affiliate_disclosure_is_visible(self):
        self.assertIn("Algunos enlaces serán de afiliado", self.home)

    def test_no_fake_product_claims(self):
        self.assertIn("No mostramos precios inventados", self.home)

    def test_sitemap_is_valid_xml(self):
        ET.parse(ROOT / "sitemap.xml")

    def test_products_start_empty(self):
        data = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
        self.assertEqual(data["products"], [])

    def test_vercel_config_is_valid_json(self):
        data = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertTrue(data["cleanUrls"])


if __name__ == "__main__":
    unittest.main()
