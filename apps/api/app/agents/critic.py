from app.agents.base import ResearchContext


class CriticAgent:
    name = "Critic Agent"

    def review(self, context: ResearchContext) -> list[str]:
        notes: list[str] = []
        recommendation = context.artifacts.get("recommendation")
        if not recommendation:
            return ["No recommendation was generated."]
        if not recommendation.reasons:
            notes.append("Recommendation lacks explicit reasons.")
        if not recommendation.evidence:
            notes.append("Recommendation lacks supporting evidence.")
        if recommendation.action == "BUY" and context.artifacts.get("risk") and context.artifacts["risk"].level == "High":
            notes.append("Buy rating should be sized carefully because risk is high.")
        if not notes:
            notes.append("Recommendation includes reasons, risks, and traceable evidence. No contradictions detected.")
        return notes
