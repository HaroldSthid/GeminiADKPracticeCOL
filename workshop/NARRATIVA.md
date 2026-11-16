# Taller: "Los lunes empiezan de cero" — Agentes de IA contra el traspaso de información entre áreas

Taller práctico de 90 minutos para público no técnico. Los asistentes ven un equipo de agentes de IA coordinarse y luego lo corren en su propio computador.

> Estado: borrador. Los pasos marcados con **[verificar]** no se han probado todavía en el entorno del taller.

---

## 1. La idea central

**Dolor:** en casi toda empresa, la información se pierde cuando pasa de un área a otra. Ventas promete algo, logística no se entera, servicio al cliente recibe el reclamo y nadie recuerda qué pasó la semana pasada. Cada lunes la operación arranca de cero.

**Mensaje del taller:** un equipo de agentes de IA no reemplaza a las áreas. Hace lo que hoy hacen mal las personas con prisa: pasar el contexto completo de una área a la siguiente y dejar memoria de lo que ocurrió.

**Frase de apertura:** "Hoy van a ver cómo una operación deja de depender de que alguien se acuerde".

## 2. La analogía: una familia es una operación pequeña

El caso del taller es la rutina diaria de una familia con una niña pequeña. Es un caso cercano para cualquiera, no expone datos de ninguna empresa y tiene el mismo problema de fondo que una compañía.

| En la familia | En la empresa | Qué hace |
| --- | --- | --- |
| **Coordinador** | Jefe de operaciones | Recibe el pedido, decide a quién llamar y entrega una sola respuesta |
| **Rutina → Comidas → Actividades** | Ventas → Logística → Servicio | Cada área recibe lo que dejó la anterior, sin repetirle la historia |
| **Diario en SQLite** | Bitácora de turno | Lo que pasó ayer queda guardado y hoy se usa |
| **Coach semanal** | Revisión semanal de operaciones | Lee la bitácora, encuentra patrones y propone ajustes |

### Los 4 componentes de cualquier agente

| Componente | Lo que significa para una persona de negocio | Dónde está en el código |
| --- | --- | --- |
| **Modelo** | El cerebro del empleado | `gemini-flash-latest` |
| **Instrucción** | Su descripción de cargo y sus reglas | Texto `instruction` de cada `agent.py` |
| **Herramientas** | Los sistemas a los que tiene acceso (ERP, CRM, hojas) | `save_day_log`, `get_recent_logs` y los especialistas como `AgentTool` |
| **Memoria** | La bitácora compartida | Base SQLite `data/family.db` |

## 3. Guion por bloques (90 min)

### Bloque 1 — El dolor (10 min)
- Contar una historia corta de traspaso fallido. Ejemplo: "Un cliente pide un cambio de dirección. Ventas lo anota, logística no lo ve, el pedido sale al lugar equivocado y servicio al cliente se entera por la queja".
- Pregunta a la sala: "¿En qué traspaso de su empresa se pierde más información?". Dejar que 3 o 4 personas respondan y anotar las respuestas, se usan en el bloque 5.

### Bloque 2 — La analogía y los 4 componentes (10 min)
- Mostrar las dos tablas de la sección 2. No explicar código.
- Mensaje: "El jefe de operaciones no hace el trabajo, decide quién lo hace y junta las respuestas".

### Bloque 3 — Demo en vivo (10 min)
Solo dos momentos, con `family_coordinator` en `adk web` (http://localhost:8000):

1. **El traspaso funciona.** Escribir: *"Organiza el día: despertó a las 6:40, ayer la siesta fue corta, hace sol."*
   - Señalar en la pestaña de eventos cómo se llama a rutina, luego a comidas y luego a actividades.
   - Señalar que el plan ya considera la siesta corta de ayer: el contexto viajó entre áreas.
2. **La memoria cambia el resultado.** *(Verificado: el plan de la sesión nueva mencionó la siesta corta guardada en la sesión anterior. Quien lee la memoria es `routine_planner`, no el coordinador: abrir su detalle en la pestaña de eventos.)*
   - Escribir: *"Guarda el registro de hoy: despertó a las 6:40, siesta corta de 40 minutos, buen humor."*
   - Abrir una sesión nueva y escribir: *"Planifica el día."*
   - La rutina debe mencionar lo que pasó el día anterior sin que nadie se lo repita. Este es el momento central del taller: es el lunes que ya no empieza de cero.

3. **La memoria encuentra patrones.** Con la base vacía no hay nada que analizar, así que antes de este momento se cargan 5 días ficticios desde `adk-web/`:

   ```bash
   python -m family_routine.demo_seed          # agrega 5 días de registros ficticios
   python -m family_routine.demo_seed --reset  # borra todo y deja la base vacía
   ```

   Luego, en `family_coach`, escribir: *"Haz la revisión semanal. Meta: siestas más largas."*
   - Los datos tienen un patrón escondido: las siestas son largas los días con paseo en la mañana y cuento en cuarto oscuro, y cortas los días sin eso. El coach lo encuentra: *(verificado)* separó los días de siesta de unas 2 horas (10, 12 y 14) de los de 40 a 45 minutos (11 y 13) y los atribuyó al ritual, al cuarto en penumbra y al auto. Con el prompt ajustado habla de "patrón alternado más que un progreso continuo", cita las fechas y valores, marca la causa como hipótesis y, con un solo registro, avisa que el análisis es preliminar. Sin ese ajuste decía "progreso notable" e inventaba desafíos (por ejemplo, la carga del cuidador).
   - Idea para el público: "la bitácora es lo que hace que la IA vea lo que a nosotros se nos pasa".

Consejo: las respuestas son largas. No las lean enteras, señalen una sola frase que demuestre el contexto heredado.

### Bloque 4 — Manos a la obra (30 min)
Los asistentes repiten la demo en su máquina. Requisitos previos (ver sección 4).

```bash
git clone https://github.com/HaroldSthid/GeminiADKPracticeCOL.git
cd GeminiADKPracticeCOL/adk-web
python -m venv .venv
# Windows:      .venv\Scripts\Activate.ps1
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
# Windows:      copy .env.example .env
# macOS/Linux:  cp .env.example .env
# Abrir .env y pegar la GOOGLE_API_KEY
python -m pytest        # debe decir "9 passed"
adk web                 # abrir http://localhost:8000 y elegir family_coordinator
```

**Puntos de control:**
1. `pytest` pasa 9 de 9 (sin clave): el entorno está bien.
2. `adk web` abre y lista 3 agentes: el servidor está bien.
3. El primer mensaje de la demo responde: la clave está bien.

Quien no logre instalar usa el notebook de Colab de la raíz del repo, que corre en el navegador sin instalar nada.

### Bloque 5 — Reto: de la familia a su empresa (20 min)
Cada persona o equipo elige un traspaso de la lista del bloque 1 y lo traduce a la estructura del taller:

| Pregunta | Ejemplo |
| --- | --- |
| ¿Quién es el coordinador? | Jefe de operaciones |
| ¿Cuáles son las 3 áreas encadenadas? | Ventas → Logística → Servicio |
| ¿Qué debe recordar la bitácora? | Cambios de dirección, reclamos, promesas al cliente |
| ¿Qué revisaría el coach cada semana? | Los reclamos que se repiten |

**Decisión: se usa la opción A.** El material está en [`RETO_OPCION_A.md`](RETO_OPCION_A.md): guía de tiempos, hoja de trabajo para imprimir, preguntas de revisión entre equipos y un ejemplo resuelto.

**Para quien quiere llevárselo a su empresa:** quien sabe usar un repositorio sigue [`ADAPTA_A_TU_EMPRESA.md`](ADAPTA_A_TU_EMPRESA.md): copia una plantilla, edita un solo archivo y lo corre con `adk web` en unos 30 minutos. Quien no programa llena la hoja de trabajo y se la entrega, junto con el prompt de [`PROMPT_PARA_IA_DE_CODIGO.md`](PROMPT_PARA_IA_DE_CODIGO.md), a una IA de código que escribe ese archivo por él; después revisa el resultado con la lista que trae el mismo documento.

**Nota para quien facilita:** el demo de la familia sigue atado a su caso (`CHILD_NAME` y un diario de despertar, siesta y ánimo), así que durante el taller el reto se hace en papel. El código para llevarlo a una empresa ya existe aparte: `adk-web/handoff_kit/` es un motor genérico y `adk-web/ops_coordinator/` es la app que `adk web` lista, con el caso de empresa de ejemplo en `handoff_kit/domains/company_orders.py`. Eso es lo que usa quien sigue la guía técnica de arriba, fuera del tiempo del reto.

### Bloque 6 — Cierre (10 min)
- Cada equipo cuenta en una frase: "El traspaso que atacaría es ____ y la bitácora guardaría ____".
- Tres ideas para llevarse:
  1. Un agente es un modelo, unas reglas, unas herramientas y una memoria.
  2. El valor está en el traspaso de contexto, no en que la IA sea más lista.
  3. Sin memoria compartida, cada día empieza de cero.
- Llamado a la acción: el repo es público, pueden clonarlo y adaptarlo.

## 4. Antes del evento (mensaje para los asistentes)

> Para el taller necesitan: un computador con **Python 3.10 o superior** y una **clave gratuita de Google AI Studio** (https://aistudio.google.com/app/apikey). Instalen Python y generen la clave antes de llegar. No compartan la clave por chat ni la suban a ningún repositorio.

## 5. Riesgos y qué hacer

| Riesgo | Qué hacer |
| --- | --- |
| Muchas personas en el mismo wifi, con límites de las claves gratuitas | Pedir que cada quien use su propia clave y tener un video corto del demo como respaldo |
| `ReadError` al llamar a Gemini | Es un corte de red, no un fallo de los agentes. Repetir el mensaje en la misma sesión |
| No instalaron Python | Usar el notebook de Colab |
| La clave quedó expuesta en pantalla | Revocarla y crear otra |
| Las respuestas largas pierden a la sala | Señalar una sola frase clave en vez de leer todo |

## 6. Pendientes antes del evento
- [x] Verificar el flujo de memoria entre sesiones (guardar registro y planificar en otra sesión).
- [x] Verificar la revisión semanal con `family_coach`. Con un solo registro el análisis es débil y generaliza a partir de un dato; para mostrarlo bien hacen falta 4 o 5 días de registros ficticios.
- [x] Preparar la base: vacía para la demo de memoria y sembrada solo para el coach (`python -m family_routine.demo_seed`, con `--reset` para vaciarla).
- [x] Probar la revisión semanal con los datos sembrados y confirmar que el coach encuentra el patrón.
- [ ] Antes del evento, correr `python -m family_routine.demo_seed --reset` para dejar `data/family.db` vacía.
- [x] Decidir entre la opción A y la B del bloque 5: el reto del taller es en papel (A) y el código para empresas queda aparte en `handoff_kit/`.
- [x] Probar `PROMPT_PARA_IA_DE_CODIGO.md` con una IA de código y una hoja de un caso distinto (soporte de tickets). Salió un archivo válido, y las dos pruebas llevaron a corregir el prompt: reglas inventadas y un patrón escrito en vez de escondido.
- [ ] Probar `PROMPT_PARA_IA_DE_CODIGO.md` con una persona no técnica real, con su propia hoja y su propia herramienta de IA.
- [ ] Probar `ADAPTA_A_TU_EMPRESA.md` de principio a fin con una persona técnica en una máquina limpia, con un caso propio y con Gemini de verdad.
- [ ] Imprimir la hoja de trabajo de `RETO_OPCION_A.md` (una por equipo) y probar el reto con 2 o 3 personas de prueba.
- [ ] Grabar el video de respaldo del demo.
- [ ] Probar el taller completo en una máquina limpia (Windows y macOS si aplica).
