# De la hoja de trabajo al prototipo: el prompt para una IA de código

Para quien **no programa** pero quiere llevar el taller a su empresa. Llenas la hoja de trabajo, se la pegas a una IA de código con este prompt, y la IA escribe el archivo del caso, lo valida y siembra los datos de ejemplo. Tú revisas el resultado con la lista del final.

> Si sabes usar un repositorio, la ruta directa es [`ADAPTA_A_TU_EMPRESA.md`](ADAPTA_A_TU_EMPRESA.md): hace lo mismo a mano.

---

## Qué necesitas

1. La hoja de trabajo llena: la Parte 2 de [`RETO_OPCION_A.md`](RETO_OPCION_A.md). Hay un ejemplo resuelto en su Parte 4.
2. Una herramienta de IA que pueda **editar archivos y ejecutar comandos** en tu computador (un asistente de código como Claude Code, o el modo agente de un editor). Un chat que solo responde texto no sirve: no puede crear el archivo ni probarlo.
3. El repositorio clonado con el entorno listo. Son los pasos de "Antes de empezar" de [`ADAPTA_A_TU_EMPRESA.md`](ADAPTA_A_TU_EMPRESA.md). Si no puedes hacerlos, pídele a una persona técnica de tu equipo que lo deje listo una vez.

## Cómo usarlo

1. Abre la herramienta de IA **dentro de la carpeta `adk-web`** del repositorio.
2. Copia el prompt de abajo y pégalo.
3. Reemplaza el bloque `[PEGA AQUÍ TU HOJA DE TRABAJO]` por tu hoja llena.
4. Responde las preguntas que te haga la IA, una a una. Si la hoja está incompleta, prefiere que pregunte a que invente.

---

## El prompt

````text
Eres un asistente de código. Tu tarea: convertir la hoja de trabajo de abajo en un caso de empresa
para este repositorio, creando UN solo archivo. Estás en la carpeta adk-web.

QUÉ ES ESTE REPOSITORIO
Un equipo de agentes de IA (Google ADK): un coordinador que reparte, tres áreas encadenadas que se
pasan el contexto, una bitácora SQLite que recuerda y un coach semanal. El motor está en handoff_kit/.
Cada caso se describe en un solo archivo de handoff_kit/domains/. No hay que tocar el motor.

PRIMERO LEE (no los modifiques)
- handoff_kit/domains/_template.py  (la plantilla comentada)
- handoff_kit/domains/company_orders.py  (un ejemplo completo y funcionando: imítalo en nivel de
  detalle y en idiomas)
- handoff_kit/domain.py  (las validaciones que tu archivo debe cumplir)

QUÉ HACER
1. Si la hoja está incompleta o ambigua, hazme UNA pregunta a la vez y espera mi respuesta.
   Si no puedes esperarme (no hay conversación), escribe tus preguntas en el reporte final y usa la
   opción más prudente: deja ese dato fuera en vez de inventarlo.
   Nunca inventes hechos de mi empresa (horarios, plazos, reglas, nombres, cifras). La única
   excepción son los 5 registros de ejemplo y los ejemplos dentro de las descripciones de los
   campos: son ficticios por diseño.
2. Propón un nombre corto para el caso: minúsculas, números y guion bajo, sin empezar por guion bajo
   (por ejemplo soporte_tickets). Dime cuál elegiste. Si ya existe un archivo con ese nombre en
   handoff_kit/domains/, no lo sobrescribas: propón otro nombre.
3. Crea handoff_kit/domains/<nombre>.py copiando la estructura de la plantilla.
4. Valídalo y pruébalo con los comandos de la sección VERIFICACIÓN.
5. Siembra los datos de ejemplo y dame el reporte final.

REGLAS DEL ARCHIVO (si no las cumples, el kit falla)
- Exactamente 3 áreas (stages) encadenadas, en el orden de la hoja, y exactamente 4 campos de bitácora
  (log_fields).
- Prohibido escribir llaves { } en CUALQUIER texto: el motor las lee como variables y falla.
- stage.key y los nombres de campo: en inglés, minúsculas con guion bajo, únicos. Un campo no puede
  llamarse subject ni date, ni igual que la key de un área.
- Idiomas, como en company_orders.py: en español, las claves y los valores de context, sample_entries,
  name, coordinator_name y title (el nombre de cada área tal como está en mi hoja); en inglés,
  instruction, receives, delivers, coordinator_role, subject_label, coach_goal_hint,
  forbidden_inventions, las descripciones de los campos, los comentarios y el docstring del archivo.
  output_language = "es-LA".
- Nombres de los 4 campos de la bitácora: en inglés, minúsculas con guion bajo, derivados de los
  nombres de mi hoja (por ejemplo "ticket y cliente" -> ticket_and_customer).
- context: solo hechos que yo di en la hoja, cada entrada en una o dos frases cortas. Los plazos y
  horarios de la hoja (por ejemplo "respuesta en 4 horas") son hechos del contexto: ponlos ahí.
- NO añadas reglas de negocio, políticas ni pasos que yo no haya mencionado en la hoja, ni en una
  instruction ni en ningún otro texto. Si una instruction necesita una regla que no está, pregúntame
  o déjala fuera. Cada instruction debe decir qué verifica el área, qué escribe y qué marca, usando
  solo lo que dice la hoja; si falta un dato, debe pedirlo, no suponerlo. Pedir un dato que falta
  nunca cuenta como una regla nueva: siempre se permite.
- forbidden_inventions: concreta y específica de mi empresa. Nombra todo lo que la hoja dice que el
  agente no debe inventar, y lo MÁS CARO que podría inventar. Si no queda claro cuál es lo más caro,
  cúbrelas todas y dímelo. Una frase genérica como "no inventes datos" no sirve.
- La decisión que la hoja dice que sigue siendo de una persona va en la instruction del área que
  podría tomarla (que debe marcarla para que la decida una persona, sin aprobarla ni prometerla) y
  también en forbidden_inventions.
- sample_entries: 5 registros ficticios, days_ago de 5 a 1, con un PATRÓN ESCONDIDO que el coach
  descubra al cruzar varios registros. La causa del patrón la eliges tú, ficticia y coherente con lo
  que busca el coach (por ejemplo un canal o un horario); no hace falta que yo te la dé.
  No escribas la causa del patrón dentro del texto de un campo:
  el patrón debe verse al comparar, no estar escrito en una frase. Usa solo los 4 campos.
  Pon primero el campo que identifica el caso. El subject es el identificador tal como lo diría mi
  gente ("481", no "TCK-481"), y debe aparecer igual dentro de ese primer campo (por ejemplo
  "ticket 481, cliente Rojas").
- Datos ficticios en los ejemplos, que son datos de relleno y no hechos de mi empresa. No uses nombres
  ni datos reales de personas o clientes.

LÍMITES
- Crea o edita SOLO handoff_kit/domains/<nombre>.py. No modifiques el motor, otros dominios, las
  pruebas ni ningún otro archivo. Si crees que hay que cambiar algo más, detente y dímelo.
- No leas, muestres ni copies el archivo .env ni ninguna clave.
- No hagas commit ni push. No arranques adk web.

VERIFICACIÓN (ejecuta cada comando y reporta el resultado real; sustituye <nombre>)
1. python -c "from handoff_kit.domains import load_domain; load_domain('<nombre>'); print('OK')"
2. python -m pytest -q   (todas las pruebas deben pasar; pueden salir avisos "DeprecationWarning"
   de ADK: son normales y no son fallos)
3. python -m handoff_kit.demo_seed --reset --domain <nombre>
   (borra los registros de ESE caso: es seguro si el caso es nuevo; si ya tenía registros, pregúntame antes)
4. python -m handoff_kit.demo_seed --domain <nombre>   (debe decir que agregó 5 registros)
Si un comando falla, corrige tu archivo y repite. No des por terminado nada que no hayas ejecutado.
Ojo: que las pruebas pasen solo demuestra que el kit carga tu archivo, no que su contenido sea
verdad. Por eso mi revisión de lo que escribiste importa.

REPORTE FINAL, en español sencillo, sin jerga
- El nombre del archivo creado.
- Un resumen de una línea por área y por campo de la bitácora.
- Los supuestos que tuviste que hacer (si hay alguno, dilo claramente).
- Una lista aparte de CUALQUIER regla, paso o detalle que escribiste y que NO estaba en mi hoja.
  Si no hay ninguno, escribe "ninguno".
- Las preguntas que no pudiste hacerme, si las hubo.
- Qué debo revisar yo a mano (mi contexto, la regla de qué no inventar y el patrón de los ejemplos).
- Los comandos para arrancar: definir HANDOFF_DOMAIN=<nombre> y ejecutar adk web.

MI HOJA DE TRABAJO
[PEGA AQUÍ TU HOJA DE TRABAJO]
````

---

## Cuando la IA termina: revisión humana (10 min)

La IA puede escribir un archivo que **funciona** pero que **no es verdad para tu empresa**. Esta revisión es tuya.

- [ ] **El contexto es real.** Lee cada entrada de `context`: los agentes la toman por cierta. Si hay un horario, un plazo o una regla que no dijiste, bórralo.
- [ ] **La regla de qué no inventar nombra lo más caro.** Si tu mayor riesgo es prometer una fecha, debe decir "fechas" con todas sus letras.
- [ ] **Las áreas hacen lo que tu gente hace.** Lee la instrucción de cada una: ¿verifica lo que de verdad verifica esa área?
- [ ] **No hay reglas que tú no dijiste.** Compara la instrucción de cada área con tu hoja y con la lista "que NO estaba en mi hoja" del reporte. Una regla inventada suena razonable y es la más difícil de notar. Bórrala si no es tuya.
- [ ] **Los 5 registros de ejemplo cuentan una historia.** ¿Se ve el patrón al comparar varios registros? Si la causa está escrita tal cual en un campo, el coach no la descubre, la lee: pídele a la IA que la quite del texto. Y si no se ve, que la haga más evidente.
- [ ] **Todo es ficticio.** Ningún nombre ni dato real de clientes.
- [ ] **Pruébalo con los 3 mensajes** del paso 6 de [`ADAPTA_A_TU_EMPRESA.md`](ADAPTA_A_TU_EMPRESA.md) y revisa la pestaña Events.

## Si algo falla

| Síntoma | Qué hacer |
| --- | --- |
| La IA propone modificar el motor | Dile que no: el caso entra en un solo archivo. Si insiste, tu traspaso probablemente es demasiado grande: acótalo a 3 áreas y 4 campos |
| La IA inventó datos de tu empresa | Pídele que los quite y que pregunte lo que falte |
| La validación falla | Pega el mensaje de error a la IA. Son claros, por ejemplo `Remove the curly braces from ...` |
| Al probar salen avisos `DeprecationWarning` | Son normales: los emite ADK y no son un fallo. Lo que importa es que diga `passed` |
| El coach no encuentra el patrón | Los 5 ejemplos no lo muestran con claridad: pide casos malos que compartan una causa evidente |
| No sabes qué le falta a tu hoja | Compárala con el ejemplo resuelto de la Parte 4 de `RETO_OPCION_A.md` |

## Qué es y qué no es esto

- **Es** una forma de pasar de una hoja de papel a un prototipo que corre, sin escribir código.
- **No es** una integración con tus sistemas, y la IA que escribe el archivo no lo conoce a fondo: por eso existe la revisión humana de arriba.
- **No reemplaza** la decisión de una persona. Los agentes proponen y registran.
