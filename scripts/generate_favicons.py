"""Script to generate all Social R favicon assets from the geometric master SVG.

Generates:
- assets/favicon/favicon.svg (Master 64x64 SVG)
- assets/favicon/social-r-favicon.svg (Identical master copy)
- assets/favicon/favicon-16x16.png
- assets/favicon/favicon-32x32.png
- assets/favicon/favicon-48x48.png
- assets/favicon/apple-touch-icon.png (180x180)
- assets/favicon/icon-192.png (192x192)
- assets/favicon/icon-512.png (512x512)
- assets/favicon/favicon.ico (Multi-size ICO: 16x16, 32x32, 48x48)
- assets/favicon/site.webmanifest
"""
import asyncio
import json
import shutil
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS_FAVICON = ROOT / "assets" / "favicon"
DOCS_FAVICON = ROOT / "docs" / "assets" / "favicon"

# Angular Pointy Geometric R Glyph Master SVG (421x409 native space matching C)
# Visual language: Sibling to Estadística Correlacional 'C'
# Background: 100% TRANSPARENT (no rect, no fake background)
# Fill: Electric Violet #8B5CF6 (sharp angular cuts, beveled remates, ramp foot)

R_PATH = "M 75 35 L 30 80 L 30 355 C 30 368 40 375 55 375 L 105 375 C 118 375 122 368 122 355 L 122 225 L 215 225 L 305 352 C 315 366 328 372 345 372 L 396 352 C 404 348 405 338 397 328 L 312 212 C 358 196 391 158 391 108 L 391 65 L 355 35 Z M 122 96 L 305 96 L 334 125 L 305 154 L 122 154 Z"

MASTER_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 421 409" fill="none" shape-rendering="geometricPrecision">
  <path fill-rule="evenodd" d="{R_PATH}" fill="#8B5CF6"/>
</svg>
"""

APPLE_SVG = MASTER_SVG

MANIFEST_DATA = {
    "name": "Social R — Introducción interactiva a R",
    "short_name": "Social R",
    "description": "Plataforma interactiva para aprender R en Ciencias Sociales",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "#0B0F19",
    "theme_color": "#8B5CF6",
    "icons": [
        {
            "src": "favicon-16x16.png",
            "sizes": "16x16",
            "type": "image/png"
        },
        {
            "src": "favicon-32x32.png",
            "sizes": "32x32",
            "type": "image/png"
        },
        {
            "src": "favicon-48x48.png",
            "sizes": "48x48",
            "type": "image/png"
        },
        {
            "src": "icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

async def generate():
    ASSETS_FAVICON.mkdir(parents=True, exist_ok=True)
    DOCS_FAVICON.mkdir(parents=True, exist_ok=True)

    # 1. Write SVGs
    svg_file = ASSETS_FAVICON / "favicon.svg"
    svg_file.write_text(MASTER_SVG, encoding="utf-8")
    shutil.copyfile(svg_file, ASSETS_FAVICON / "social-r-favicon.svg")
    print(f"Generated {svg_file}")

    # Write manifest
    manifest_file = ASSETS_FAVICON / "site.webmanifest"
    manifest_file.write_text(json.dumps(MANIFEST_DATA, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {manifest_file}")

    # Temporary HTML pages to render with Playwright at crisp resolutions
    temp_dir = ROOT / "scratch"
    temp_dir.mkdir(exist_ok=True)
    temp_html = temp_dir / "favicon_render.html"
    temp_apple_html = temp_dir / "favicon_apple_render.html"

    temp_html.write_text(f"""<!DOCTYPE html><html><head><style>html, body {{ margin:0; padding:0; overflow:hidden; width:100%; height:100%; background:transparent; }} svg {{ width:100%; height:100%; display:block; }}</style></head><body>{MASTER_SVG}</body></html>""", encoding="utf-8")
    temp_apple_html.write_text(f"""<!DOCTYPE html><html><head><style>html, body {{ margin:0; padding:0; overflow:hidden; width:100%; height:100%; background:transparent; }} svg {{ width:100%; height:100%; display:block; }}</style></head><body>{APPLE_SVG}</body></html>""", encoding="utf-8")

    sizes = [
        (16, "favicon-16x16.png", temp_html),
        (32, "favicon-32x32.png", temp_html),
        (48, "favicon-48x48.png", temp_html),
        (180, "apple-touch-icon.png", temp_apple_html),
        (192, "icon-192.png", temp_html),
        (512, "icon-512.png", temp_html),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for size, filename, html_path in sizes:
            page = await browser.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
            await page.goto(f"file:///{html_path.resolve().as_posix()}")
            target = ASSETS_FAVICON / filename
            await page.screenshot(path=str(target), omit_background=True)
            print(f"Rendered {filename} ({size}x{size})")
            await page.close()
        await browser.close()

    # Create multi-resolution ICO file using Pillow
    img16 = Image.open(ASSETS_FAVICON / "favicon-16x16.png").convert("RGBA")
    img32 = Image.open(ASSETS_FAVICON / "favicon-32x32.png").convert("RGBA")
    img48 = Image.open(ASSETS_FAVICON / "favicon-48x48.png").convert("RGBA")

    ico_path = ASSETS_FAVICON / "favicon.ico"
    img48.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=[img16, img32]
    )
    print(f"Generated multi-resolution ICO at {ico_path} with sizes 16x16, 32x32, 48x48")

    # Copy all generated assets to docs/assets/favicon/ and root/docs root for maximum fallback
    for item in ASSETS_FAVICON.iterdir():
        if item.is_file():
            shutil.copyfile(item, DOCS_FAVICON / item.name)

    # Also place favicon.ico in root and docs/
    shutil.copyfile(ico_path, ROOT / "favicon.ico")
    shutil.copyfile(ico_path, ROOT / "docs" / "favicon.ico")
    shutil.copyfile(svg_file, ROOT / "favicon.svg")
    shutil.copyfile(svg_file, ROOT / "docs" / "favicon.svg")

    print("\nAll Favicon Assets Successfully Generated and Synced to docs/!")

if __name__ == "__main__":
    asyncio.run(generate())
