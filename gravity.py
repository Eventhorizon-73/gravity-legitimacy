# =============================================
# Gravity - Edge Case Ready Version
# Add your real edge cases in the section below
# =============================================

from datetime import datetime

class Belnap:
    T = "T"   # APPROVE
    F = "F"   # STOP - Denied
    N = "N"   # STOP - Unknown
    B = "B"   # STOP - Conflict

    @staticmethod
    def meet(a, b):
        if a == Belnap.T and b == Belnap.T: return Belnap.T
        if a == Belnap.F or b == Belnap.F: return Belnap.F
        if a == Belnap.N and b == Belnap.N: return Belnap.N
        return Belnap.B

class Gravity:
    def __init__(self):
        self.events = []

    def add_event(self, type_, actor, subject, scope, payload=""):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "type": type_,
            "actor": actor,
            "subject": subject,
            "scope": scope,
            "payload": payload
        })

    def evaluate(self, person, capability, scope):
        witnesses = []
        value = Belnap.N

        # ================== YOUR EDGE CASES GO HERE ==================
        # Add your real rules below (I'll help you write them)

        def clause_training_complete(events):
            training_done = any(e["type"] == "training_completed" for e in events)
            return Belnap.T if training_done else Belnap.N

        def clause_no_conflicts(events):
            # Example: conflict if more than 3 events (you can change this)
            return Belnap.B if len(events) > 3 else Belnap.T

        # Add more clauses here ↓↓↓ (your real edge cases)
        # Example: clause_sleep_cycle_ok, clause_no_active_investigation, etc.

        # =============================================================

        clauses = [
            ("Training Complete", clause_training_complete),
            ("No Active Conflicts", clause_no_conflicts),
            # Add your new clauses here
        ]

        for name, func in clauses:
            result = func(self.events)
            witnesses.append(f"{name}: {result}")
            value = Belnap.meet(value, result)

        # Final rendering contract
        if value == Belnap.T:
            return "APPROVE", f"✅ All clauses satisfied"
        elif value == Belnap.F:
            return "STOP", f"❌ DENIED: {witnesses}"
        elif value == Belnap.B:
            return "STOP", f"⚠️ CONFLICT: {witnesses}"
        else:
            return "STOP", f"❓ UNKNOWN: {witnesses}"

# ====================== TEST ======================
if __name__ == "__main__":
    g = Gravity()

    # Add your test events here
    g.add_event("access_request", "lisa", "ethan", "sensitive_data")
    g.add_event("training_completed", "system", "ethan", "compliance")

    result, explanation = g.evaluate("ethan", "sensitive_data", "compliance")
    print("RESULT:", result)
    print("EXPLANATION:", explanation)
