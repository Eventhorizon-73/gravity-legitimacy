# =============================================
# Gravity - O.J. Simpson Edge Case Ready
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

        # O.J. Simpson 1995 clauses (R1-R5)
        def r1_evidence_beyond_reasonable_doubt(events):
            dna = any("dna" in e["payload"].lower() for e in events)
            glove = any("glove" in e["payload"].lower() for e in events)
            if dna and glove: return Belnap.B
            if dna: return Belnap.T
            return Belnap.N

        def r2_prosecution_burden(events):
            return Belnap.T if any("prosecution" in e["type"] for e in events) else Belnap.N

        def r3_acquit_on_doubt(events):
            return Belnap.B if any("doubt" in e["payload"].lower() for e in events) else Belnap.T

        def r4_procedural_fairness(events):
            return Belnap.B if any("media" in e["payload"].lower() for e in events) else Belnap.T

        def r5_criminal_standard_not_public_suspicion(events):
            return Belnap.B if any("public" in e["payload"].lower() for e in events) else Belnap.T

        clauses = [
            ("R1. Evidence Beyond Reasonable Doubt", r1_evidence_beyond_reasonable_doubt),
            ("R2. Prosecution Bears Burden", r2_prosecution_burden),
            ("R3. Acquit on Material Doubt", r3_acquit_on_doubt),
            ("R4. Procedural Fairness", r4_procedural_fairness),
            ("R5. Criminal Standard, Not Public Suspicion", r5_criminal_standard_not_public_suspicion),
        ]

        for name, func in clauses:
            result = func(self.events)
            witnesses.append(f"{name}: {result}")
            value = Belnap.meet(value, result)

        if value == Belnap.T:
            return "APPROVE", f"✅ Legitimate conviction"
        elif value == Belnap.F:
            return "STOP", f"❌ Conviction illegitimate: {witnesses}"
        elif value == Belnap.B:
            return "STOP", f"⚠️ CONFLICT (legitimacy unclear): {witnesses}"
        else:
            return "STOP", f"❓ UNKNOWN / insufficient evidence: {witnesses}"

# ====================== TEST ======================
if __name__ == "__main__":
    g = Gravity()

    g.add_event("dna_evidence", "prosecution", "o.j.simpson", "murder_trial", "DNA match on blood")
    g.add_event("glove_demonstration", "defense", "o.j.simpson", "murder_trial", "Glove did not fit")
    g.add_event("jury_instruction", "judge", "o.j.simpson", "murder_trial", "Beyond reasonable doubt")
    g.add_event("media_pressure", "public", "o.j.simpson", "murder_trial", "Massive public suspicion")
    g.add_event("reasonable_doubt", "defense", "o.j.simpson", "murder_trial", "Timeline and witness conflicts")

    result, explanation = g.evaluate("o.j.simpson", "criminal_conviction", "murder_trial")
    print("\n" + "="*60)
    print("O.J. SIMPSON 1995 MURDER CONVICTION EVALUATION")
    print("="*60)
    print("RESULT:", result)
    print("EXPLANATION:", explanation)
