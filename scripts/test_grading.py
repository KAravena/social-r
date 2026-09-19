#!/usr/bin/env python3
"""Test grading execution with correct and incorrect inputs via webR and Quarto Live."""
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
        const testGrading = async () => {
            const webROjs = window._ojs.ojsConnector.mainModule._scope.get('webROjs')._value;
            const webR = await webROjs.webRPromise;
            const { WebREvaluator, WebRGrader, b64Decode } = window._exercise_ojs_runtime;

            // Get check code for exercise 0
            const checkScript = document.querySelector('script[type="exercise-check-intro-r-01-000-contents"]');
            const checkData = checkScript ? JSON.parse(b64Decode(checkScript.textContent)) : null;

            // Test evaluating user_code "18 + 11"
            const context1 = {
                code: "18 + 11",
                options: {
                    id: "webr-1-contents",
                    envir: "exercise-env-intro-r-01-000",
                    exercise: "intro-r-01-000"
                }
            };
            const evaluator1 = new WebREvaluator(webR, context1);
            await evaluator1.process({});
            const grader1 = new WebRGrader(evaluator1);
            const feedback1 = await grader1.gradeExercise();

            // Test evaluating user_code "18 + 12"
            const context2 = {
                code: "18 + 12",
                options: {
                    id: "webr-1-contents",
                    envir: "exercise-env-intro-r-01-000",
                    exercise: "intro-r-01-000"
                }
            };
            const evaluator2 = new WebREvaluator(webR, context2);
            await evaluator2.process({});
            const grader2 = new WebRGrader(evaluator2);
            const feedback2 = await grader2.gradeExercise();

            return {
                checkCode: checkData ? checkData.code : null,
                feedback1Text: feedback1 ? feedback1.textContent.trim() : null,
                feedback1Class: feedback1 ? feedback1.className : null,
                feedback2Text: feedback2 ? feedback2.textContent.trim() : null,
                feedback2Class: feedback2 ? feedback2.className : null
            };
        };
        return testGrading();
    """)
    print("Grading Test Results:", json.dumps(res, indent=2))
finally:
    driver.quit()
