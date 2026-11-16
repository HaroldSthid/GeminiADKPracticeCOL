# Adapta esto a tu empresa en 30 minutos

Guía para quien sabe usar un repositorio de GitHub. Al terminar tendrás un prototipo propio del equipo de agentes: un coordinador, tres áreas que se pasan el contexto, una bitácora que recuerda y un coach semanal, todo con el caso de tu empresa.

Solo editas **un archivo**. No tocas el motor.

> Si no programas, llena primero la hoja de trabajo de [`RETO_OPCION_A.md`](RETO_OPCION_A.md). Esa hoja es exactamente lo que se pide en el paso 2. Y si prefieres que lo escriba una IA de código, usa el prompt de [`PROMPT_PARA_IA_DE_CODIGO.md`](PROMPT_PARA_IA_DE_CODIGO.md).

---

## Antes de empezar (5 min)

Necesitas Python 3.10 o superior y una clave gratuita de [Google AI Studio](https://aistudio.google.com/app/apikey).

**En Windows, clona en una carpeta de ruta corta**, por ejemplo `C:\taller`. Las dependencias de Google traen archivos con rutas larguísimas y, en una carpeta muy anidada (como `Documentos\Mis proyectos\...`), `pip` falla con `WinError 206: el nombre del archivo o la extensión es demasiado largo`.

```bash
git clone https://github.com/HaroldSthid/GeminiADKPracticeCOL.git
cd GeminiADKPracticeCOL/adk-web
python -m venv .venv
```

### Activa el entorno y comprueba que de verdad quedó activo

```bash
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Comprueba que está activo antes de instalar nada. La ruta que imprime este comando debe terminar en `.venv`:

```bash
python -c "import sys; print(sys.prefix)"
```

**Si PowerShell dice que "la ejecución de scripts está deshabilitada"**, la activación falló y `python` sigue siendo el de todo el sistema. No instales nada así: las dependencias quedarían en tu Python global. Tienes dos salidas:

- **No actives el entorno y usa su Python directamente.** En esta guía, donde veas `python` escribe `.venv\Scripts\python.exe`, y donde veas `adk` escribe `.venv\Scripts\adk.exe`. Funciona siempre, con o sin esa restricción.
- O habilita los scripts una sola vez para tu usuario con `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` y vuelve a activar.

### Instala y prueba

```bash
pip install -r requirements.txt
# Windows: copy .env.example .env     macOS/Linux: cp .env.example .env
# Abre .env y pega tu GOOGLE_API_KEY
python -m pytest        # todas las pruebas deben pasar
```

Si `pytest` no pasa, no sigas: el entorno tiene un problema y es más barato arreglarlo ahora.

**Usa datos ficticios** mientras pruebas. No pegues nombres ni datos reales de clientes.

---

## Paso 1. Copia la plantilla (1 min)

Elige un nombre corto para tu caso: solo letras minúsculas, números y guion bajo, y que no empiece por guion bajo. Ejemplo: `soporte_tickets`.

```bash
# macOS/Linux
cp handoff_kit/domains/_template.py handoff_kit/domains/soporte_tickets.py
# Windows (PowerShell)
Copy-Item handoff_kit\domains\_template.py handoff_kit\domains\soporte_tickets.py
```

Desde aquí solo editas `handoff_kit/domains/soporte_tickets.py`. Cada campo tiene un comentario que explica qué escribir. Hay un ejemplo completo y funcionando en `handoff_kit/domains/company_orders.py`.

## Paso 2. Llénala desde tu hoja de trabajo (15 min)

| Qué llenar en el archivo | De dónde sale en la hoja |
| --- | --- |
| `name` | El traspaso elegido |
| `context` | Qué hace la empresa, horarios, plazos y reglas. **Solo hechos reales**: los agentes los toman por verdad |
| `coordinator_name` y `coordinator_role` | El coordinador (el jefe que reparte) |
| `stages` (exactamente 3) | Las 3 áreas encadenadas: qué recibe, qué entrega y las reglas de su trabajo |
| `log_fields` (exactamente 4) | Los 4 campos de la bitácora |
| `subject_label` | Sobre qué es cada registro: pedido, caso, ticket |
| `coach_goal_hint` | Qué patrón busca el coach cada semana |
| `forbidden_inventions` | La regla "qué no debe inventar el agente" |
| `sample_entries` (5 días) | Cinco registros ficticios con un patrón escondido que el coach pueda descubrir |

Reglas que evitan los errores más comunes:
- **No escribas llaves `{ }` en ningún texto.** ADK las lee como variables y falla en plena demo. El kit lo detecta y te lo avisa.
- **Un solo traspaso.** Si no te cabe en 3 áreas y 4 campos, el traspaso es demasiado grande: acótalo.
- **Escribe en `forbidden_inventions` lo más caro que el agente podría inventar** en tu empresa (una fecha prometida, un monto, un nombre).
- **El identificador de `sample_entries` debe ser como lo escribe tu gente**: si dicen "ticket 481", usa `"481"`, no `"TCK-481"`. El agente lo guarda tal como lo escribe el usuario.

## Paso 3. Valídala sin gastar la clave (2 min)

```bash
python -c "from handoff_kit.domains import load_domain; load_domain('soporte_tickets'); print('OK')"
```

Si algo está mal, el mensaje dice qué corregir:

| Mensaje | Qué pasó |
| --- | --- |
| `Remove the curly braces from ...` | Escribiste `{` o `}` en un texto |
| `A domain needs exactly 3 stages` / `4 log fields` | Faltan o sobran áreas o campos |
| `Log field '...' is reserved` | Un campo se llama `subject` o `date` |
| `Sample entry ... uses undeclared fields` | Un registro de ejemplo usa un campo que no declaraste |
| `Unknown domain` | El nombre del archivo no coincide con el que pasaste |

## Paso 4. Prepara la bitácora de tu caso (2 min)

Cada caso tiene su propia bitácora, en `data/handoff_<tu_caso>.db`, así que no se mezcla con el ejemplo ni con otros casos.

```bash
python -m handoff_kit.demo_seed --domain soporte_tickets            # siembra tus 5 días
```

Para empezar otra vez con esa misma bitácora vacía:

```bash
python -m handoff_kit.demo_seed --reset --domain soporte_tickets    # la vacía
python -m handoff_kit.demo_seed --domain soporte_tickets            # la vuelve a sembrar
```

La semilla nunca crea un registro de hoy, para que puedas guardar el de hoy en vivo. Y siempre pasa `--domain`: sin él, la semilla usa el caso de ejemplo.

## Paso 5. Arranca el servidor con tu caso (1 min)

```bash
# macOS/Linux
export HANDOFF_DOMAIN=soporte_tickets
# Windows (PowerShell)
$env:HANDOFF_DOMAIN = "soporte_tickets"

adk web
```

Abre http://localhost:8000 y elige **`ops_coordinator`** en el selector. La app se llama igual para todos los casos: lo que cambia es el contenido.

**Cada vez que edites el archivo, reinicia `adk web`.** ADK guarda los agentes en memoria y no ve los cambios hasta reiniciar.

## Paso 6. Pruébalo (4 min)

Escribe estos tres mensajes, adaptados a tu caso. Abre la pestaña **Events** para ver quién llama a quién.

| # | Qué escribes | Qué debes ver |
| --- | --- | --- |
| 1 | Un caso concreto de tu traspaso y *"haz el flujo completo"* | El coordinador llama a las 3 áreas en orden. La regla o el plazo que escribiste en `context` aparece en la respuesta |
| 2 | *"Guarda el registro: ..."* con los datos del caso | Llama a `save_log`. Lo que no dijiste queda como `unknown` y el identificador se guarda tal como lo escribiste |
| 3 | *"Haz la revisión semanal. Meta: ..."* | El coach cita fechas e identificadores de tus registros y encuentra el patrón que escondiste |

---

## Cuando algo sale mal

| Síntoma | Causa probable | Qué hacer |
| --- | --- | --- |
| El coach no encuentra tu patrón | El patrón en `sample_entries` es débil o no hay 4 o 5 días | Hazlo más evidente: que los casos malos compartan una causa clara |
| Aparecen datos de otro caso | Forzaste una misma base para varios casos con la variable `HANDOFF_DB`, o sembraste sin `--domain` | Quita `HANDOFF_DB` y repite el paso 4 con `--domain` |
| El coach dice que no hay registros | Sembraste un caso y arrancaste el servidor con otro `HANDOFF_DOMAIN` | Usa el mismo nombre en la semilla y en `HANDOFF_DOMAIN` |
| Tus cambios no aparecen | El servidor sigue con la versión vieja | Reinicia `adk web` |
| El agente inventa un dato | `forbidden_inventions` es vago | Nómbralo con precisión: "Nunca inventes fechas de entrega ni montos" |
| `WinError 206` o "nombre de archivo demasiado largo" al instalar | Clonaste en una carpeta de ruta muy larga | Clona de nuevo en una ruta corta como `C:\taller` y repite la instalación |
| "La ejecución de scripts está deshabilitada" al activar el entorno | PowerShell bloquea `Activate.ps1` por defecto | Usa `.venv\Scripts\python.exe` directamente, como dice "Antes de empezar" |
| `ModuleNotFoundError: No module named 'google'` | El entorno no tiene las dependencias: se instalaron en otro Python | Instala con `.venv\Scripts\python.exe -m pip install -r requirements.txt` |
| `ReadError` al llamar a Gemini | Corte de red, no un fallo de los agentes | Repite el mensaje en la misma sesión |
| Error de clave o cuota | La clave falta, está mal pegada o llegó a su límite gratuito | Revisa `.env`, revócala y crea otra si se expuso |

## Qué es y qué no es esto

- **Es** un prototipo para probar si el traspaso se puede ordenar con agentes y una bitácora compartida.
- **No es** una integración con tus sistemas. Conectarlo a un ERP o a un CRM es un proyecto con el equipo de TI.
- **No decide por ti.** Los agentes proponen y registran. Las decisiones críticas siguen siendo de una persona, y por eso la hoja de trabajo pregunta cuáles son.
- **No reemplaza revisar.** El modelo puede rellenar con frases agradables. Contrasta siempre el análisis del coach con la bitácora.
