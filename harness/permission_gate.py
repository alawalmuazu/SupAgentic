from enum import Enum
from typing import List, Dict, Any, Optional

class PermissionMode(Enum):
    PLAN = "plan"
    DEFAULT = "default"
    ACCEPT_EDITS = "acceptEdits"
    AUTO = "auto"
    DONT_ASK = "dontAsk"
    BYPASS_PERMISSIONS = "bypassPermissions"
    BUBBLE = "bubble"

class PermissionDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"

class PermissionRule:
    def __init__(self, tool_pattern: str, decision: PermissionDecision):
        self.tool_pattern = tool_pattern
        self.decision = decision

class PermissionGate:
    """
    Implements a deny-first permission hierarchy for tool invocations.
    Deny rules always override allow rules. Unrecognized actions fall back 
    to asking the user or taking the mode-specific default behavior.
    """
    def __init__(self, mode: PermissionMode = PermissionMode.DEFAULT):
        self.mode = mode
        self.rules: List[PermissionRule] = []

    def set_mode(self, mode: PermissionMode):
        self.mode = mode

    def add_rule(self, rule: PermissionRule):
        """Add a declarative allow/deny rule."""
        self.rules.append(rule)

    def evaluate(self, tool_name: str, input_args: Dict[str, Any]) -> PermissionDecision:
        """
        Deny-first rule evaluation.
        1. Check if ANY deny rule matches. If so, return DENY immediately.
        2. Check if an allow rule matches. If so, return ALLOW.
        3. Determine fallback decision based on PermissionMode.
        """
        # Feature-gate/pre-filter simulation: matching logic
        has_allow_match = False

        for rule in self.rules:
            # Simple wildcard/exact matching for prototype
            if rule.tool_pattern == "*" or rule.tool_pattern == tool_name:
                if rule.decision == PermissionDecision.DENY:
                    return PermissionDecision.DENY
                elif rule.decision == PermissionDecision.ALLOW:
                    has_allow_match = True

        if has_allow_match:
            return PermissionDecision.ALLOW

        # Mode-based fallback (Gradual trust spectrum)
        if self.mode == PermissionMode.DONT_ASK:
            return PermissionDecision.ALLOW  # Still respects explicit Deny rules evaluated above
        elif self.mode == PermissionMode.BYPASS_PERMISSIONS:
            return PermissionDecision.ALLOW
        elif self.mode == PermissionMode.ACCEPT_EDITS and tool_name.startswith("fs_edit"):
            return PermissionDecision.ALLOW
        elif self.mode == PermissionMode.PLAN:
            return PermissionDecision.ASK
        
        return PermissionDecision.ASK

    def run_pre_tool_hook(self, tool_name: str, args: Dict[str, Any]):
        """
        Simulates PreToolUse hooks which can intercept calls and rewrite input.
        """
        return tool_name, args

