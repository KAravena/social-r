#!/usr/bin/env python3
"""Verify grading on all 4 exercises."""
import json
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

options = EdgeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Edge(options=options)

try:
    driver.get("http://127.0.0.1:4200/")
    time.sleep(4.0)

    res = driver.execute_script("""
        const testAll = async () => {
            const webROjs = window._ojs.ojsConnector.mainModule._scope.get('webROjs')._value;
            const webR = await webROjs.webRPromise;
            const { WebREvaluator, WebRGrader } = window._exercise_ojs_runtime;

            async function gradeCode(exId, code) {
                const context = {
                    code: code,
                    options: {
                        id: `webr-${exId}-contents`,
                        envir: `exercise-env-${exId}`,
                        exercise: exId
                    }
                };
                const evaluator = new WebREvaluator(webR, context);
                await evaluator.process({});
                const grader = new WebRGrader(evaluator);
                const fb = await grader.gradeExercise();
                return {
                    text: fb ? fb.textContent.trim() : 'no fb',
                    className: fb ? fb.className : 'no class'
                };
            }

            // Ex 0: 18 + 12
            const ex0_bad = await gradeCode('intro-r-01-000', '18 + 11');
            const ex0_good = await gradeCode('intro-r-01-000', '18 + 12');

            // Ex 1: 25 + 17
            const ex1_bad = await gradeCode('intro-r-01-001', '25 + 10');
            const ex1_good = await gradeCode('intro-r-01-001', '25 + 17');

            // Ex 2: numero_estudiantes <- 120
            const ex2_bad = await gradeCode('intro-r-01-002', 'numero_estudiantes <- 100');
            const ex2_good = await gradeCode('intro-r-01-002', 'numero_estudiantes <- 120');

            // Ex 3: edad_promedio <- 21.4
            const ex3_char = await gradeCode('intro-r-01-003', 'edad_promedio <- "21.4"');
            const ex3_int = await gradeCode('intro-r-01-003', 'edad_promedio <- 22');
            const ex3_good = await gradeCode('intro-r-01-003', 'edad_promedio <- 21.4');

            return {
                ex0: { bad: ex0_bad, good: ex0_good },
                ex1: { bad: ex1_bad, good: ex1_good },
                ex2: { bad: ex2_bad, good: ex2_good },
                ex3: { char: ex3_char, int: ex3_int, good: ex3_good }
            };
        };
        return testAll();
    """)
    print(json.dumps(res, indent=2))
finally:
    driver.quit()
