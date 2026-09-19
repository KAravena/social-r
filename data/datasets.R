# Social R - Datasets Contractuales Canónicos (M01-M13)
# Definiciones reproducibles de todos los data frames del curso

# 1. M04-M08: encuesta_social_demo
encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  horas_cuidado = c(6, NA, 0, 8, 4, 5, NA, 7),
  stringsAsFactors = FALSE
)

# 2. M04: encuesta_barrio
encuesta_barrio <- data.frame(
  persona = 1:4,
  edad = c(34, 27, 41, 22),
  transporte = c("Bus", "Metro", "Bus", "Bicicleta"),
  minutos_viaje = c(45, 30, 50, 20),
  stringsAsFactors = FALSE
)

# Versión M06 de encuesta_barrio con missing
encuesta_barrio_m6 <- data.frame(
  id = 1:6,
  minutos_viaje = c(35, NA, 50, 20, NA, 40),
  transporte = c("Bus", "Metro", "Bus", "Bicicleta", "Metro", "Bus"),
  stringsAsFactors = FALSE
)

# 3. M05: encuesta_jovenes
encuesta_jovenes <- data.frame(
  id = 1:8,
  edad = c(18, 20, 19, 22, 21, 23, 19, 24),
  estudia = c("Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí"),
  comuna = c("Norte", "Centro", "Sur", "Centro", "Norte", "Sur", "Norte", "Centro"),
  transporte = c("Bus", "Metro", "Bicicleta", "Bus", "Metro", "Metro", "Bus", "Bicicleta"),
  stringsAsFactors = FALSE
)

# 4. M07: encuesta_campus
encuesta_campus <- data.frame(
  id = 1:8,
  transporte = c("Metro", "Bus", "Bicicleta", "Metro", "A pie", "Bus", "Metro", "Bicicleta"),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  satisfaccion = c("Alta", "Media", "Alta", "Baja", "Media", "Alta", "Media", "Alta"),
  stringsAsFactors = FALSE
)

# 5. M08: encuesta_movilidad
encuesta_movilidad <- data.frame(
  id = 1:10,
  transporte = c("Metro", "Bus", "Metro", "Bus", "Bicicleta", "Metro", "Bus", "A pie", "Metro", "Bus"),
  minutos_viaje = c(25, 30, 32, 28, 35, 27, 31, 29, 34, 90),
  stringsAsFactors = FALSE
)

# 6. M09-M11: encuesta_social
encuesta_social <- data.frame(
  id = 1:12,
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 11, 4, 6),
  puntaje_metodos = c(59, 68, 58, 64, 62, 75, 65, 64, 74, 84, 59, 73),
  horas_trabajo = c(20, 35, 0, 25, 40, 0, 30, 45, 0, 38, 0, 32),
  horas_sueno = c(8.4, 7.7, 8.5, 7.6, 7.6, 8.2, NA, 7.1, 8.3, 7.7, 8.1, 7.4),
  trabaja = c("Sí", "Sí", "No", "Sí", "Sí", "No", "Sí", "Sí", "No", "Sí", "No", "Sí"),
  edad = c(20, 22, 19, 21, 24, 23, 20, 25, 27, 26, 22, 24),
  horas_ocio = c(6.0, 5.2, 6.1, 5.0, 5.8, 5.4, 5.6, 5.2, 5.0, 4.8, 5.5, 5.1),
  trabaja_01 = c(1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1),
  ingreso_miles = c(420, 650, 300, 380, 720, 450, 500, 800, 520, 620, 350, 550),
  stringsAsFactors = FALSE
)

# 7. M09: encuesta_lectura
encuesta_lectura <- data.frame(
  id = 1:10,
  minutos_lectura = c(15, 35, 25, 55, 20, 50, 30, 60, 40, 45),
  puntaje_comprension = c(50, 57, 66, 84, 59, 69, 68, 83, 55, 62),
  stringsAsFactors = FALSE
)

# 8. M10: encuesta_emprendimiento
encuesta_emprendimiento <- data.frame(
  id = 1:8,
  antiguedad_anos = c(1, 2, 3, 4, 5, 6, 7, 8),
  ventas_mensuales = c(100, 110, 120, 140, 180, 300, 800, 3000),
  stringsAsFactors = FALSE
)

# 9. M11: seguimiento (con missing en pares)
seguimiento <- data.frame(
  horas_estudio = c(2, 4, 3, 6, 5, 8, 7, 10, 9, 6),
  horas_sueno = c(8.1, 7.4, NA, 7.8, 6.9, 7.2, 6.5, NA, 7.0, 7.6),
  estres = c(3, 5, 4, 6, NA, 8, 5, 7, NA, 4),
  stringsAsFactors = FALSE
)

# 10. M12: encuesta_participacion
# N = 60; participacion (40 Participa, 20 No participa); transporte (15 Metro, 30 Bus, 15 Bicicleta)
set.seed(42)
encuesta_participacion <- data.frame(
  id = 1:60,
  participacion_organizacion = c(rep("Participa", 40), rep("No participa", 20)),
  transporte_campus = c(
    rep("Metro", 12), rep("Bus", 20), rep("Bicicleta", 8),
    rep("Metro", 3), rep("Bus", 10), rep("Bicicleta", 7)
  ),
  stringsAsFactors = FALSE
)

# 11. M12: encuesta_comunidad
# N = 80; zona (Norte, Centro, Sur); actividad (Alta, Media, Baja)
encuesta_comunidad <- data.frame(
  id = 1:80,
  zona_residencia = rep(c("Norte", "Centro", "Sur"), length.out = 80),
  actividad_comunitaria = rep(c("Alta", "Media", "Baja", "Media"), 20),
  stringsAsFactors = FALSE
)

# 12. M13: encuesta_vida_universitaria
# N = 48; 32 Diurna, 16 Vespertina
encuesta_vida_universitaria <- data.frame(
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

# 13. M13: encuesta_vinculos_barriales
# N = 40; ocupado (Sí/No); participa_vecinal_01 (1/0); confianza_comunitaria
encuesta_vinculos_barriales <- data.frame(
  id = 1:40,
  ocupado = c(rep("Sí", 28), rep("No", 12)),
  participa_vecinal_01 = c(rep(c(1, 0, 1, 1, 0, 1, 0), 4), rep(c(0, 1, 0), 4)),
  confianza_comunitaria = c(
    c(7, 8, 6, 9, 5, 8, 6, 7, 8, 9, 6, 7, 8, 6, 9, 7, 8, 5, 7, 8, 6, 9, 7, 8, 6, 7, 8, 6),
    c(5, 6, 4, 6, 5, 7, 4, 5, 6, 5, 6, 4)
  ),
  stringsAsFactors = FALSE
)
