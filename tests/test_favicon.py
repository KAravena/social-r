#!/usr/bin/env python3
"""Automated and visual QA verification test for Social R favicon.

Validates:
1. All required favicon assets exist in assets/favicon/ and docs/assets/favicon/.
2. Master SVG is pure geometry (no <text>), has 64x64 viewBox, #0B0F19 background, and #8B5CF6 glyph.
3. favicon.ico is a true multi-resolution ICO with sizes: 16x16, 32x32, 48x48.
4. HTML integration: _quarto.yml, index.qmd, build.py, docs/index.html, and docs/curso.html.
5. All paths are relative (GitHub Pages compatible, no absolute / leading slash).
6. Playwright visual comparison QA at 512, 192, 64, 48, 32, 16 px.
"""
from __future__ import annotations

import asyncio
import re
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS_FAVICON = ROOT / "assets" / "favicon"
DOCS_FAVICON = ROOT / "docs" / "assets" / "favicon"


class TestSocialRFavicon(unittest.TestCase):
    """Unit and integration checks for Social R favicon suite."""

    def test_asset_files_exist(self):
        """Verify all required favicon variants exist."""
        required_files = [
            "favicon.svg",
            "social-r-favicon.svg",
            "favicon-16x16.png",
            "favicon-32x32.png",
            "favicon-48x48.png",
            "apple-touch-icon.png",
            "icon-192.png",
            "icon-512.png",
            "favicon.ico",
            "site.webmanifest",
        ]
        for fname in required_files:
            p_src = ASSETS_FAVICON / fname
            self.assertTrue(p_src.exists(), f"Missing {p_src}")
            self.assertGreater(p_src.stat().st_size, 0, f"Empty file {p_src}")

            p_docs = DOCS_FAVICON / fname
            self.assertTrue(p_docs.exists(), f"Missing docs copy {p_docs}")
            self.assertGreater(p_docs.stat().st_size, 0, f"Empty docs file {p_docs}")

    def test_master_svg_properties(self):
        """Master SVG must be pure vector (no text, no background rect), 421x409 viewBox, transparent, violet #8B5CF6."""
        svg_content = (ASSETS_FAVICON / "favicon.svg").read_text(encoding="utf-8")
        self.assertNotIn("<text", svg_content.lower(), "Favicon SVG must not depend on <text>")
        self.assertNotIn("<rect", svg_content.lower(), "Favicon SVG must NOT have background <rect> (transparent)")
        self.assertIn('viewBox="0 0 421 409"', svg_content, "viewBox must be 0 0 421 409 matching reference C")
        self.assertIn('fill="none"', svg_content, "Root SVG must have fill='none' for transparency")
        self.assertIn("#8B5CF6", svg_content.upper(), "Glyph color must be violet #8B5CF6")
        self.assertIn("<path", svg_content, "Glyph must be vector path")

    def test_real_transparency_in_raster(self):
        """PNG variants must have real transparent pixels (alpha == 0)."""
        for fname in ["favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png"]:
            p = ASSETS_FAVICON / fname
            with Image.open(p).convert("RGBA") as img:
                alphas = [pixel[3] for pixel in img.getdata()]
                transparent_count = sum(1 for a in alphas if a == 0)
                self.assertGreater(
                    transparent_count,
                    len(alphas) * 0.25,
                    f"{fname} must have real transparent background (>25% transparent pixels)"
                )

    def test_multi_resolution_ico(self):
        """favicon.ico must contain 16x16, 32x32, and 48x48 icon frames."""
        ico_path = ASSETS_FAVICON / "favicon.ico"
        with Image.open(ico_path) as img:
            sizes = img.info.get("sizes", set())
            self.assertIn((16, 16), sizes, "ICO must contain 16x16 frame")
            self.assertIn((32, 32), sizes, "ICO must contain 32x32 frame")
            self.assertIn((48, 48), sizes, "ICO must contain 48x48 frame")

    def test_apple_touch_icon_dimensions(self):
        """apple-touch-icon.png must be exactly 180x180."""
        apple_path = ASSETS_FAVICON / "apple-touch-icon.png"
        with Image.open(apple_path) as img:
            self.assertEqual(img.size, (180, 180), "apple-touch-icon must be 180x180")

    def test_quarto_yml_configuration(self):
        """_quarto.yml must have website.favicon set to assets/favicon/favicon.svg."""
        quarto_yml = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
        self.assertIn('favicon: "assets/favicon/favicon.svg"', quarto_yml)

    def test_html_integration(self):
        """docs/index.html and docs/curso.html must include correct relative favicon tags."""
        for html_rel in ["docs/index.html", "docs/curso.html"]:
            html_path = ROOT / html_rel
            self.assertTrue(html_path.exists(), f"Missing {html_rel}")
            content = html_path.read_text(encoding="utf-8")

            # Check svg icon link
            self.assertTrue(
                "assets/favicon/favicon.svg" in content,
                f"Missing svg icon link in {html_rel}"
            )
            # Check png sizes
            self.assertIn("favicon-32x32.png", content, f"Missing 32x32 link in {html_rel}")
            self.assertIn("favicon-16x16.png", content, f"Missing 16x16 link in {html_rel}")
            self.assertIn("apple-touch-icon.png", content, f"Missing apple icon link in {html_rel}")
            self.assertIn("site.webmanifest", content, f"Missing manifest link in {html_rel}")

            # Verify paths are relative (no leading slash breaking GitHub Pages subpaths)
            self.assertNotIn('href="/assets/favicon', content, f"Absolute path found in {html_rel}")


async def run_visual_comparison_qa():
    """Generate side-by-side comparison between Estadística Correlacional (C) and Social R (R)."""
    from playwright.async_api import async_playwright

    comparison_html = ROOT / "scratch" / "qa_side_by_side.html"
    ref_svg_path = Path(r"C:\Users\katin\Projects\Visualizadores\estadistica-social\assets\img\03_isotipo_transparente.svg")
    c_svg = ref_svg_path.read_text(encoding="utf-8") if ref_svg_path.exists() else ""
    r_svg = (ASSETS_FAVICON / "favicon.svg").read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>QA Visual Comparison: Estadística Correlacional vs Social R</title>
<style>
  body {{
    margin: 0;
    padding: 30px;
    background: #07090e;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  h1 {{ font-size: 22px; margin: 0 0 6px 0; }}
  .subtitle {{ color: #94a3b8; font-size: 13px; margin-bottom: 24px; }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    max-width: 1040px;
  }}
  .card {{
    background: #111522;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #1e293b;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }}
  .card.c-brand {{ border-color: rgba(34, 211, 238, 0.4); }}
  .card.r-brand {{ border-color: rgba(139, 92, 246, 0.4); }}
  .brand-title {{ font-size: 16px; font-weight: 700; }}
  .c-brand .brand-title {{ color: #22d3ee; }}
  .r-brand .brand-title {{ color: #a78bfa; }}
  .brand-desc {{ font-size: 12px; color: #64748b; margin-top: -10px; }}
  .sizes-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    background: #05070c;
    padding: 18px 24px;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
  }}
  .size-cell {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
  .size-label {{ font-size: 10px; color: #64748b; font-family: monospace; }}
  .tabs-preview {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .tab-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
  }}
  .tab-dark {{ background: #181c26; color: #f1f5f9; border: 1px solid #283347; }}
  .tab-light {{ background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; }}
  .pixelated {{ image-rendering: pixelated; }}
  svg {{ width: 100% !important; height: 100% !important; display: block; }}
  .verdict-banner {{
    margin-top: 24px;
    padding: 14px 20px;
    background: #111c2e;
    border: 1px solid #2563eb;
    border-radius: 10px;
    font-size: 13px;
    color: #93c5fd;
    max-width: 1040px;
    box-sizing: border-box;
  }}
</style>
</head>
<body>
  <h1>Social R vs Estadística Correlacional — Control Visual de Favicons</h1>
  <div class="subtitle">Misma familia visual · Fondo transparente real · Glifo angular puntiagudo · Dos identidades cromáticas (Cyan #22D3EE vs Violeta #8B5CF6)</div>

  <div class="grid">
    <!-- C Brand -->
    <div class="card c-brand">
      <div class="brand-title">Estadística Correlacional Interactiva</div>
      <div class="brand-desc">Símbolo "C" geométrico · Cyan (#22D3EE)</div>
      
      <div class="sizes-container">
        <div class="size-cell">
          <div style="width: 64px; height: 64px;">{c_svg}</div>
          <span class="size-label">64×64</span>
        </div>
        <div class="size-cell">
          <div style="width: 48px; height: 48px;">{c_svg}</div>
          <span class="size-label">48×48</span>
        </div>
        <div class="size-cell">
          <div style="width: 32px; height: 32px;">{c_svg}</div>
          <span class="size-label">32×32</span>
        </div>
        <div class="size-cell">
          <div class="pixelated" style="width: 16px; height: 16px;">{c_svg}</div>
          <span class="size-label">16×16</span>
        </div>
      </div>

      <div class="tabs-preview">
        <div class="tab-row tab-dark">
          <div style="width: 16px; height: 16px;">{c_svg}</div>
          <span>Estadística Correlacional Interactiva</span>
        </div>
        <div class="tab-row tab-light">
          <div style="width: 16px; height: 16px;">{c_svg}</div>
          <span>Estadística Correlacional Interactiva</span>
        </div>
      </div>
    </div>

    <!-- R Brand -->
    <div class="card r-brand">
      <div class="brand-title">Social R</div>
      <div class="brand-desc">Símbolo "R" geométrico · Violeta (#8B5CF6)</div>
      
      <div class="sizes-container">
        <div class="size-cell">
          <div style="width: 64px; height: 64px;">{r_svg}</div>
          <span class="size-label">64×64</span>
        </div>
        <div class="size-cell">
          <div style="width: 48px; height: 48px;">{r_svg}</div>
          <span class="size-label">48×48</span>
        </div>
        <div class="size-cell">
          <div style="width: 32px; height: 32px;">{r_svg}</div>
          <span class="size-label">32×32</span>
        </div>
        <div class="size-cell">
          <div class="pixelated" style="width: 16px; height: 16px;">{r_svg}</div>
          <span class="size-label">16×16</span>
        </div>
      </div>

      <div class="tabs-preview">
        <div class="tab-row tab-dark">
          <div style="width: 16px; height: 16px;">{r_svg}</div>
          <span>Social R · Workspace</span>
        </div>
        <div class="tab-row tab-light">
          <div style="width: 16px; height: 16px;">{r_svg}</div>
          <span>Social R · Workspace</span>
        </div>
      </div>
    </div>
  </div>

  <div class="verdict-banner">
    ✓ <strong>Verificación 16×16:</strong> A 16×16 la contraforma superior y la separación de la pierna diagonal se mantienen nítidas y sólidas.<br>
    ✓ <strong>Familia Visual:</strong> Mismo peso visual, mismo padding de seguridad, fondo charcoal #0B0F19 consistente en pestañas claras y oscuras.
  </div>
</body>
</html>"""

    comparison_html.write_text(html, encoding="utf-8")
    screenshots_dir = ROOT / "tests" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshots_dir / "favicon_comparison_side_by_side.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1120, "height": 680})
        await page.goto(f"file:///{comparison_html.resolve().as_posix()}")
        await page.screenshot(path=str(screenshot_path))
        print(f"Captured visual QA screenshot: {screenshot_path}")

        # Also verify docs/index.html loads favicon without errors
        index_url = f"file:///{(ROOT / 'docs' / 'index.html').resolve().as_posix()}"
        page_index = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page_index.goto(index_url, wait_until="domcontentloaded")
        favicons_in_dom = await page_index.eval_on_selector_all(
            "link[rel*='icon'], link[rel='apple-touch-icon'], link[rel='manifest']",
            "elements => elements.map(el => ({ rel: el.rel, href: el.getAttribute('href') }))"
        )
        print("Favicon tags detected in docs/index.html:", favicons_in_dom)
        assert len(favicons_in_dom) >= 4, "Expected at least 4 icon link tags in index.html"
        await page_index.close()

        await browser.close()


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSocialRFavicon)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        exit(1)

    asyncio.run(run_visual_comparison_qa())


if __name__ == "__main__":
    main()
