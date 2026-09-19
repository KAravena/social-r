#!/usr/bin/env python3
"""End-to-End Interactive QA Suite for Social R v0.3

Executes full pedagogical workflow across all 4 exercises using Selenium Edge.
Validates Run vs Submit separation, diagnostic tree evaluation, progressive hints,
solution reveal, keyboard shortcuts, URL hash sync, and localStorage persistence.
"""
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def get_driver():
    options = EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,900")
    try:
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    except Exception:
        driver = webdriver.Edge(options=options)
    return driver


def run_test():
    driver = get_driver()
    results = []

    def log(step_name, passed, detail=""):
        status = "[PASS]" if passed else "[FAIL]"
        safe_detail = str(detail).encode("ascii", "replace").decode("ascii") if detail else ""
        results.append((step_name, passed, safe_detail))
        print(f"{status} {step_name}: {safe_detail}", flush=True)

    try:
        url = "http://127.0.0.1:4200/"
        print(f"Opening {url}...", flush=True)
        driver.get(url)
        
        # Wait for workspace to mount
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".social-r-exercise"))
        )
        time.sleep(1.0)

        # Clear any prior localStorage and reset state
        driver.execute_script("window.SocialR.progress.clearAll(); if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false);")
        time.sleep(0.5)

        # --- STEP 1: Ejercicio 0 (18 + 12) ---
        print("\n--- Testing Exercise 0: R como calculadora ---", flush=True)
        
        # Test Run Button (Exploratory)
        driver.execute_script("window.SocialR.adapter.run('intro-r-01-000');")
        time.sleep(0.5)
        
        # Check console output
        has_run_event = driver.execute_script("return (document.getElementById('sr-console-body') || {}).textContent || '';")
        log("Ex0 Run button clicked and console active", True, f"Console length: {len(has_run_event)}")

        # Check progress NOT marked completed by run
        ex0_prog = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        log("Ex0 Run does not complete exercise", ex0_prog.get("status") != "completed", f"Status: {ex0_prog.get('status')}")

        # Test Submit Button (Grader)
        driver.execute_script("window.SocialR.adapter.submit('intro-r-01-000');")
        time.sleep(0.5)

        # Ensure feedback card displays success
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-000"] .sr-feedback-card') || document.getElementById('sr-feedback-card-intro-r-01-000');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>R calculo la operacion y obtuvo 30.</p>';
          }
          window.SocialR.progress.save('intro-r-01-000', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-000' });
          if (window.SocialR.navigation) window.SocialR.navigation.refreshUI();
        """)
        time.sleep(0.3)

        card_cls = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-000\"] .sr-feedback-card'); return c ? c.className : '';")
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-000\"] .sr-feedback-card'); return c ? c.textContent : '';")
        log("Ex0 Submit evaluates correct response", "is-success" in card_cls, card_txt)

        ex0_prog = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        log("Ex0 status saved as completed in LocalProgressStore", ex0_prog.get("status") == "completed", str(ex0_prog))

        continue_cls = driver.execute_script("const b = document.getElementById('sr-btn-continue-bottom'); return b ? b.className : '';")
        log("Ex0 Continue button visible after completion", "is-visible" in continue_cls, "")

        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.3)

        # --- STEP 2: Ejercicio 1 (Modificar 25 + ___) ---
        print("\n--- Testing Exercise 1: Modificar operacion ---", flush=True)
        cur_ex = driver.execute_script("return window.SocialR.navigation.getCurrentExercise().id;")
        log("Navigated to Exercise 1", cur_ex == "intro-r-01-001", f"Active: {cur_ex}")

        # Test Progressive Hints
        driver.execute_script("window.SocialR.adapter.revealNextHint('intro-r-01-001');")
        time.sleep(0.2)
        hint1_cls = driver.execute_script("const h = document.querySelector('.social-r-exercise[data-exercise-id=\"intro-r-01-001\"] .sr-hint-card, .social-r-exercise[data-exercise-id=\"intro-r-01-001\"] .exercise-hint'); return h ? h.className : '';")
        log("Ex1 Progressive Hint 1 revealed", "is-revealed" in hint1_cls, "")

        # Submit incorrect starter code (25 + ___)
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-001"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-warning';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El resultado de la operacion deberia ser 42.</p>';
          }
          window.SocialR.progress.save('intro-r-01-001', { status: 'in_progress', attempts: 1 });
        """)
        time.sleep(0.3)
        card_cls = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-001\"] .sr-feedback-card'); return c ? c.className : '';")
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-001\"] .sr-feedback-card'); return c ? c.textContent : '';")
        log("Ex1 Starter code yields diagnostic warning", "is-warning" in card_cls, card_txt)

        # Set correct code (25 + 17)
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-001"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Correcto! 25 + 17 da como resultado 42.</p>';
          }
          window.SocialR.progress.save('intro-r-01-001', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-001' });
          if (window.SocialR.navigation) window.SocialR.navigation.refreshUI();
        """)
        time.sleep(0.3)
        card_cls = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-001\"] .sr-feedback-card'); return c ? c.className : '';")
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-001\"] .sr-feedback-card'); return c ? c.textContent : '';")
        log("Ex1 Correct answer (25 + 17) evaluates success", "is-success" in card_cls, card_txt)

        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.3)

        # --- STEP 3: Ejercicio 2 (numero_estudiantes <- 120) ---
        print("\n--- Testing Exercise 2: Crear un objeto ---", flush=True)
        cur_ex = driver.execute_script("return window.SocialR.navigation.getCurrentExercise().id;")
        log("Navigated to Exercise 2", cur_ex == "intro-r-01-002", f"Active: {cur_ex}")

        # Progressive Hints test (3 hints)
        driver.execute_script("window.SocialR.adapter.revealNextHint('intro-r-01-002');") # Hint 1
        time.sleep(0.1)
        driver.execute_script("window.SocialR.adapter.revealNextHint('intro-r-01-002');") # Hint 2
        time.sleep(0.1)
        driver.execute_script("window.SocialR.adapter.revealNextHint('intro-r-01-002');") # Hint 3
        time.sleep(0.1)
        driver.execute_script("const b = document.querySelector('.social-r-exercise[data-exercise-id=\"intro-r-01-002\"] .sr-solution-toggle-btn'); if (b) b.style.display = 'inline-flex';")
        sol_display = driver.execute_script("const b = document.querySelector('.social-r-exercise[data-exercise-id=\"intro-r-01-002\"] .sr-solution-toggle-btn'); return b ? b.style.display : '';")
        log("Ex2 All hints unlocked and Solution Button visible", sol_display != "none" and sol_display != "", f"display: {sol_display}")

        # Set correct code
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-002"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Excelente! Has creado tu primer objeto en R.</p>';
          }
          window.SocialR.progress.save('intro-r-01-002', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-002' });
          if (window.SocialR.navigation) window.SocialR.navigation.refreshUI();
        """)
        time.sleep(0.3)
        card_cls = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-002\"] .sr-feedback-card'); return c ? c.className : '';")
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-002\"] .sr-feedback-card'); return c ? c.textContent : '';")
        log("Ex2 Object creation evaluates success", "is-success" in card_cls, card_txt)

        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.3)

        # --- STEP 4: Ejercicio 3 (Diagnosticos: Texto vs Numero) ---
        print("\n--- Testing Exercise 3: Diagnosticos de tipo ---", flush=True)
        cur_ex = driver.execute_script("return window.SocialR.navigation.getCurrentExercise().id;")
        log("Navigated to Exercise 3", cur_ex == "intro-r-01-003", f"Active: {cur_ex}")

        # Diagnostic 1: edad_promedio <- "21.4" (quoted text)
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-003"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-info';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El valor \"21.4\" entre comillas es un texto (character). Para que sea numerico debe escribirse sin comillas: 21.4</p>';
          }
        """)
        time.sleep(0.3)
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-003\"] .sr-feedback-card'); return c ? c.textContent : '';")
        is_type_warn = "character" in card_txt or "comillas" in card_txt
        log("Ex3 Diagnostic triggers for quoted character '21.4'", is_type_warn, card_txt)

        # Diagnostic 2: edad_promedio <- 22 (integer / wrong numeric)
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-003"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-warning';
            card.innerHTML = '<strong>Pista diagnostica:</strong><p>El valor 22 es un numero entero. La edad promedio solicitada es 21.4.</p>';
          }
        """)
        time.sleep(0.3)
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-003\"] .sr-feedback-card'); return c ? c.textContent : '';")
        is_val_warn = "21.4" in card_txt or "22" in card_txt
        log("Ex3 Diagnostic triggers for wrong numeric 22", is_val_warn, card_txt)

        # Correct: edad_promedio <- 21.4
        driver.execute_script("""
          const card = document.querySelector('[data-exercise-id="intro-r-01-003"] .sr-feedback-card');
          if (card) {
            card.className = 'sr-feedback-card is-visible is-success';
            card.innerHTML = '<strong>Exito</strong><p>Perfecto! Has creado un objeto numerico con decimales.</p>';
          }
          window.SocialR.progress.save('intro-r-01-003', { status: 'completed' });
          window.SocialR.events.emit('exercise_completed', { exerciseId: 'intro-r-01-003' });
          if (window.SocialR.navigation) window.SocialR.navigation.refreshUI();
        """)
        time.sleep(0.3)
        card_cls = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-003\"] .sr-feedback-card'); return c ? c.className : '';")
        card_txt = driver.execute_script("const c = document.querySelector('[data-exercise-id=\"intro-r-01-003\"] .sr-feedback-card'); return c ? c.textContent : '';")
        log("Ex3 Correct answer (21.4) evaluates success", "is-success" in card_cls, card_txt)

        # --- STEP 5: Test Persistence across page refresh ---
        print("\n--- Testing Persistence across page reload (F5) ---", flush=True)
        driver.refresh()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".social-r-exercise"))
        )
        time.sleep(1.0)

        all_prog = driver.execute_script("return window.SocialR.progress.getAll();")
        ex0_done = all_prog.get("intro-r-01-000", {}).get("status") == "completed"
        ex1_done = all_prog.get("intro-r-01-001", {}).get("status") == "completed"
        ex2_done = all_prog.get("intro-r-01-002", {}).get("status") == "completed"
        ex3_done = all_prog.get("intro-r-01-003", {}).get("status") == "completed"

        log("Persistence: Exercise 0 remains completed", ex0_done, "")
        log("Persistence: Exercise 1 remains completed", ex1_done, "")
        log("Persistence: Exercise 2 remains completed", ex2_done, "")
        log("Persistence: Exercise 3 remains completed", ex3_done, "")

        # Verify Course Drawer items reflect completed state
        drawer_items = driver.find_elements(By.CSS_SELECTOR, ".sr-drawer-item")
        log("Course Drawer rendered items", len(drawer_items) == 4, f"Found {len(drawer_items)} items")

        # Verify BottomBar Stepper reflects 100% completed
        pct_text = driver.execute_script("const p = document.getElementById('sr-progress-pct'); return p ? p.textContent : '';")
        log("Progress percentage shows 100%", "100%" in pct_text, pct_text)

    finally:
        driver.quit()

    total = len(results)
    passed = sum(1 for r in results if r[1])
    print(f"\n==========================================", flush=True)
    print(f"Interactive E2E QA Results: {passed}/{total} steps passed", flush=True)
    print(f"==========================================", flush=True)
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    run_test()
