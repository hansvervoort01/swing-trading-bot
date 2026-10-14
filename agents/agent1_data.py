from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent1_Data')
class DataIngestionAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 1: Data & Ingestie] Validatie volume, Code P en Earnings Blackout...")
        s = state.trade_signal
        if s.daily_volume_usd < 10000000:
            state.rejection_reason = "Afgekeurd Agent 1: Volume onder $10M."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        if s.days_to_earnings <= 21:
            state.rejection_reason = f"Afgekeurd Agent 1: Earnings binnen 3 weken ({s.days_to_earnings} dagen)."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        if s.transaction_code != 'P':
            state.rejection_reason = "Afgekeurd Agent 1: Geen Code P."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        state.data_passed = True
        state.audit_trail.append("Agent 1: PASSED")
        logger.info("[Agent 1] Data validatie geslaagd.")
        return state
