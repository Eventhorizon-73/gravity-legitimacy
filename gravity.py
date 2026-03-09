# =============================================
# Gravity - Ultra Simple Working Version
# Just run this and you'll see it working
# =============================================

from datetime import datetime

class Belnap:
    T = "T"   # Approve
    F = "F"   # Denied
    N = "N"   # Unknown
    B = "B"   # Conflict

    @staticmethod
    def meet(a, b):
        if a == Belnap.T and b == Belnap.T: return Belnap.T
        if a == Belnap.F or b == Belnap.F: return Belnap.F
        if a == Belnap.N and b == Belnap.N: return Belnap.N
        return Belnap.B

class Gravity:
    def __init__(self):
        self.events = []

    def add_event(self, type_, actor, subject, scope):
        self.events.append({"type": type_, "actor": actor, "subject": subject, "scope": scope})
        print(f"✅ Event added: {type_} for {subject}")

    def evaluate(self, person, capability, scope):
        print(f"\n🔍 Evaluating: {person} requesting {capability} in {scope}")
        print(f"Events so far: {len(self.events)}")

        # Simple example clauses (you can change these later)
        training_done = any(e["type"] == "training_completed" for e in self.events)
        has_conflict = len(self.events) > 3

        value = Belnap.T
        if not training_done:
            value = Belnap.meet(value, Belnap.N)
        if has_conflict:
            value = Belnap.meet(value, Belnap.B)

        if value == Belnap.T:
            return "APPROVE", "✅ All good - everything checks out"
        elif value == Belnap.B:
            return "STOP", f"⚠️ CONFLICT detected ({len(self.events)} events)"
        else:
            return "STOP", f"❓ UNKNOWN - missing requirements (training: {training_done})"

# ====================== TEST IT ======================
if __name__ == "__main__":
    g = Gravity()

    g.add_event("access_request", "lisa", "ethan", "sensitive_data")
    g.add_event("training_completed", "system", "ethan", "compliance")

    result, explanation = g.evaluate("ethan", "sensitive_data", "compliance")
    print("\n" + "="*50)
    print("FINAL RESULT:", result)
    print("EXPLANATION:", explanation)
