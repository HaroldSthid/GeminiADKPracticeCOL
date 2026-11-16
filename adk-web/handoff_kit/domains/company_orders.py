"""Worked example: a delivery-address change gets lost between Sales, Logistics and Service.

All company data below is fictional. Context facts and sample logs are in Spanish because
the workshop audience reads them in the chat; instructions stay in English.
"""

from ..domain import Domain, LogField, SampleEntry, Stage

DOMAIN = Domain(
    name="Cambios de dirección de entrega",
    output_language="es-LA",
    context={
        "Empresa": "Distribuidora Andina Demo S.A.S., distribuidora mediana de productos de oficina (empresa ficticia).",
        "Horario": "Ventas y Servicio atienden de 8:00 a 18:00. Logística despacha los pedidos a las 15:00.",
        "SLA": "Un cambio de dirección solo es posible si el pedido aún no fue despachado.",
        "Canales": "El cliente puede pedir el cambio por el sistema, por correo o por teléfono.",
        "Problema": "Los cambios de dirección se pierden entre Ventas, Logística y Servicio al Cliente.",
    },
    coordinator_name="Despachador Andino",
    coordinator_role=(
        "You coordinate three areas (Sales, Logistics, Customer Service) so that a customer's "
        "delivery-address change is received, passed on and confirmed without getting lost."
    ),
    stages=(
        Stage(
            key="sales",
            title="Sales",
            receives="the customer's request to change the delivery address of an order",
            delivers="a clear change ticket: order, customer, new address, channel and time received",
            instruction=(
                "Capture the change exactly as the customer stated it: order, customer, new address, "
                "channel (system, email or phone) and time received. Check whether the order is still "
                "before the 15:00 dispatch cut-off. Ask for any missing data instead of guessing. "
                "Write a short handoff note for Logistics with the received time highlighted."
            ),
        ),
        Stage(
            key="logistics",
            title="Logistics",
            receives="the change ticket from Sales",
            delivers="a decision on whether the change can still be applied and the next step",
            instruction=(
                "Read the Sales ticket. Decide, only from the facts given, whether the order was already "
                "dispatched. If not, say the address must be updated and by whom. If it was dispatched, "
                "say the change cannot be applied normally and propose the options to check (carrier "
                "redirect or re-delivery). Flag when the change reached you late."
            ),
        ),
        Stage(
            key="service",
            title="Customer Service",
            receives="the Logistics decision on the address change",
            delivers="a clear message to the customer and a follow-up note",
            instruction=(
                "Write a short, honest message to the customer with the real status of the change. "
                "Confirm the change only if the Logistics decision says it was applied. Otherwise explain "
                "what is pending and what the customer can expect. Add a one-line follow-up note listing "
                "who must check what."
            ),
        ),
    ),
    log_fields=(
        LogField("order_and_customer", "Order number and customer, e.g. 'pedido 1042, cliente Rojas'."),
        LogField("requested_change", "What the customer asked to change, e.g. 'nueva dirección: Calle 10 # 5-20'."),
        LogField("received_by_and_when", "Who received the request, through which channel and at what time."),
        LogField("status", "Where the change stands now, e.g. 'applied on time' or 'informed late'."),
    ),
    subject_label="order",
    coach_goal_hint=(
        "address changes that reach Logistics late, and what they have in common "
        "(time received, channel, who received them)"
    ),
    forbidden_inventions=(
        "Never invent delivery dates. Never confirm a change the log does not record. "
        "Never invent customer names, order numbers or addresses."
    ),
    sample_entries=(
        SampleEntry(5, "1001", {
            "order_and_customer": "pedido 1001, cliente Rojas",
            "requested_change": "Cambio a Calle 10 # 5-20",
            "received_by_and_when": "Ventas, por el sistema, 9:15",
            "status": "aplicado a tiempo",
        }),
        SampleEntry(4, "1007", {
            "order_and_customer": "pedido 1007, cliente Gómez",
            "requested_change": "Cambio a Carrera 7 # 40-12",
            "received_by_and_when": "Ventas, por teléfono, 15:40",
            "status": "informado tarde / pedido ya despachado",
        }),
        SampleEntry(3, "1013", {
            "order_and_customer": "pedido 1013, cliente Torres",
            "requested_change": "Cambio a Avenida 30 # 12-08",
            "received_by_and_when": "Ventas, por el sistema, 10:05",
            "status": "aplicado a tiempo",
        }),
        SampleEntry(2, "1019", {
            "order_and_customer": "pedido 1019, cliente Mejía",
            "requested_change": "Cambio a Calle 50 # 8-33",
            "received_by_and_when": "Ventas, por teléfono, 16:20",
            "status": "informado tarde / pedido ya despachado",
        }),
        SampleEntry(1, "1024", {
            "order_and_customer": "pedido 1024, cliente Vargas",
            "requested_change": "Cambio a Carrera 15 # 22-47",
            "received_by_and_when": "Ventas, por el sistema, 8:50",
            "status": "aplicado a tiempo",
        }),
    ),
)
