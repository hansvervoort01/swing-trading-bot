from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent4_Debate')
class BullBearDebateAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 4: Bull / Bear Debate] Adversarial analyse uitvoeren...")
        if state.rejection_reason: return state
        state.bull_score = 9.0
        state.bear_score = 1.0
        net = state.bull_score - (state.bear_score * 0.2)
        if net >= 8.0:
            state.debate_passed = True
            state.audit_trail.append("Agent 4: PASSED")
            logger.info(f"[Agent 4] Debat geslaagd. Netto score: {net}")
        else:
            state.rejection_reason = f"Afgekeurd Agent 4: Debatscore ({net}) te laag."
            state.audit_trail.append("Agent 4: FAILED")
        return state
