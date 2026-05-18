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
from agents.treatment_agent   import TreatmentPlannerAgent
from agents.liaison_agent     import ClinicianLiaisonAgent


class OrchestratorAgent:
    def __init__(self):
        self.intake     = PatientIntakeAgent()
        self.diagnostic = DiagnosticReasoningAgent()
        self.treatment  = TreatmentPlannerAgent()
        self.liaison    = ClinicianLiaisonAgent()

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


        except Exception as exc:
            result["error"] = str(exc)
            result["traceback"] = traceback.format_exc()

        result["pipeline_ms"] = round((time.time() - pipeline_start) * 1000)
        return result
