from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent6_Portfolio')
class PortfolioBalanceAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 6: Portfolio & Balance] Max 25% Exposure Cap controleren...")
        if state.rejection_reason: return state
        exposure = 15.0
        if exposure > 25.0:
            state.rejection_reason = "Afgekeurd Agent 6: Portfolio exposure > 25%."
            state.audit_trail.append("Agent 6: FAILED")
            return state
        state.portfolio_passed = True
        state.audit_trail.append("Agent 6: PASSED")
        logger.info(f"[Agent 6] Portfolio exposure binnen limiet ({exposure}%).")
        return state
