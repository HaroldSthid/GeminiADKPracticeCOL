# Rutina familiar con ADK Web

Segunda versión del sistema: el mismo equipo de agentes del notebook de Colab, pero como proyecto de **Google ADK** que corre en tu computador con `adk web` (interfaz de chat + visor de eventos). Los datos del ejemplo son ficticios (Luna, Maria, Joao): cámbialos en `family_routine/profile.py`.

> Esta versión **no se puede alojar en GitHub Pages**: ADK web es un servidor Python. Cada persona lo corre en su máquina con su propia clave de Gemini.

## Qué hay aquí

| Carpeta | Agente | Para qué sirve |
| --- | --- | --- |
| `family_coordinator/` | Coordinador | **Empieza por aquí.** Decide a qué especialista llamar y guarda el registro del día |
| `family_routine/` | Rutina → Comidas → Actividades | Cadena fija de 3 agentes (`SequentialAgent`) que se pasan el resultado por estado de sesión |
| `family_coach/` | Coach semanal | Lee los registros guardados y recomienda ajustes para la próxima semana |

## Los 4 componentes de un sistema de agentes

| Componente | Dónde está |
| --- | --- |
| **Modelo** | `gemini-flash-latest` en cada `agent.py` |
| **Instrucción** | El rol, las reglas y el formato de cada agente (el coordinador además tiene reglas de enrutamiento) |
| **Herramientas** | `save_day_log` y `get_recent_logs` (`family_routine/tools.py`) y los especialistas expuestos como `AgentTool` |
| **Memoria** | Estado de sesión (`routine`, `meals`) y una base **SQLite** (`data/family.db`) con los registros diarios, compartida entre los agentes |

## Cómo correrlo

Necesitas Python 3.10 o superior y una clave gratuita de [Google AI Studio](https://aistudio.google.com/app/apikey).

```bash
cd adk-web
python -m venv .venv
# Windows:      .venv\Scripts\Activate.ps1
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # Windows: copy .env.example .env  -> luego pega tu GOOGLE_API_KEY
python -m pytest            # pruebas de las herramientas, sin clave
adk web                     # abre http://localhost:8000 y elige family_coordinator
```

## Qué probar

En `family_coordinator`, en este orden:

1. *"Organiza el día: despertó a las 6:40, ayer la siesta fue corta, hace sol."* → llama a rutina, comidas y actividades.
2. *"¿Qué cocino con huevos y espinaca?"* → llama solo al especialista de comidas.
3. *"Guarda el registro de hoy: despertó a las 6:40, siesta corta de 40 minutos, buen humor."* → guarda en SQLite.
4. En otra sesión: *"Planifica el día."* → la rutina ya sabe cómo fue el día anterior.
5. Elige `family_coach` y pide: *"Haz la revisión semanal. Meta: siestas más largas."*

Mira la pestaña de eventos: ahí se ven las llamadas a herramientas y el estado que viaja entre agentes.

## Límites a tener presentes

- La memoria es un diario ordenado por fecha, no memoria semántica.
- Está atada a `CHILD_NAME` de `profile.py`: es una sola familia.
- Tu clave se queda en tu `.env`. Si la pegas en un chat o la subes por error, revócala y crea otra.
- `data/` y `.env` están en `.gitignore`: los datos de tu familia no deberían subirse a un repositorio público.
