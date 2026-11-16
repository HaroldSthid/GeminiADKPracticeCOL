from family_routine.model import flash
from handoff_kit.agents import build_team
from handoff_kit.domains import load_domain

# Pick the case with HANDOFF_DOMAIN (default: company_orders); edit one file in handoff_kit/domains/.
coordinator, _coach = build_team(load_domain(), flash())
root_agent = coordinator
