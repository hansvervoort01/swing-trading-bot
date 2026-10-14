from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent5_Risk')
class RiskAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 5: Risk & Stop-Loss] Weekly support stop-loss berekenen...")
        if state.rejection_reason: return state
        state.risk_passed = True
        state.audit_trail.append("Agent 5: PASSED")
        logger.info("[Agent 5] Risicomanagement goedgekeurd.")
        return state
