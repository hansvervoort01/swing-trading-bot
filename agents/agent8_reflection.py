from state import AgentState
from utils.logger import setup_logger
logger = setup_logger('Agent8_Reflection')
class ReflectionAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 8: Reflection & Backtest Sandbox] Quality Gate evaluatie...")
        if state.rejection_reason: return state
        state.final_score = state.bull_score
        all_passed = (
            state.data_passed and state.macro_passed and state.technical_passed and
            state.debate_passed and state.risk_passed and state.portfolio_passed and
            state.execution_passed
        )
        if state.final_score >= 8.5 and all_passed:
            state.unanimous_agreement = True
            state.approved_for_trade = True
            state.audit_trail.append("Agent 8: PASSED")
            logger.info(f"[Agent 8] QUALITY GATE GEHAALD! Eindscore: {state.final_score}/10 (Unaniem akkoord).")
        else:
            state.approved_for_trade = False
            state.rejection_reason = f"Afgekeurd Quality Gate: Score ({state.final_score}) < 8.5 of geen unaniem akkoord."
            state.audit_trail.append("Agent 8: FAILED")
            logger.warning(f"[Agent 8] {state.rejection_reason}")
        return state
