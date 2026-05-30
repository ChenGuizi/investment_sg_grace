from app.schemas.market import DeepResearchReport


class KnowledgeGraphBuilder:
    def from_report(self, report: DeepResearchReport) -> dict:
        nodes = [
            {"id": report.ticker, "type": "company"},
            {"id": "AI demand", "type": "event"},
            {"id": "Interest rates", "type": "macro"},
        ]
        links = [
            {"source": "AI demand", "target": report.ticker, "relationship": "supports earnings expectations"},
            {"source": "Interest rates", "target": report.ticker, "relationship": "affects valuation multiple"},
        ]
        for finding in report.agent_findings:
            node_id = finding.agent.replace(" Agent", "")
            nodes.append({"id": node_id, "type": "agent_finding", "score": finding.score.value})
            links.append({"source": node_id, "target": report.ticker, "relationship": "informs recommendation"})
        return {"nodes": nodes, "links": links}
