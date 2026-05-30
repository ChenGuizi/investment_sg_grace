from app.core.config import Settings


class AIProvider:
    async def summarize(self, prompt: str, context: dict | None = None) -> str:
        raise NotImplementedError


class DemoAIProvider(AIProvider):
    async def summarize(self, prompt: str, context: dict | None = None) -> str:
        ticker = (context or {}).get("ticker", "the stock")
        return f"{ticker} analysis combines market context, news, fundamentals, technicals, and risk-adjusted evidence."


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def summarize(self, prompt: str, context: dict | None = None) -> str:
        # Wire to the OpenAI Responses API in production.
        return await DemoAIProvider().summarize(prompt, context)


class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def summarize(self, prompt: str, context: dict | None = None) -> str:
        # Wire to Anthropic Claude Messages API in production.
        return await DemoAIProvider().summarize(prompt, context)


def get_ai_provider(settings: Settings) -> AIProvider:
    if settings.openai_api_key:
        return OpenAIProvider(settings.openai_api_key)
    if settings.anthropic_api_key:
        return ClaudeProvider(settings.anthropic_api_key)
    return DemoAIProvider()
