# =============================================
# Gravity: Improved Working Prototype (v3)
# Belnap 4-valued Legitimacy Logic
# T = APPROVE
# F, N, B = STOP + clear explanation
# =============================================

from datetime import datetime

class Belnap:
    T = "T"   # Approve
    F = "F"   # Stop - Denied
    N = "N"   # Stop - Unknown
    B = "B"   # Stop - Conflict

    @staticmethod
    def meet(a, b):
        if a == Belnap.T and b == Belnap.T: return Belnap.T
        if a == Belnap.F or b == Belnap.F: return Belnap.F
        if a == Belnap.N and b == Belnap.N: return Belnap.N
        return Belnap.B

class Gravity:
    def __init__(self):
        self.events = []
        self.clauses = []

    def add_event(self, type_, actor, subject, scope, payload=""):
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
        self.clauses.append({"name": name, "eval": evaluate_func})

    def evaluate(self, person, capability, scope):
        witnesses = []
        value = Belnap.N

        for clause in self.clauses:
            result = clause["eval"](person, capability, scope, self.events)
            witnesses.append(f"{clause['name']}: {result}")
            value = Belnap.meet(value, result)

        # Rendering contract
        if value == Belnap.T:
            return "APPROVE", f"✅ Approved — all clauses satisfied"
        elif value == Belnap.F:
            return "STOP", f"❌ DENIED: {witnesses}"
        elif value == Belnap.B:
            return "STOP", f"⚠️ CONFLICT: {witnesses}"
        else:
            return "STOP", f"❓ UNKNOWN / insufficient evidence: {witnesses}"

# ====================== EXAMPLE USAGE (your test) ======================
if __name__ == "__main__":
    g = Gravity()

    # === Your real clauses go here ===
    def clause_training_complete(person, cap, scope, events):
        # Looks for any training event
        return Belnap.T if any(e["type"] == "training_completed" for e in events) else Belnap.N

    def clause_no_conflicts(person, cap, scope, events):
        # Dummy conflict example (you can change this)
        return Belnap.B if len(events) > 3 else Belnap.T

    g.add_clause("Training Complete", clause_training_complete)
    g.add_clause("No Active Conflicts", clause_no_conflicts)

    # Add your test events
    g.add_event("access_request", "lisa", "ethan", "sensitive_data")
    g.add_event("training_completed", "system", "ethan", "compliance")

    # Run it
    result, explanation = g.evaluate("ethan", "sensitive_data", "compliance")
    print("RESULT:", result)
    print("EXPLANATION:", explanation)
    Improve prototype with better example clauses

