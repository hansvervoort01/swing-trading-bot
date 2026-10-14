from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent2_Macro')
class MacroAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 2: Macro & Circuit Breaker] Controleren marktconditie...")
        if state.rejection_reason: return state
        if state.macro_status == 'ROOD':
            state.rejection_reason = "Afgekeurd Agent 2: Macro lockdown."
            state.audit_trail.append("Agent 2: FAILED")
            return state
        state.macro_passed = True
        state.audit_trail.append("Agent 2: PASSED")
        logger.info("[Agent 2] Marktconditie goedgekeurd (GROEN).")
        return state
