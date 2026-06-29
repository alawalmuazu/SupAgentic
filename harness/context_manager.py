from typing import List, Dict, Any, Tuple
import copy

class ContextManager:
    """
    Implements a progressive 5-layer context compaction pipeline:
    1. Budget reduction (Truncate single large outputs)
    2. Snip (Remove old history)
    3. Microcompact (Cache-aware compression based on IDs)
    4. Context Collapse (Read-time projection of summaries)
    5. Auto-compact (LLM full summary)
    """

    def __init__(self, max_context_budget: int = 100000):
        self.max_context_budget = max_context_budget
        self.messages: List[Dict[str, Any]] = []

    def load_user_context(self) -> List[Dict[str, Any]]:
        """Simulates lazy-loading 4-level hierarchy of CLAUDE.md files."""
        return [{"role": "user", "content": "Loaded CLAUDE.md guidelines"}]

    def append_message(self, message: Dict[str, Any]):
        self.messages.append(message)

    def size_of(self, messages: List[Dict[str, Any]]) -> int:
        return sum(len(str(m.get("content", ""))) for m in messages)

    def compact_pipeline(self) -> List[Dict[str, Any]]:
        """
        Runs the 5 sequential context shapers before a model call.
        Applies lighter reductions first before escalating to heavier ones.
        """
        messages_shaping = copy.deepcopy(self.messages)

        # 1. Budget Reduction (Cap tool result sizes)
        for msg in messages_shaping:
            if msg.get("type") == "tool_result" and len(str(msg.get("content", ""))) > 8000:
                msg["content"] = "[Content truncated due to budget constraints. Reference saved.]"

        current_size = self.size_of(messages_shaping)
        if current_size < self.max_context_budget: return messages_shaping
        
        # 2. Snip (Trim older history segments)
        if len(messages_shaping) > 10:
            # Retain first system prompts and last 10 turns
            messages_shaping = messages_shaping[:2] + messages_shaping[-10:]
            
        current_size = self.size_of(messages_shaping)
        if current_size < self.max_context_budget: return messages_shaping

        # 3. Microcompact (Fine-grained item deletion)
        # Placeholder for targeted removal of specific intermediate tool searches

        # 4. Context Collapse (Read-time projection)
        # Summarize mid-history blocks into single summary points invisibly

        # 5. Auto Compact (Full LLM Summary, last resort)
        if current_size > self.max_context_budget:
            summary = self._call_model_summarize(messages_shaping)
            messages_shaping = messages_shaping[:2] + [{"role": "system", "content": f"History Summary: {summary}"}] + messages_shaping[-2:]

        return messages_shaping

    def _call_model_summarize(self, msgs: List[Dict[str, Any]]) -> str:
        """Simulate LLM summarization call."""
        return "Summarized conversation containing multiple iterative execution steps."
