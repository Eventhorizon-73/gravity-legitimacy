# =============================================
# Gravity: Minimal Working Prototype (v3)
# Belnap 4-valued Legitimacy Logic
# T = APPROVE
# F, N, B = STOP + clear explanation
# =============================================

from collections import defaultdict
from datetime import datetime

# ====================== 4-VALUED LOGIC ======================
class Belnap:
    T = "T"   # True (approve)
    F = "F"   # False (deny)
    N = "N"   # Neither (unknown)
    B = "B"   # Both (conflict)

    @staticmethod
    def meet(a, b):
        """Truth-meet conjunction (conservative)"""
        if a == Belnap.T and b == Belnap.T: return Belnap.T
        if a == Belnap.F or b == Belnap.F: return Belnap.F
        if a == Belnap.N and b == Belnap.N: return Belnap.N
        return Belnap.B

# ====================== CORE GRAVITY ENGINE ======================
class Gravity:
    def __init__(self):
        self.events = []                    # immutable event stream
        self.clauses = []                   # your policy rules

    def add_event(self, type_, actor, subject, scope, payload=""):
        """Add an event to the stream"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": type_,
            "actor": actor,
            "subject": subject,
            "scope": scope,
            "payload": payload
        }
        self.events.append(event)
        return event

    def add_clause(self, name, evaluate_func):
        """Add a policy clause (your rules)"""
        self.clauses.append({"name": name, "eval": evaluate_func})

    def evaluate(self, person, capability, scope):
        """Main evaluation: returns (result, explanation)"""
        requirements = []  # in real version this would be more complex

        # Simple example logic - replace with your real clauses
        witnesses = []
        value = Belnap.N

        for clause in self.clauses:
            result = clause["eval"](person, capability, scope, self.events)
            witnesses.append(f"{clause['name']}: {result}")
            value = Belnap.meet(value, result)

        # Final rendering contract
        if value == Belnap.T:
            return "APPROVE", f"✅ All clauses satisfied ({len(witnesses)} witnesses)"
        elif value == Belnap.F:
            return "STOP", f"❌ Denied: {witnesses}"
        elif value == Belnap.B:
            return "STOP", f"⚠️ CONFLICT detected: {witnesses}"
        else:
            return "STOP", f"❓ UNKNOWN / insufficient evidence: {witnesses}"

# ====================== EXAMPLE USAGE ======================
if __name__ == "__main__":
    g = Gravity()

    # Example clauses (you can replace these with your real ones)
    def clause_training_complete(person, cap, scope, events):
        # Dummy check - in real version this would look at events
        return Belnap.T if "training" in str(events) else Belnap.N

    def clause_no_conflicts(person, cap, scope, events):
        # Dummy conflict example
        return Belnap.B if len(events) > 2 else Belnap.T

    g.add_clause("Training Complete", clause_training_complete)
    g.add_clause("No Active Conflicts", clause_no_conflicts)

    # Add some test events
    g.add_event("access_request", "lisa", "ethan", "sensitive_data")
    g.add_event("training_completed", "system", "ethan", "compliance")

    # Run evaluation
    result, explanation = g.evaluate("ethan", "sensitive_data", "compliance")
    print(f"Result: {result}")
    print(f"Explanation: {explanation}")
