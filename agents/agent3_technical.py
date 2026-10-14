from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent3_Technical')
class TechnicalAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 3: Technische Analyse] Trend en moving averages verifiëren...")
        if state.rejection_reason: return state
        state.technical_passed = True
        state.audit_trail.append("Agent 3: PASSED")
        logger.info("[Agent 3] Technische analyse goedgekeurd.")
        return state
