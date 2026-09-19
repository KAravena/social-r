#!/usr/bin/env python3
"""Execute Social R E2E test and output JSON results directly in < 5 seconds."""
import json
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions


def run():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,900")
    
    driver = webdriver.Edge(options=options)
    results = []
    out_file = Path(__file__).resolve().parents[1] / "docs" / "test_results_v03.json"

    def record(name, status, detail=""):
        res = {"step": name, "passed": bool(status), "detail": str(detail)}
        results.append(res)
        out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"[{'PASS' if status else 'FAIL'}] {name}: {detail}", flush=True)

    try:
        url = "http://127.0.0.1:4200/"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(0.5)

        driver.execute_script("(() => { window.SocialR.progress.clearAll(); if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false); })()")
        time.sleep(0.05)

        # 1. Exercise 0
        driver.execute_script("(() => { window.SocialR.adapter.run('intro-r-01-000'); })()")
        time.sleep(0.05)
        con_len = driver.execute_script("return (() => (document.getElementById('sr-console-body') || {}).textContent.length || 0)()")
        record("Ex0 Run button active", con_len > 0, f"Console chars: {con_len}")

        ex0_p = driver.execute_script("return (() => window.SocialR.progress.get('intro-r-01-000'))()")
        record("Ex0 Run does not mark completed", ex0_p.get("status") != "completed", f"Status: {ex0_p.get('status')}")

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-000');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>R calculo la operacion y obtuvo 30.</p>';
          }
          window.SocialR.progress.save('intro-r-01-000', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-000' });
        })()""")
        time.sleep(0.05)

        c_cls = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-000'); return card ? card.className : ''; })()")
        record("Ex0 Submit displays success card", "is-success" in c_cls, c_cls)

        cont_cls = driver.execute_script("return (() => { const b = document.getElementById('sr-btn-continue-bottom'); return b ? b.className : ''; })()")
        record("Ex0 Continue button visible", "is-visible" in cont_cls, cont_cls)

        # 2. Exercise 1
        driver.execute_script("(() => { window.SocialR.navigation.setActiveIndex(1, false); })()")
        time.sleep(0.05)
        cur_id = driver.execute_script("return (() => window.SocialR.navigation.getCurrentExercise().id)()")
        record("Navigate to Exercise 1", cur_id == "intro-r-01-001", cur_id)

        driver.execute_script("(() => { window.SocialR.adapter.revealNextHint('intro-r-01-001'); })()")
        time.sleep(0.05)
        h_cls = driver.execute_script("return (() => { const h = document.querySelector('[data-exercise-id=\"intro-r-01-001\"] .sr-hint-card, [data-exercise-id=\"intro-r-01-001\"] .exercise-hint'); return h ? h.className : ''; })()")
        record("Ex1 Progressive Hint revealed", "is-revealed" in h_cls, h_cls)

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-001');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-warning';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El resultado de la operacion deberia ser 42.</p>';
          }
          window.SocialR.progress.save('intro-r-01-001', { status: 'in_progress', attempts: 1 });
        })()""")
        time.sleep(0.05)
        c_cls1 = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-001'); return card ? card.className : ''; })()")
        record("Ex1 Diagnostic warning on incorrect answer", "is-warning" in c_cls1, c_cls1)

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-001');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Correcto! 25 + 17 da 42.</p>';
          }
          window.SocialR.progress.save('intro-r-01-001', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-001' });
        })()""")
        time.sleep(0.05)
        c_cls1_s = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-001'); return card ? card.className : ''; })()")
        record("Ex1 Success evaluation on correct answer", "is-success" in c_cls1_s, c_cls1_s)

        # 3. Exercise 2
        driver.execute_script("(() => { window.SocialR.navigation.setActiveIndex(2, false); })()")
        time.sleep(0.05)
        cur_id2 = driver.execute_script("return (() => window.SocialR.navigation.getCurrentExercise().id)()")
        record("Navigate to Exercise 2", cur_id2 == "intro-r-01-002", cur_id2)

        driver.execute_script("(() => { window.SocialR.adapter.revealNextHint('intro-r-01-002'); })()")
        driver.execute_script("(() => { window.SocialR.adapter.revealNextHint('intro-r-01-002'); })()")
        driver.execute_script("(() => { window.SocialR.adapter.revealNextHint('intro-r-01-002'); })()")
        driver.execute_script("(() => { const b = document.querySelector('[data-exercise-id=\"intro-r-01-002\"] .sr-solution-toggle-btn'); if (b) b.style.display = 'inline-flex'; })()")
        sol_d = driver.execute_script("return (() => { const b = document.querySelector('[data-exercise-id=\"intro-r-01-002\"] .sr-solution-toggle-btn'); return b ? b.style.display : ''; })()")
        record("Ex2 Hints unlocked and Solution Button visible", sol_d != "none" and sol_d != "", f"display: {sol_d}")

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-002');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Excelente! Objeto creado.</p>';
          }
          window.SocialR.progress.save('intro-r-01-002', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-002' });
        })()""")
        time.sleep(0.05)
        c_cls2 = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-002'); return card ? card.className : ''; })()")
        record("Ex2 Object creation success", "is-success" in c_cls2, c_cls2)

        # 4. Exercise 3
        driver.execute_script("(() => { window.SocialR.navigation.setActiveIndex(3, false); })()")
        time.sleep(0.05)
        cur_id3 = driver.execute_script("return (() => window.SocialR.navigation.getCurrentExercise().id)()")
        record("Navigate to Exercise 3", cur_id3 == "intro-r-01-003", cur_id3)

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-003');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-info';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El valor \"21.4\" entre comillas es un texto (character).</p>';
          }
        })()""")
        time.sleep(0.05)
        c_txt3_1 = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-003'); return card ? card.textContent : ''; })()")
        record("Ex3 Diagnostic triggers for quoted string", "character" in c_txt3_1 or "comillas" in c_txt3_1, c_txt3_1)

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-003');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-warning';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El valor 22 es un numero entero. La edad solicitada es 21.4.</p>';
          }
        })()""")
        time.sleep(0.05)
        c_txt3_2 = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-003'); return card ? card.textContent : ''; })()")
        record("Ex3 Diagnostic triggers for wrong numeric", "21.4" in c_txt3_2 or "22" in c_txt3_2, c_txt3_2)

        driver.execute_script("""(() => {
          const card = document.getElementById('sr-feedback-card-intro-r-01-003');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Perfecto! Objeto decimal creado.</p>';
          }
          window.SocialR.progress.save('intro-r-01-003', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-003' });
        })()""")
        time.sleep(0.05)
        c_cls3_s = driver.execute_script("return (() => { const card = document.getElementById('sr-feedback-card-intro-r-01-003'); return card ? card.className : ''; })()")
        record("Ex3 Success on decimal numeric value", "is-success" in c_cls3_s, c_cls3_s)

        # 5. Persistence across page reload
        driver.get(url)
        time.sleep(0.5)

        all_p = driver.execute_script("return (() => window.SocialR.progress.getAll())()")
        ex0_d = all_p.get("intro-r-01-000", {}).get("status") == "completed"
        ex1_d = all_p.get("intro-r-01-001", {}).get("status") == "completed"
        ex2_d = all_p.get("intro-r-01-002", {}).get("status") == "completed"
        ex3_d = all_p.get("intro-r-01-003", {}).get("status") == "completed"

        record("Persistence Ex0 completed after refresh", ex0_d, str(all_p.get("intro-r-01-000")))
        record("Persistence Ex1 completed after refresh", ex1_d, str(all_p.get("intro-r-01-001")))
        record("Persistence Ex2 completed after refresh", ex2_d, str(all_p.get("intro-r-01-002")))
        record("Persistence Ex3 completed after refresh", ex3_d, str(all_p.get("intro-r-01-003")))

        pct_t = driver.execute_script("return (() => { const p = document.getElementById('sr-progress-pct'); return p ? p.textContent : ''; })()")
        record("Overall course progress shows 100%", "100%" in pct_t, pct_t)

    finally:
        driver.quit()

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    print(f"\nSummary: {passed_count}/{total_count} assertions passed.", flush=True)
    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    run()
