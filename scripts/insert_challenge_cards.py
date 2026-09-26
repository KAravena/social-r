import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

modules = [
    ("01-empezar-a-pensar-con-r", "intro-r-01-challenge", False),
    ("02-trabajar-con-varios-valores", "intro-r-02-challenge", False),
    ("03-hacer-preguntas-a-los-datos", "intro-r-03-challenge", False),
    ("04-entender-una-base-de-datos", "intro-r-04-challenge", False),
    ("05-seleccionar-y-filtrar-datos", "intro-r-05-challenge", False),
    ("06-trabajar-cuando-faltan-datos", "intro-r-06-challenge", True),
    ("07-describir-categorias", "intro-r-07-challenge", True),
    ("08-describir-cantidades", "intro-r-08-challenge", True),
    ("09-ver-relaciones-entre-dos-cantidades", "intro-r-09-challenge", True),
    ("10-elegir-y-evaluar-una-correlacion", "intro-r-10-challenge", True),
    ("11-trabajar-con-varias-correlaciones", "intro-r-11-challenge", True),
    ("12-relacionar-categorias", "intro-r-12-challenge", True),
    ("13-de-la-pregunta-al-analisis", "intro-r-13-challenge", True),
]

index_path = ROOT / "index.qmd"
content = index_path.read_text(encoding="utf-8")

for mod_slug, challenge_id, is_standby in modules:
    standby_card_class = " sr-challenge-card--standby" if is_standby else ""
    standby_badge_class = " sr-challenge-badge--standby" if is_standby else ""
    status_attr = "standby" if is_standby else "pending"
    status_text = "En preparación" if is_standby else "Disponible al completar el módulo"
    comment = " (Standby)" if is_standby else ""

    card_html = f"""            <!-- Desafío final{comment} -->
            <div class="sr-challenge-card{standby_card_class}" data-challenge-mod="{mod_slug}" data-challenge-id="{challenge_id}">
              <div class="sr-challenge-card__left">
                <div class="sr-challenge-card__eyebrow">
                  <span class="sr-challenge-icon" aria-hidden="true">◇</span>
                  <span class="sr-challenge-label">DESAFÍO FINAL</span>
                </div>
                <div class="sr-challenge-card__desc">Integra lo aprendido en este módulo.</div>
              </div>
              <div class="sr-challenge-card__right">
                <span class="sr-challenge-badge{standby_badge_class}" data-status="{status_attr}">{status_text}</span>
              </div>
            </div>"""

    # Check if card already present
    if f'data-challenge-id="{challenge_id}"' in content:
        print(f"Skipping {challenge_id}, already present")
        continue

    # Find the ul for this module and insert after </ul>
    mod_pattern = re.compile(rf'(data-module-id="{mod_slug}"[\s\S]*?</ul>)', re.MULTILINE)
    match = mod_pattern.search(content)
    if not match:
        print(f"ERROR: could not find module {mod_slug}")
        continue
    replacement = match.group(1) + "\n" + card_html
    content = content[:match.start()] + replacement + content[match.end():]

index_path.write_text(content, encoding="utf-8")
print("Successfully inserted challenge cards into index.qmd!")
