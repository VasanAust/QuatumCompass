import math
from typing import List, Literal, Dict, TypedDict

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
GateType = Literal["H", "X", "CNOT", None]

class Probabilities(TypedDict):
    b00: int  # representing |00>
    b01: int  # representing |01>
    b10: int  # representing |10>
    b11: int  # representing |11>


# ==========================================
# FROM: CircuitBuilderSimulation.tsx
# ==========================================
class TerminalCircuitBuilderSimulation:
    """
    Simulates a 2-qubit quantum circuit wire canvas, processing real-time 
    state-vector mathematical matrix operations for visual text histograms.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        
        # 4 slots on each of the 2 wires[cite: 11]
        self.wire0: List[GateType] = [None, None, None, None]  # wire 0: q0[cite: 11]
        self.wire1: List[GateType] = [None, None, None, None]  # wire 1: q1[cite: 11]
        self.selected_gate: GateType = "H"                     # Default chosen item palette[cite: 11]
        self.probabilities: Dict[str, int] = {                 # Computational basis probabilities[cite: 11]
            "00": 100,
            "01": 0,
            "10": 0,
            "11": 0
        }
        self.has_run = False[cite: 11]

    def select_gate(self, gate: GateType):
        """Sets active gate inside the palette toolbelt array selector."""
        if gate in ["H", "X", "CNOT", None]:
            self.selected_gate = gate
            print(f"[Palette Selection]: Active gate tool set to -> {gate}")

    def handle_slot_click(self, wire_idx: int, slot_idx: int):
        """Toggles selected gate injection inside designated coordinate space index maps."""
        if slot_idx < 0 or slot_idx >= 4:
            return

        self.has_run = False[cite: 11]
        target_wire = self.wire0 if wire_idx == 0 else self.wire1[cite: 11]
        
        # If already has that gate, toggle it to null. Otherwise set to selectedGate.[cite: 11]
        if target_wire[slot_idx] == self.selected_gate:
            target_wire[slot_idx] = None
        else:
            target_wire[slot_idx] = self.selected_gate

    def clear_circuit(self):
        """Resets structural storage frames and resets basis registration arrays."""
        self.wire0 = [None, None, None, None][cite: 11]
        self.wire1 = [None, None, None, None][cite: 11]
        self.probabilities = {"00": 100, "01": 0, "10": 0, "11": 0}[cite: 11]
        self.has_run = False[cite: 11]
        print("[System Interaction]: Circuit canvas cleared and reset.")

    def run_circuit_sim(self):
        """
        Executes structural mathematical simulation step calculations across execution lines.
        Computes state-vector changes and probability distributions[cite: 11].
        """
        # 2-qubit state vector: [c00, c01, c10, c11] representing states |00>, |01>, |10>, |11>[cite: 11]
        # Qubit 1 is MSB, Qubit 0 is LSB. E.g. |q1 q0>[cite: 11]
        state = [1.0, 0.0, 0.0, 0.0][cite: 11]

        for col in range(4):[cite: 11]
            g0 = self.wire0[col][cite: 11]
            g1 = self.wire1[col][cite: 11]

            # 1. Process wire 0 gate (H or X)[cite: 11]
            if g0 == "H":[cite: 11]
                next_state = [0.0, 0.0, 0.0, 0.0]
                inv_sqrt2 = 1.0 / math.sqrt(2)[cite: 11]
                # Hadamard on q0 mapping:[cite: 11]
                # |00> -> (|00> + |01>)/sqrt(2), |01> -> (|00> - |01>)/sqrt(2)[cite: 11]
                # |10> -> (|10> + |11>)/sqrt(2), |11> -> (|10> - |11>)/sqrt(2)[cite: 11]
                next_state[0] = (state[0] + state[1]) * inv_sqrt2[cite: 11]
                next_state[1] = (state[0] - state[1]) * inv_sqrt2[cite: 11]
                next_state[2] = (state[2] + state[3]) * inv_sqrt2[cite: 11]
                next_state[3] = (state[2] - state[3]) * inv_sqrt2[cite: 11]
                state = next_state[cite: 11]
            elif g0 == "X":[cite: 11]
                # Swap |00> <-> |01> and |10> <-> |11>[cite: 11]
                state = [state[1], state[0], state[3], state[2]][cite: 11]

            # 2. Process wire 1 gate (H or X)[cite: 11]
            if g1 == "H":[cite: 11]
                next_state = [0.0, 0.0, 0.0, 0.0]
                inv_sqrt2 = 1.0 / math.sqrt(2)[cite: 11]
                # Hadamard on q1 mapping:[cite: 11]
                # |00> -> (|00> + |10>)/sqrt(2), |10> -> (|00> - |10>)/sqrt(2)[cite: 11]
                # |01> -> (|01> + |11>)/sqrt(2), |11> -> (|01> - |11>)/sqrt(2)[cite: 11]
                next_state[0] = (state[0] + state[2]) * inv_sqrt2[cite: 11]
                next_state[2] = (state[0] - state[2]) * inv_sqrt2[cite: 11]
                next_state[1] = (state[1] + state[3]) * inv_sqrt2[cite: 11]
                next_state[3] = (state[1] - state[3]) * inv_sqrt2[cite: 11]
                state = next_state[cite: 11]
            elif g1 == "X":[cite: 11]
                # Swap |00> <-> |10> and |01> <-> |11>[cite: 11]
                state = [state[2], state[3], state[0], state[1]][cite: 11]

            # 3. Process CNOT gate (if CNOT is on either wire, let's treat wire 0 as control if placed on wire 0, etc.)[cite: 11]
            # Case A: CNOT is on wire 0 at this column. Let's make q0 control and q1 target.[cite: 11]
            if g0 == "CNOT" and g1 != "CNOT":[cite: 11]
                state = [state[0], state[3], state[2], state[1]][cite: 11]
            # Case B: CNOT is on wire 1. Let's make q1 control and q0 target.[cite: 11]
            elif g1 == "CNOT" and g0 != "CNOT":[cite: 11]
                state = [state[0], state[1], state[3], state[2]][cite: 11]
            # Case C: CNOT is placed on BOTH wires. That creates a coupled CNOT (Bell State creator if combined with H on wire 0)[cite: 11]
            elif g0 == "CNOT" and g1 == "CNOT":[cite: 11]
                state = [state[0], state[3], state[2], state[1]][cite: 11]

        # Calculate probabilities as squared amplitudes (multiplied by 100 for percentage)[cite: 11]
        p00 = round(state[0] * state[0] * 100)[cite: 11]
        p01 = round(state[1] * state[1] * 100)[cite: 11]
        p10 = round(state[2] * state[2] * 100)[cite: 11]
        p11 = round(state[3] * state[3] * 100)[cite: 11]

        self.probabilities = {[cite: 11]
            "00": max(0, p00),[cite: 11]
            "01": max(0, p01),[cite: 11]
            "10": max(0, p10),[cite: 11]
            "11": max(0, p11),[cite: 11]
        }[cite: 11]
        self.has_run = True[cite: 11]

    def render_ui(self):
        """Displays textual canvas wires schematic along with localized histograms."""
        print("\n" + "⚡" * 25)
        print(f"🎛️  QUANTUM CIRCUIT BUILDER  |  Tool: {self.selected_gate}")
        print("⚡" * 25)

        # Render helper method for horizontal circuit layouts
        def format_wire(label: str, slots: List[GateType]) -> str:
            line_str = f"{label} ───"
            slot_strings = [f"[{g if g else ' '}]" for g in slots]
            return line_str + "───────".join(slot_strings) + "───"

        print(format_wire("q0", self.wire0))[cite: 11]
        print("         │         │         │         │")
        print(format_wire("q1", self.wire1))[cite: 11]
        print("-" * 50)

        # Output dynamic text block histogram components matching execution state maps
        print("📊 Probability Histograms:")
        for state_key, prob in self.probabilities.items():
            bar_width = 10
            filled = int((prob / 100) * bar_width)
            bar_str = "█" * filled + "░" * (bar_width - filled)
            print(f"   |{state_key}⟩ : {bar_str} {prob}%")
        print("⚡" * 25 + "\n")


# Executable runtime instance sandbox
if __name__ == "__main__":
    circuit_sim = TerminalCircuitBuilderSimulation()

    # Place an 'H' gate on slot 0 of wire q0 to prepare an initial state superposition vector
    circuit_sim.select_gate("H")
    circuit_sim.handle_slot_click(wire_idx=0, slot_idx=0)

    # Place a 'CNOT' gate on slot 1 of wire q0 to generate a maximal Bell state entanglement distribution
    circuit_sim.select_gate("CNOT")
    circuit_sim.handle_slot_click(wire_idx=0, slot_idx=1)

    # Compute calculations and refresh output display
    print("Simulating computation engine call...")
    circuit_sim.run_circuit_sim()
    circuit_sim.render_ui()