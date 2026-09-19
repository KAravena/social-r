#!/usr/bin/env python3
"""Social R - Complete 13 Modules YAML Generator

Reads all 13 canonical locked Markdown files in md_finales/ and generates
complete, validated declarative YAML content for Social R.
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
LOCKED_DIR = ROOT / "md_finales"
CONTENT_DIR = ROOT / "content" / "courses" / "intro-r"
MODULES_DIR = CONTENT_DIR / "modules"
COURSE_YML = CONTENT_DIR / "course.yml"
SCHEMA_PATH = ROOT / "content" / "exercise.schema.json"

MODULE_METADATA = {
    1: {
        "slug": "01-empezar-a-pensar-con-r",
        "title": "Módulo 1: Empezar a pensar con R",
        "short_title": "Módulo 1",
        "description": "Aprende a comunicarte con R ejecutando instrucciones, creando tus primeros objetos con <-, consultando su contenido y reutilizándolos en nuevos cálculos para responder preguntas sociales.",
        "difficulty": "intro",
    },
    2: {
        "slug": "02-trabajar-con-varios-valores",
        "title": "Módulo 2: Trabajar con varios valores",
        "short_title": "Módulo 2",
        "description": "Descubre cómo organizar múltiples datos de una misma característica mediante vectores con c(), comprender el orden de las observaciones y acceder a posiciones específicas con corchetes [].",
        "difficulty": "beginner",
    },
    3: {
        "slug": "03-hacer-preguntas-a-los-datos",
        "title": "Módulo 3: Hacer preguntas a los datos",
        "short_title": "Módulo 3",
        "description": "Aprende a formular comparaciones con operadores relacionales (> , ==), comprender las respuestas lógicas TRUE y FALSE producidas por R, y seleccionar datos por condiciones sustantivas.",
        "difficulty": "beginner",
    },
    4: {
        "slug": "04-entender-una-base-de-datos",
        "title": "Módulo 4: Entender una base de datos",
        "short_title": "Módulo 4",
        "description": "Comprende la estructura de un data frame: cómo las filas representan casos o personas, las columnas representan variables, y cómo extraer una columna como vector utilizando el operador $.",
        "difficulty": "beginner",
    },
    5: {
        "slug": "05-seleccionar-y-filtrar-datos",
        "title": "Módulo 5: Seleccionar y filtrar datos",
        "short_title": "Módulo 5",
        "description": "Domina la preparación reproducible de datos con filter(), select() y el pipe nativo |>, encadenando transformaciones claras sin modificar la base de datos original.",
        "difficulty": "basic",
    },
    6: {
        "slug": "06-trabajar-cuando-faltan-datos",
        "title": "Módulo 6: Trabajar cuando faltan datos",
        "short_title": "Módulo 6",
        "description": "Aprende a identificar y tratar datos ausentes (NA), distinguiéndolos de ceros o texto, usando is.na(), sum(is.na()) y cálculos con valores disponibles mediante na.rm = TRUE.",
        "difficulty": "basic",
    },
    7: {
        "slug": "07-describir-categorias",
        "title": "Módulo 7: Describir categorías",
        "short_title": "Módulo 7",
        "description": "Distingue variables categóricas de cuantitativas, construye tablas de frecuencias con table() y calcula proporciones y porcentajes con prop.table() para interpretar la distribución social.",
        "difficulty": "basic",
    },
    8: {
        "slug": "08-describir-cantidades",
        "title": "Módulo 8: Describir cantidades",
        "short_title": "Módulo 8",
        "description": "Explora variables cuantitativas mediante histogramas, medidas de tendencia central (media y mediana) y medidas de dispersión (desviación estándar), evaluando el impacto de valores extremos.",
        "difficulty": "intermediate",
    },
    9: {
        "slug": "09-ver-relaciones-entre-dos-cantidades",
        "title": "Módulo 9: Ver relaciones entre dos cantidades",
        "short_title": "Módulo 9",
        "description": "Analiza relaciones bivariadas numéricas mediante diagramas de dispersión (scatterplots) con plot() y resume su fuerza y dirección lineal con el coeficiente de correlación de Pearson.",
        "difficulty": "intermediate",
    },
    10: {
        "slug": "10-elegir-y-evaluar-una-correlacion",
        "title": "Módulo 10: Elegir y evaluar una correlación",
        "short_title": "Módulo 10",
        "description": "Distingue relaciones lineales de monotónicas curvas, elige entre Pearson y Spearman (rho), y evalúa la evidencia inferencial con cor.test() interpretando p-values e intervalos de confianza.",
        "difficulty": "intermediate",
    },
    11: {
        "slug": "11-trabajar-con-varias-correlaciones",
        "title": "Módulo 11: Trabajar con varias correlaciones",
        "short_title": "Módulo 11",
        "description": "Construye matrices de correlación multivariadas con cor(), interpreta celdas, simetría y diagonal, maneja datos ausentes con pairwise y analiza variables binarias 0/1.",
        "difficulty": "advanced",
    },
    12: {
        "slug": "12-relacionar-categorias",
        "title": "Módulo 12: Relacionar categorías",
        "short_title": "Módulo 12",
        "description": "Analiza tablas de contingencia bidimensionales con table(x, y), compara porcentajes por fila con prop.table(t, 1), y evalúa independencia estadística mediante la prueba de chi-cuadrado.",
        "difficulty": "advanced",
    },
    13: {
        "slug": "13-de-la-pregunta-al-analisis",
        "title": "Módulo 13: De la pregunta al análisis",
        "short_title": "Módulo 13",
        "description": "Proyecto integrador: desde la pregunta sustantiva de investigación social hasta la selección de estrategia analítica, preparación de datos, modelado estadístico y conclusiones fundamentadas.",
        "difficulty": "advanced",
    },
}

DATASET_SETUP_R = {
    2: """tiempos_viaje <- c(25, 40, 35, 50, 30)
respuestas_diarias <- c(18, 22, 15, 25, 20)
horas_estudio <- c(4, 6, 2, 8, 5)""",
    3: """tiempos_viaje <- c(25, 40, 35, 50, 30)
supera_30 <- tiempos_viaje > 30
horas_estudio <- c(3, 5, 2, 6, 4)
carreras <- c("Sociología", "Historia", "Sociología", "Antropología")
es_sociologia <- carreras == "Sociología"
horas_cuidado <- c(6, 12, 8, 15, 10)""",
    4: """encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
encuesta_barrio <- data.frame(
  persona = 1:4,
  edad = c(34, 27, 41, 22),
  transporte = c("Bus", "Metro", "Bus", "Bicicleta"),
  minutos_viaje = c(45, 30, 50, 20),
  stringsAsFactors = FALSE
)""",
    5: """suppressPackageStartupMessages(library(dplyr))
encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
encuesta_jovenes <- data.frame(
  id = 1:8,
  edad = c(18, 20, 19, 22, 21, 23, 19, 24),
  estudia = c("Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí"),
  comuna = c("Norte", "Centro", "Sur", "Centro", "Norte", "Sur", "Norte", "Centro"),
  transporte = c("Bus", "Metro", "Bicicleta", "Bus", "Metro", "Metro", "Bus", "Bicicleta"),
  stringsAsFactors = FALSE
)""",
    6: """encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  horas_cuidado = c(6, NA, 0, 8, 4, 5, NA, 7),
  stringsAsFactors = FALSE
)
horas_cuidado <- c(6, 0, NA, 8, 4)
encuesta_barrio <- data.frame(
  id = 1:6,
  minutos_viaje = c(35, NA, 50, 20, NA, 40),
  transporte = c("Bus", "Metro", "Bus", "Bicicleta", "Metro", "Bus"),
  stringsAsFactors = FALSE
)""",
    7: """encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
tabla_carrera <- table(encuesta_social_demo$carrera)
encuesta_campus <- data.frame(
  id = 1:8,
  transporte = c("Metro", "Bus", "Bicicleta", "Metro", "A pie", "Bus", "Metro", "Bicicleta"),
  stringsAsFactors = FALSE
)""",
    8: """encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  horas_cuidado = c(6, NA, 0, 8, 4, 5, NA, 7),
  stringsAsFactors = FALSE
)
horas_estudio <- encuesta_social_demo$horas_estudio
minutos_lectura <- c(25, 10, 20, 30, 15, 22, 18)
viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)
viaje_extremo <- c(20, 22, 24, 25, 26, 28, 120)
grupo_a <- c(4, 4, 4, 4, 4)
grupo_b <- c(2, 3, 4, 5, 6)
encuesta_movilidad <- data.frame(
  id = 1:10,
  transporte = c("Metro", "Bus", "Metro", "Bus", "Bicicleta", "Metro", "Bus", "A pie", "Metro", "Bus"),
  minutos_viaje = c(25, 30, 32, 28, 35, 27, 31, 29, 34, 90),
  stringsAsFactors = FALSE
)""",
    9: """encuesta_social <- data.frame(
  id = 1:12,
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 11, 4, 6),
  puntaje_metodos = c(59, 68, 58, 64, 62, 75, 65, 64, 74, 84, 59, 73),
  horas_trabajo = c(20, 35, 0, 25, 40, 0, 30, 45, 0, 38, 0, 32),
  horas_sueno = c(8.4, 7.7, 8.5, 7.6, 7.6, 8.2, NA, 7.1, 8.3, 7.7, 8.1, 7.4),
  trabaja = c("Sí", "Sí", "No", "Sí", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
encuesta_lectura <- data.frame(
  id = 1:10,
  minutos_lectura = c(15, 35, 25, 55, 20, 50, 30, 60, 40, 45),
  puntaje_comprension = c(50, 57, 66, 84, 59, 69, 68, 83, 55, 62),
  stringsAsFactors = FALSE
)""",
    10: """encuesta_social <- data.frame(
  id = 1:12,
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 11, 4, 6),
  puntaje_metodos = c(59, 68, 58, 64, 62, 75, 65, 64, 74, 84, 59, 73),
  edad = c(20, 22, 19, 21, 24, 23, 20, 25, 27, 26, 22, 24),
  horas_ocio = c(6.0, 5.2, 6.1, 5.0, 5.8, 5.4, 5.6, 5.2, 5.0, 4.8, 5.5, 5.1),
  stringsAsFactors = FALSE
)
x_curva <- c(1, 2, 3, 4, 5, 6, 7, 8)
y_curva <- c(1, 2, 4, 8, 16, 32, 64, 128)
encuesta_emprendimiento <- data.frame(
  id = 1:8,
  antiguedad_anos = c(1, 2, 3, 4, 5, 6, 7, 8),
  ventas_mensuales = c(100, 110, 120, 140, 180, 300, 800, 3000),
  stringsAsFactors = FALSE
)""",
    11: """encuesta_social <- data.frame(
  id = 1:12,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25, 27, 26, 22, 24),
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 11, 4, 6),
  horas_ocio = c(6.0, 5.2, 6.1, 5.0, 5.8, 5.4, 5.6, 5.2, 5.0, 4.8, 5.5, 5.1),
  trabaja_01 = c(1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1),
  ingreso_miles = c(420, 650, 300, 380, 720, 450, 500, 800, 520, 620, 350, 550),
  stringsAsFactors = FALSE
)
seguimiento <- data.frame(
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 6),
  horas_sueno = c(8.1, 7.4, NA, 7.8, 6.9, 7.2, 6.5, NA, 7.0, 7.6),
  estres = c(3, 5, 4, 6, NA, 8, 5, 7, NA, 4),
  stringsAsFactors = FALSE
)""",
    12: """set.seed(42)
encuesta_participacion <- data.frame(
  id = 1:60,
  participacion_organizacion = c(rep("Participa", 40), rep("No participa", 20)),
  transporte_campus = c(
    rep("Metro", 12), rep("Bus", 20), rep("Bicicleta", 8),
    rep("Metro", 3), rep("Bus", 10), rep("Bicicleta", 7)
  ),
  stringsAsFactors = FALSE
)
tabla <- table(encuesta_participacion$participacion_organizacion, encuesta_participacion$transporte_campus)
encuesta_comunidad <- data.frame(
  id = 1:80,
  zona_residencia = rep(c("Norte", "Centro", "Sur"), length.out = 80),
  actividad_comunitaria = rep(c("Alta", "Media", "Baja", "Media"), 20),
  stringsAsFactors = FALSE
)""",
    13: """encuesta_vida_universitaria <- data.frame(
  id = 1:48,
  jornada = c(rep("Diurna", 32), rep("Vespertina", 16)),
  horas_estudio = c(
    c(2, 4, 3, 6, 5, 8, 7, 10, 9, 11, 4, 6, 3, 5, 2, 7, 8, 6, 4, 5, 9, 3, 4, 6, 5, 7, 8, 4, 6, 5, 3, 7),
    c(2, 3, 1, 4, 2, 5, 3, 4, 2, 3, 4, 1, 3, 2, 4, 3)
  ),
  autoeficacia_academica = c(
    c(59, 68, 58, 64, 62, 75, 65, 64, 74, 84, 59, 73, 60, 66, 56, 70, 78, 69, 63, 67, 79, 58, 62, 71, 65, 72, 76, 61, 70, 64, 57, 74),
    c(52, 55, 48, 60, 51, 62, 54, 58, 50, 56, 61, 47, 55, 53, 63, 57)
  ),
  transporte_campus = rep(c("Metro", "Bus", "Bicicleta", "Bus"), 12),
  participa_organizacion = rep(c("Sí", "No", "Sí", "No", "No", "Sí"), 8),
  stringsAsFactors = FALSE
)
datos_estudio_diurno <- subset(encuesta_vida_universitaria, jornada == "Diurna", select = c("horas_estudio", "autoeficacia_academica"))
encuesta_vinculos_barriales <- data.frame(
  id = 1:40,
  ocupado = c(rep("Sí", 28), rep("No", 12)),
  participa_vecinal_01 = c(rep(c(1, 0, 1, 1, 0, 1, 0), 4), rep(c(0, 1, 0), 4)),
  confianza_comunitaria = c(
    c(7, 8, 6, 9, 5, 8, 6, 7, 8, 9, 6, 7, 8, 6, 9, 7, 8, 5, 7, 8, 6, 9, 7, 8, 6, 7, 8, 6),
    c(5, 6, 4, 6, 5, 7, 4, 5, 6, 5, 6, 4)
  ),
  stringsAsFactors = FALSE
)""",
}

def clean_text(t: str) -> str:
    return re.sub(r"\r\n", "\n", t).strip()

def extract_fenced(text: str) -> str:
    m = re.search(r"```(?:r|text)?\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).rstrip()
    return ""

def slugify(title: str) -> str:
    t = title.lower()
    t = re.sub(r"[áàäâ]", "a", t)
    t = re.sub(r"[éèëê]", "e", t)
    t = re.sub(r"[íìïî]", "i", t)
    t = re.sub(r"[óòöô]", "o", t)
    t = re.sub(r"[úùüû]", "u", t)
    t = re.sub(r"[ñ]", "n", t)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")

def split_context_instruction(s10: str, s8: str) -> tuple[str, str]:
    s10 = clean_text(s10)
    if "**Tarea.**" in s10 or "#### Tu tarea" in s10 or "**Tarea:**" in s10:
        parts = re.split(r"\*\*(?:Tarea|Tu tarea)[.:]?\*\*", s10, maxsplit=1)
        ctx = clean_text(parts[0])
        ctx = re.sub(r"^\*\*(?:Situación)[.:]?\*\*\s*", "", ctx)
        inst = clean_text(parts[1])
        return (ctx if ctx else clean_text(s8)), inst
    
    if "\n\n" in s10:
        paras = s10.split("\n\n")
        ctx = "\n\n".join(paras[:-1]).strip()
        inst = paras[-1].strip()
        return (ctx if ctx else clean_text(s8)), inst
    
    return clean_text(s8), s10

def parse_hints(body: str) -> list[dict[str, Any]]:
    hint_matches = re.finditer(r"### (?:2[2-9]|3[0-2])\.\s*Hint\s*(\d+)\s*\n(.*?)(?=\n###|\Z)", body, re.DOTALL)
    hints = []
    for hm in hint_matches:
        idx = int(hm.group(1))
        htext = clean_text(hm.group(2))
        title_labels = ["Conceptual", "Procedimiento", "Sintaxis / Acción", "Casi resuelta", "Orientación"]
        title_label = title_labels[min(idx - 1, len(title_labels) - 1)]
        title = f"Pista {idx} · {title_label}"
        
        code = None
        code_m = re.search(r"```(?:r)?\s*\n(.*?)```", htext, re.DOTALL)
        if code_m:
            code = code_m.group(1).rstrip()
            htext = re.sub(r"```(?:r)?\s*\n.*?```", "", htext, flags=re.DOTALL).strip()
        
        if not htext:
            htext = "Puedes guiarte con la siguiente sintaxis o estructura de código:"
        
        hint_obj = {"title": title, "text": htext}
        if code:
            hint_obj["code"] = code
        hints.append(hint_obj)
    return hints

def get_exercise_specs(m_num: int, ex_num: int, s13: str, s15: str, s14: str, s16: str, s17: str, s19: str, s20: str, s21: str):
    starter = extract_fenced(s13)
    solution = extract_fenced(s15)
    checks: list[dict[str, Any]] = []
    diags: list[dict[str, Any]] = []

    # Custom specifications for specific exercises
    if m_num == 1 and ex_num == 1:
        starter = "18 + 12"
        solution = "18 + 12"
        checks = [
            {"type": "result_equals", "expected": 30, "message": "El resultado de la operación debería ser 30."}
        ]
        diags = [
            {"when_r": "identical(.res_val, 30) && !grepl('\\\\+', .user_code)",
             "message": "30 es el resultado correcto, pero aquí queremos que R haga el cálculo. Vuelve a usar la suma y ejecútala.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 1 and ex_num == 2:
        starter = "18 + 12"
        solution = "18 + 15"
        checks = [
            {"type": "result_equals", "expected": 33, "message": "El resultado con el segundo conteo actualizado a 15 debería ser 33."}
        ]
        diags = [
            {"when_r": "identical(.res_val, 30)",
             "message": "El resultado sigue siendo 30. Recuerda cambiar el segundo número a 15 y volver a ejecutar.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 1 and ex_num == 3:
        starter = "respuestas <- 33\n\nrespuestas"
        solution = "respuestas <- 33\n\nrespuestas"
        checks = [
            {"type": "object_exists", "object": "respuestas", "message": "Debes crear el objeto 'respuestas'."},
            {"type": "object_value", "object": "respuestas", "expected": 33, "message": "El objeto 'respuestas' debe guardar el valor 33."}
        ]
        diags = [
            {"when_r": "!exists('respuestas', envir = .target_env)",
             "message": "Crea el objeto con `respuestas <- 33`.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 1 and ex_num == 4:
        starter = "respuestas_sociologia <- 18\n\n# crea respuestas_antropologia con 15\n\n\n# consulta ambos objetos\n"
        solution = "respuestas_sociologia <- 18\nrespuestas_antropologia <- 15\n\nrespuestas_sociologia\nrespuestas_antropologia"
        checks = [
            {"type": "object_exists", "object": "respuestas_sociologia", "message": "Falta el objeto 'respuestas_sociologia'."},
            {"type": "object_value", "object": "respuestas_sociologia", "expected": 18, "message": "Conserva 'respuestas_sociologia' con 18."},
            {"type": "object_exists", "object": "respuestas_antropologia", "message": "Falta crear 'respuestas_antropologia'."},
            {"type": "object_value", "object": "respuestas_antropologia", "expected": 15, "message": "'respuestas_antropologia' debe guardar 15."}
        ]
        diags = [
            {"when_r": "!exists('respuestas_antropologia', envir = .target_env)",
             "message": "Crea 'respuestas_antropologia <- 15'.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 1:
        starter = "# Pregunta 1: ¿Cuántos años tiene la persona que estudia 5 horas?\nedad_persona_2 <- ___"
        solution = "edad_persona_2 <- 22"
        checks = [
            {"type": "object_exists", "object": "edad_persona_2", "message": "Debes crear el objeto 'edad_persona_2'."},
            {"type": "object_value", "object": "edad_persona_2", "expected": 22, "message": "La persona que estudia 5 horas tiene 22 años (Persona 2)."}
        ]
        diags = [
            {"when_r": "exists('edad_persona_2', envir = .target_env) && !isTRUE(all.equal(get('edad_persona_2', envir = .target_env), 22))",
             "message": "Revisa la tabla: la Persona 2 tiene 22 años y estudia 5 horas.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 2:
        starter = "# Pregunta 2: Escribe las 4 edades que aparecen en la encuesta como un vector\nedades_encuesta <- c(___, ___, ___, ___)"
        solution = "edades_encuesta <- c(20, 22, 19, 21)"
        checks = [
            {"type": "object_exists", "object": "edades_encuesta", "message": "Debes crear el objeto 'edades_encuesta'."},
            {"type": "object_value", "object": "edades_encuesta", "expected": [20, 22, 19, 21], "message": "Las edades de las 4 personas son 20, 22, 19 y 21."}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 3:
        starter = "head(encuesta_social_demo)"
        solution = "head(encuesta_social_demo)"
        checks = [
            {"type": "custom_r", "code": "is.data.frame(.res_val) && nrow(.res_val) == 6 && 'carrera' %in% names(.res_val)",
             "message": "head(encuesta_social_demo) debe mostrar las primeras 6 filas de la base."}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 4:
        starter = "encuesta_social_demo$horas_estudio"
        solution = "encuesta_social_demo$horas_estudio"
        checks = [
            {"type": "result_equals", "expected": [3, 5, 2, 4, 6, 3, 5, 2],
             "message": "Al extraer la columna con $horas_estudio obtienes el vector de 8 horas de estudio."}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 5:
        starter = "str(encuesta_social_demo)"
        solution = "str(encuesta_social_demo)"
        checks = [
            {"type": "custom_r", "code": "grepl('str\\\\s*\\\\(', .user_code)",
             "message": "Ejecuta str(encuesta_social_demo) para observar la estructura interna de la base."}
        ]
        return starter, solution, checks, diags

    if m_num == 4 and ex_num == 6:
        starter = "encuesta_barrio$minutos_viaje"
        solution = "encuesta_barrio$minutos_viaje"
        checks = [
            {"type": "result_equals", "expected": [45, 30, 50, 20],
             "message": "Extrae la columna minutos_viaje de encuesta_barrio con el operador $."}
        ]
        return starter, solution, checks, diags

    if m_num == 7 and ex_num == 1:
        starter = '# Clasifica cada variable como "categoria" o "cantidad":\ntipo_carrera <- "___"\ntipo_horas <- "___"\ntipo_zona_codigo <- "___"'
        solution = 'tipo_carrera <- "categoria"\ntipo_horas <- "cantidad"\ntipo_zona_codigo <- "categoria"'
        checks = [
            {"type": "object_value", "object": "tipo_carrera", "expected": "categoria", "message": "'carrera' representa categorías (nombres), no cantidades."},
            {"type": "object_value", "object": "tipo_horas", "expected": "cantidad", "message": "'horas_estudio' representa una cantidad numérica."},
            {"type": "object_value", "object": "tipo_zona_codigo", "expected": "categoria", "message": "Aunque use números (1, 2, 3), 'zona_codigo' representa categorías (Norte, Centro, Sur)."}
        ]
        diags = [
            {"when_r": "exists('tipo_zona_codigo', envir = .target_env) && identical(get('tipo_zona_codigo', envir = .target_env), 'cantidad')",
             "message": "Cuidado: 'zona_codigo' usa números solo como etiquetas (1 = Norte, 2 = Centro). Es una categoría.", "type": "warning"}
        ]
        return starter, solution, checks, diags

    if m_num == 9 and ex_num == 1:
        starter = "# Escribe las horas de estudio y el puntaje de la Persona 3 como un par c(x, y)\npar_persona_3 <- c(___, ___)"
        solution = "par_persona_3 <- c(3, 58)"
        checks = [
            {"type": "object_exists", "object": "par_persona_3", "message": "Debes definir 'par_persona_3'."},
            {"type": "object_value", "object": "par_persona_3", "expected": [3, 58], "message": "El caso 3 tiene 3 horas de estudio y puntaje 58: c(3, 58)."}
        ]
        return starter, solution, checks, diags

    if m_num == 9 and ex_num == 3:
        starter = '# Clasifica la relación de cada gráfico como "positiva", "negativa" o "sin_direccion":\ndireccion_a <- "___"  # Gráfico A\ndireccion_b <- "___"  # Gráfico B\ndireccion_c <- "___"  # Gráfico C'
        solution = 'direccion_a <- "positiva"\ndireccion_b <- "negativa"\ndireccion_c <- "sin_direccion"'
        checks = [
            {"type": "object_value", "object": "direccion_a", "expected": "positiva", "message": "El Gráfico A asciende de izquierda a derecha: relación positiva."},
            {"type": "object_value", "object": "direccion_b", "expected": "negativa", "message": "El Gráfico B desciende de izquierda a derecha: relación negativa."},
            {"type": "object_value", "object": "direccion_c", "expected": "sin_direccion", "message": "El Gráfico C muestra una nube dispersa sin tendencia lineal: sin dirección clara."}
        ]
        return starter, solution, checks, diags

    if m_num == 9 and ex_num == 4:
        starter = '# ¿Cuál gráfico tiene los puntos más concentrados alrededor de una línea? ("A" o "B")\ngrafico_mas_concentrado <- "___"'
        solution = 'grafico_mas_concentrado <- "A"'
        checks = [
            {"type": "object_value", "object": "grafico_mas_concentrado", "expected": "A", "message": "El Gráfico A tiene puntos mucho más concentrados y alineados (r ≈ 0.99) que el B (r ≈ 0.77)."}
        ]
        return starter, solution, checks, diags

    if m_num == 10 and ex_num == 1:
        starter = "# Ejecuta la correlación de Spearman para la relación monotónica curva:\ncor(x_curva, y_curva, method = \"spearman\")"
        solution = 'cor(x_curva, y_curva, method = "spearman")'
        checks = [
            {"type": "result_equals", "expected": 1.0, "message": "El coeficiente de Spearman para una relación monotónica creciente perfecta es 1."}
        ]
        return starter, solution, checks, diags

    if m_num == 10 and ex_num == 3:
        starter = '# Elige el método ("pearson", "spearman" o "ninguno") para cada escenario:\nmetodo_a <- "___"  # Relación aproximadamente lineal\nmetodo_b <- "___"  # Relación monotónica curva\nmetodo_c <- "___"  # Relación en forma de U'
        solution = 'metodo_a <- "pearson"\nmetodo_b <- "spearman"\nmetodo_c <- "ninguno"'
        checks = [
            {"type": "object_value", "object": "metodo_a", "expected": "pearson", "message": "Para relaciones aproximadamente lineales el método estándar es Pearson."},
            {"type": "object_value", "object": "metodo_b", "expected": "spearman", "message": "Para relaciones monotónicas curvas o basadas en rangos usamos Spearman."},
            {"type": "object_value", "object": "metodo_c", "expected": "ninguno", "message": "Un patrón en forma de U no es lineal ni monotónico: ni Pearson ni Spearman lo resumen adecuadamente."}
        ]
        return starter, solution, checks, diags

    if m_num == 10 and ex_num == 5:
        starter = '# Responde si cada afirmación sobre el p-value (p = 0.00496) es TRUE o FALSE:\nafirmacion_probabilidad_h0 <- ___    # "¿p es la probabilidad de que H0 sea cierta?"\nafirmacion_incompatibilidad <- ___   # "¿p indica cuán incompatibles son los datos con H0?"'
        solution = "afirmacion_probabilidad_h0 <- FALSE\nafirmacion_incompatibilidad <- TRUE"
        checks = [
            {"type": "object_value", "object": "afirmacion_probabilidad_h0", "expected": False, "message": "Falso: el p-value NO es la probabilidad de que la hipótesis nula sea verdadera."},
            {"type": "object_value", "object": "afirmacion_incompatibilidad", "expected": True, "message": "Verdadero: un p pequeño indica que los datos observados son poco compatibles con el escenario nulo."}
        ]
        return starter, solution, checks, diags

    if m_num == 10 and ex_num == 6:
        starter = '# Compara ambos estudios (ambos r = 0.50):\nestudio_menor_p <- "___"             # "¿Cuál tiene menor p-value? ("Estudio A" o "Estudio B")"\nestudio_mayor_precision <- "___"     # "¿Cuál tiene el IC más estrecho/preciso? ("Estudio A" o "Estudio B")"'
        solution = 'estudio_menor_p <- "Estudio B"\nestudio_mayor_precision <- "Estudio B"'
        checks = [
            {"type": "object_value", "object": "estudio_menor_p", "expected": "Estudio B", "message": "El Estudio B tiene N = 50, por lo que produce mucha mayor evidencia estadística (p = 0.0002 frente a p = 0.098)."},
            {"type": "object_value", "object": "estudio_mayor_precision", "expected": "Estudio B", "message": "Con mayor tamaño muestral, el intervalo de confianza es más estrecho y preciso."}
        ]
        return starter, solution, checks, diags

    if m_num == 11 and ex_num == 3:
        starter = "# ¿Cuántos pares únicos de correlación contiene una matriz de 3 variables? (sin contar diagonal ni repeticiones)\npares_unicos <- ___"
        solution = "pares_unicos <- 3"
        checks = [
            {"type": "object_value", "object": "pares_unicos", "expected": 3, "message": "Una matriz de 3x3 tiene 3 pares únicos: (1,2), (1,3) y (2,3)."}
        ]
        return starter, solution, checks, diags

    if m_num == 12 and ex_num == 3:
        starter = "# ¿Qué porcentaje de personas esperaríamos que usen Metro si el transporte fuera independiente de la participación? (25, 50 o 75)\nporcentaje_esperado_metro <- ___"
        solution = "porcentaje_esperado_metro <- 25"
        checks = [
            {"type": "object_value", "object": "porcentaje_esperado_metro", "expected": 25, "message": "Como el 25% del total usa Metro (15 de 60), bajo independencia esperaríamos ese mismo 25% en cada grupo."}
        ]
        return starter, solution, checks, diags

    if m_num == 12 and ex_num == 6:
        starter = '# Compara ambas tablas (ambas p < 0.05). ¿Cuál muestra una asociación más fuerte y concentrada? ("Tabla 1" o "Tabla 2")\ntabla_asociacion_mas_fuerte <- "___"'
        solution = 'tabla_asociacion_mas_fuerte <- "Tabla 2"'
        checks = [
            {"type": "object_value", "object": "tabla_asociacion_mas_fuerte", "expected": "Tabla 2", "message": "La Tabla 2 tiene una asociación sustantivamente más fuerte (V de Cramér mayor) a pesar de que ambas son estadísticamente significativas."}
        ]
        return starter, solution, checks, diags

    if m_num == 13 and ex_num == 1:
        starter = '# Clasifica el tipo de problema ("cuantitativo" o "categorico"):\nproblema_1 <- "___"  # Horas de estudio y autoeficacia (números)\nproblema_2 <- "___"  # Transporte y participación (grupos/categorías)'
        solution = 'problema_1 <- "cuantitativo"\nproblema_2 <- "categorico"'
        checks = [
            {"type": "object_value", "object": "problema_1", "expected": "cuantitativo", "message": "Horas y puntajes son cantidades continuas: problema cuantitativo (correlación)."},
            {"type": "object_value", "object": "problema_2", "expected": "categorico", "message": "Transporte y participación son grupos: problema categórico (tablas de contingencia y chi-cuadrado)."}
        ]
        return starter, solution, checks, diags

    # General extraction
    if not starter:
        starter = extract_fenced(s15)
    if not solution:
        solution = starter

    # Parse assignment in solution
    assign_match = re.search(r"^([a-zA-Z0-9._]+)\s*(?:<-|=)\s*(.*?)$", solution, re.M)
    is_plot = bool(re.search(r"\b(plot|hist|barplot)\s*\(", solution))
    is_str = bool(re.search(r"\bstr\s*\(", solution))

    if is_plot:
        checks.append({
            "type": "custom_r",
            "code": "grepl('(plot|hist|barplot)\\\\s*\\\\(', .user_code)",
            "message": "Asegúrate de generar el gráfico solicitado utilizando la función correspondiente (plot, hist o barplot)."
        })
    elif is_str:
        checks.append({
            "type": "custom_r",
            "code": "grepl('str\\\\s*\\\\(', .user_code)",
            "message": "Usa la función str() para inspeccionar la estructura de la base."
        })
    elif assign_match:
        obj_name = assign_match.group(1).strip()
        checks.append({
            "type": "object_exists",
            "object": obj_name,
            "message": f"Debes crear el objeto '{obj_name}' usando <-."
        })
        checks.append({
            "type": "custom_r",
            "code": f"exists('{obj_name}', envir = .target_env, inherits = FALSE)",
            "message": f"El objeto '{obj_name}' debe existir en el entorno."
        })
    else:
        clean_res = clean_text(s16).strip("`").replace(">", "").strip().rstrip(".")
        num_match = re.match(r"^([0-9]+(?:\.[0-9]+)?)$", clean_res)
        if num_match:
            val = float(num_match.group(1)) if "." in num_match.group(1) else int(num_match.group(1))
            checks.append({
                "type": "result_equals",
                "expected": val,
                "message": f"El resultado de la operación debería ser {val}."
            })
        else:
            checks.append({
                "type": "custom_r",
                "code": "!is.null(.res_val)",
                "message": "Ejecuta la instrucción para obtener el resultado esperado."
            })

    diags.append({
        "when_r": "is.null(.res_val) && !exists('.result', envir = .target_env)",
        "message": "Recuerda ejecutar tu código con Ctrl + Enter o pulsar el botón para comprobar.",
        "type": "info"
    })

    return starter, solution, checks, diags

def build_all():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    print(f"Purging existing modules in {MODULES_DIR} ...")
    for item in MODULES_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)

    all_exercise_records = []
    course_modules_yml = []

    for m_num in range(1, 14):
        meta = MODULE_METADATA[m_num]
        slug = meta["slug"]
        mod_title = meta["title"]
        short_title = meta["short_title"]
        m_dir = MODULES_DIR / slug
        ex_dir = m_dir / "exercises"
        ex_dir.mkdir(parents=True, exist_ok=True)

        locked_path = LOCKED_DIR / f"social_r_modulo_{m_num:02d}_diseno_LOCKED.md"
        if not locked_path.exists():
            raise FileNotFoundError(f"Locked file not found: {locked_path}")

        content = locked_path.read_text(encoding="utf-8")
        raw_exs = re.split(r"\n##\s+(M\d+[-_]E\d+.*?)\n", content)

        exercises_data = []
        for i in range(1, len(raw_exs), 2):
            header = raw_exs[i].strip()
            body = raw_exs[i + 1]

            # Extract pure exercise title without "M1-E1 — " or "E1 — "
            clean_title = re.sub(r"^(?:M\d+[-_])?E\d+\s*[—–-]\s*", "", header).strip()
            ex_idx = len(exercises_data) + 1

            def get_sec(pat: str) -> str:
                m = re.search(pat, body, re.DOTALL)
                return clean_text(m.group(1)) if m else ""

            s4 = get_sec(r"### 4\.\s*Capacidad después[^\n]*\n(.*?)(?=\n###|\Z)")
            s8 = get_sec(r"### 8\.\s*Contexto sustantivo[^\n]*\n(.*?)(?=\n###|\Z)")
            s10 = get_sec(r"### 10\.\s*Texto para\s*(?:el\s*)?estudiante[^\n]*\n(.*?)(?=\n###|\Z)")
            s13 = get_sec(r"### 13\.\s*Starter[^\n]*\n(.*?)(?=\n###|\Z)")
            s14 = get_sec(r"### 14\.\s*Acción esperada[^\n]*\n(.*?)(?=\n###|\Z)")
            s15 = get_sec(r"### 15\.\s*Solución canónica[^\n]*\n(.*?)(?=\n###|\Z)")
            s16 = get_sec(r"### 16\.\s*Resultado esperado[^\n]*\n(.*?)(?=\n###|\Z)")
            s17 = get_sec(r"### 17\.\s*Criterio[^\n]*\n(.*?)(?=\n###|\Z)")
            s19 = get_sec(r"### 19\.\s*Error esperado[^\n]*\n(.*?)(?=\n###|\Z)")
            s20 = get_sec(r"### 20\.\s*Feedback[^\n]*\n(.*?)(?=\n###|\Z)")
            s21 = get_sec(r"### 21\.\s*Feedback[^\n]*\n(.*?)(?=\n###|\Z)")

            hints = parse_hints(body)
            starter, solution, checks, diags = get_exercise_specs(
                m_num, ex_idx, s13, s15, s14, s16, s17, s19, s20, s21
            )
            ctx, inst = split_context_instruction(s10, s8)

            success_msg = s20.strip()
            if not success_msg:
                success_msg = f"¡Excelente trabajo! Has completado el ejercicio correctamente."

            ex_record = {
                "m_num": m_num,
                "ex_idx": ex_idx,
                "id": f"intro-r-{m_num:02d}-{ex_idx:03d}",
                "course": "intro-r",
                "module": slug,
                "order": ex_idx - 1,
                "title": clean_title,
                "context": ctx,
                "instruction": inst,
                "learning_objectives": {
                    "r": s4[:120].strip().rstrip(";.") if s4 else f"Aprender y aplicar conceptos de R para {clean_title.lower()}.",
                    "data": s8[:120].strip().rstrip(";.") if s8 else "Comprender la estructura de los datos.",
                    "social": f"Aplicación a investigación social en {mod_title.lower()}."
                },
                "ui": {
                    "show_workflow_help": (m_num == 1 and ex_idx == 1),
                    "show_objective": True
                },
                "difficulty": meta["difficulty"],
                "type": "code",
                "starter_code": starter,
                "setup_code": DATASET_SETUP_R.get(m_num, ""),
                "solution_code": solution,
                "checks": checks,
                "diagnostics": diags,
                "hints": hints,
                "success_message": success_msg,
                "file_slug": f"{ex_idx:02d}-{slugify(clean_title)}.yml"
            }
            exercises_data.append(ex_record)
            all_exercise_records.append(ex_record)

        # Build module.yml
        mod_yml_data = {
            "id": slug,
            "title": mod_title,
            "short_title": short_title,
            "order": m_num,
            "description": meta["description"],
            "learning_outcomes": [
                f"Dominar las habilidades nucleares del {short_title}.",
                f"Aplicar análisis reproducible con datos de ciencias sociales."
            ],
            "exercises": [ex["id"] for ex in exercises_data]
        }
        (m_dir / "module.yml").write_text(yaml.dump(mod_yml_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

        course_modules_yml.append({
            "id": slug,
            "title": mod_title,
            "path": f"modules/{slug}"
        })

    # Link navigation pointers and write exercise YAMLs
    for i, ex in enumerate(all_exercise_records):
        nxt = all_exercise_records[i + 1]["id"] if i + 1 < len(all_exercise_records) else None
        ex["navigation"] = {"next": nxt}
        ex_dir = MODULES_DIR / ex["module"] / "exercises"
        yml_path = ex_dir / ex["file_slug"]

        clean_ex = {k: v for k, v in ex.items() if not k.startswith("m_") and k not in ("ex_idx", "file_slug")}
        clean_ex["schema_version"] = 1

        errors = list(validator.iter_errors(clean_ex))
        if errors:
            err_msgs = [f"  {e.path}: {e.message}" for e in errors]
            raise ValueError(f"Schema validation error in {clean_ex['id']} ({clean_ex['title']}):\n" + "\n".join(err_msgs))

        yml_content = yaml.dump(clean_ex, sort_keys=False, allow_unicode=True)
        yml_path.write_text(yml_content, encoding="utf-8")

    # Update course.yml
    course_data = {
        "id": "intro-r",
        "title": "Introducción a R para Ciencias Sociales",
        "description": "Plataforma interactiva completa con los 13 módulos de fundamentos de programación y análisis de datos en R para investigación social.",
        "version": "1.0.0",
        "modules": course_modules_yml
    }
    COURSE_YML.write_text(yaml.dump(course_data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"\n[OK] Successfully built and validated all 13 modules ({len(all_exercise_records)} exercises total)!")

if __name__ == "__main__":
    build_all()
