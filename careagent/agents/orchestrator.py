"""
Orchestrator Agent
------------------
Central coordinator for CareAgent.  Receives a patient record,
dispatches to each sub-agent in sequence, aggregates results,
and returns a unified clinical decision-support response.
"""

import time
import traceback
from typing import Optional

from agents.intake_agent      import PatientIntakeAgent
from agents.diagnostic_agent  import DiagnosticReasoningAgent



class OrchestratorAgent:
    def __init__(self):
        self.intake     = PatientIntakeAgent()
        self.diagnostic = DiagnosticReasoningAgent()


    def run(self, raw_patient: dict, use_llm: bool = True) -> dict:
        """
        Full pipeline:
          1. Intake    → structured patient summary + flags
          2. Diagnostic→ differential diagnoses + SHAP scores
          3. Treatment → evidence-based care pathway
          4. Liaison   → plain-language report for clinician
        """
        pipeline_start = time.time()
        result = {
            "patient_id": raw_patient.get("patient_id", "UNKNOWN"),
            "pipeline_ms": 0,
            "error": None,
            "intake":    {},
            "diagnostic":{},
            "treatment": {},
            "liaison":   {},
        }

        try:
            # ── Step 1: Patient Intake ─────────────────────────────────
            t0 = time.time()
            intake_out = self.intake.process(raw_patient)
            intake_out["agent_ms"] = round((time.time() - t0) * 1000)
            result["intake"] = intake_out

            # ── Step 2: Diagnostic Reasoning ──────────────────────────
            t0 = time.time()
            diag_out = self.diagnostic.reason(intake_out)
            diag_out["agent_ms"] = round((time.time() - t0) * 1000)
            result["diagnostic"] = diag_out

        
        except Exception as exc:
            result["error"] = str(exc)
            result["traceback"] = traceback.format_exc()

        result["pipeline_ms"] = round((time.time() - pipeline_start) * 1000)
        return result
