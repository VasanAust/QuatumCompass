import random
import time
import math
from typing import Literal, Dict, Any, Optional

# ==========================================
# DEPENDENCY MAP: Sub-Simulations Placeholder
# (Links with previously generated scripts.py modules)
# ==========================================
# In practice, you can import or paste the following classes above this block:
# - TerminalCoinFlipSimulation
# - TerminalDoubleSlitSimulation
# - TerminalBlochSphereSimulation
# - TerminalEntanglementStarsSimulation
# - TerminalCircuitBuilderSimulation


# ==========================================
# FROM: SimulationRenderer.tsx (Console Core Dispatcher)
# ==========================================
class TerminalSimulationRenderer:
    """
    Acts as a central routing hub and canvas wrapper. Handles the custom visual
    states for standalone inline simulations (box_peek, measurement, algorithm_viz,
    stabilizer, vqe_viz) and coordinates sub-simulation assets.
    """
    def __init__(self, sim_type: str, accent_color: str = "PURPLE"):
        self.type = sim_type
        self.accent_color = accent_color

        # Inline dynamic state engines matching React component hooks
        self.box_state: Literal["closed", "awake", "asleep"] = "closed"
        self.meas_state = {
            "alpha": 0.707,
            "beta": 0.707,
            "result": None,
            "is_measuring": False
        }
        self.grover_step = 0
        self.stabilizer_grid = [False] * 9
        self.vqe_theta = 0.5

    def peek_box(self):
        """Toggles the state vector configuration of the mystery quantum box container."""
        if self.box_state != "closed":
            self.box_state = "closed"
            print("[Sim Interaction]: Closed the mystery box lid. State reset to superposition.")
            return

        # Collapses down into discrete classical outcomes
        self.box_state = "awake" if random.random() > 0.5 else "asleep"
        print(f"[Sim Interaction]: Peeked inside! The wave function collapsed: Cat is {self.box_state.upper()}.")

    def trigger_measurement(self):
        """Simulates Born rule amplitude squared probabilistic evaluation intervals."""
        self.meas_state["is_measuring"] = True
        self.meas_state["result"] = None
        print("\nFiring projection measurement pulse . . . ⚡")
        time.sleep(0.4)

        # Probabilities calculated as squared magnitudes of orthogonal components
        p0 = self.meas_state["alpha"] ** 2
        
        self.meas_state["result"] = "0" if random.random() < p0 else "1"
        self.meas_state["is_measuring"] = False
        print(f"[Sim Interaction]: State collapsed to projection state register |{self.meas_state['result']}⟩.")

    def step_grover(self):
        """Cycles through step matrices of the Grover Amplitude Amplification phase loop."""
        self.grover_step = (self.grover_step + 1) % 4
        print(f"[Sim Interaction]: Advanced algorithm timeline index to Step {self.grover_step}")

    def toggle_stabilizer_node(self, node_idx: int):
        """Alters active parity bits layout matrix configurations."""
        if 0 <= node_idx < 9:
            self.stabilizer_grid[node_idx] = not self.stabilizer_grid[node_idx]
            print(f"[Sim Interaction]: Stabilization node coordinate [{node_idx}] flipped.")

    def set_vqe_theta(self, val: float):
        """Updates internal parameter coordinates to recalculate variational bounds."""
        self.vqe_theta = max(0.0, min(val, 1.0))
        print(f"[Sim Interaction]: Variational angle parameter shifted to {self.vqe_theta:.2f}")

    def render_ui(self):
        """Dispatches text-canvas window frames based on matching type strings."""
        print("\n" + "🔳" * 25)
        print(f"🎬  SIMULATION CANVAS ENGINE  |  Active Module: {self.type.upper()}")
        print("🔳" * 25)

        if self.type == "box_peek":
            print("   📦 QUANTUM MYSTERY BOX CONTAINER")
            print("   ----------------------------------------")
            if self.box_state == "closed":
                print("   [🔒 LID CLOSED] The wave function is mixed.")
                print("   The cat is BOTH |AWAKE⟩ and |ASLEEP⟩ simultaneously.")
            else:
                print(f"   [🔓 LID OPEN] The system has collapsed into a definite state.")
                print(f"   🐱 Outcome: Cat is found {self.box_state.upper()}!")
            print("   ----------------------------------------")
            print("   Options: [1] Toggle Box Lid / Peek Inside")

        elif self.type == "measurement":
            p0 = (self.meas_state["alpha"] ** 2) * 100
            p1 = (self.meas_state["beta"] ** 2) * 100
            print("   📏 MEASUREMENT COLLAPSE SLIDER SPREAD")
            print(f"   State vectors: {self.meas_state['alpha']:.3f}|0⟩ + {self.meas_state['beta']:.3f}|1⟩")
            print(f"   Probability:   |0⟩ ({p0:.1f}%) ░░░░░░░░░░ |1⟩ ({p1:.1f}%)")
            print(f"   Active Output: [|{self.meas_state['result']}⟩]" if self.meas_state["result"] else "   Active Output: [Wavelength Unmeasured]")
            print("   ----------------------------------------")
            print("   Options: [1] Fire Measurement Trigger")

        elif self.type == "algorithm_viz":
            steps = ["Initial Uniform State", "Oracle Phase Inversion Shift", "Inversion About the Mean Reflection", "Amplified Target Found Matrix"]
            print("   🔍 GROVER'S SEARCH AMPLITUDE AMPLIFICATION")
            print(f"   Timeline Node: Step {self.grover_step}/3 — {steps[self.grover_step]}")
            
            # Text chart graph representing probability target vector growing taller
            heights = [2, 1, 4, 8] if self.grover_step == 3 else