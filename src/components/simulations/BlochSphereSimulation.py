from typing import Dict, TypedDict

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class StatePoint(TypedDict):
    label: str
    x: float          # Simulated coordinate tracking
    y: float
    desc: str
    math: str


# ==========================================
# FROM: BlochSphereSimulation.tsx (Console Simulation)
# ==========================================
class TerminalBlochSphereSimulation:
    """
    Simulates the visual Bloch Sphere component, allowing state manipulation,
    coordinate logging, and localized mathematical basis vector calculations.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        self.center = {"x": 150.0, "y": 80.0}
        self.radius = 55.0

        # Predefined structural state vector projections matching the React map coordinates
        self.states: Dict[str, StatePoint] = {
            "|0⟩": {
                "label": "|0⟩",
                "x": self.center["x"],
                "y": self.center["y"] - self.radius,
                "desc": "North Pole (Ground State)",
                "math": "|ψ⟩ = 1|0⟩ + 0|1⟩",
            },
            "|1⟩": {
                "label": "|1⟩",
                "x": self.center["x"],
                "y": self.center["y"] + self.radius,
                "desc": "South Pole (Excited State)",
                "math": "|ψ⟩ = 0|0⟩ + 1|1⟩",
            },
            "|+⟩": {
                "label": "|+⟩",
                "x": self.center["x"] - self.radius * 0.7,
                "y": self.center["y"] + self.radius * 0.4,
                "desc": "Superposition (Equator, X-axis)",
                "math": "|ψ⟩ = 1/√2(|0⟩ + |1⟩)",
            },
            "|−⟩": {
                "label": "|−⟩",
                "x": self.center["x"] + self.radius * 0.7,
                "y": self.center["y"] - self.radius * 0.4,
                "desc": "Superposition (Equator, X-axis inverse)",
                "math": "|ψ⟩ = 1/√2(|0⟩ - |1⟩)",
            },
            "|i⟩": {
                "label": "|i⟩",
                "x": self.center["x"] + self.radius * 0.2,
                "y": self.center["y"] + self.radius * 0.6,
                "desc": "Superposition (Equator, Y-axis)",
                "math": "|ψ⟩ = 1/√2(|0⟩ + i|1⟩)",
            },
            "|−i⟩": {
                "label": "|−i⟩",
                "x": self.center["x"] - self.radius * 0.2,
                "y": self.center["y"] - self.radius * 0.6,
                "desc": "Superposition (Equator, Y-axis inverse)",
                "math": "|ψ⟩ = 1/√2(|0⟩ - i|1⟩)",
            },
        }
        
        # Default state choice assignment
        self.current_state_key = "|0⟩"

    def render_ui(self):
        """Renders a text representation of the 3D sphere model wireframe and active node metrics."""
        active_point = self.states[self.current_state_key]

        print("\n" + "🌀" * 20)
        print(f"🌐  BLOCH SPHERE SIMULATION  |  Active: {self.current_state_key}")
        print("🌀" * 20)
        
        # Display ascii geometric rendering grid representation
        print("         /---------\\         ")
        print("        /     |     \\        ")
        print(f"  |0⟩  [      * ]       <- Active Vector: ({active_point['x']:.1f}, {active_point['y']:.1f})")
        print("        \\     |     /        ")
        print("         \\---------/         ")
        print("             |               ")
        print("            |1⟩              ")
        print("-" * 40)
        
        # Vector description overlay labels
        print(f"📡 State Description: {active_point['desc']}")
        print(f"📐 Mathematical Form: {active_point['math']}")
        print("-" * 40)
        
        # Render interaction options matching state grid triggers
        print("Available States to Apply:")
        print("  " + "  ".join(f"[{k}]" if k == self.current_state_key else f" {k} " for k in self.states.keys()))
        print("🌀" * 20 + "\n")

    def set_current_state(self, state_key: str):
        """Updates simulation data metrics according to state button selections."""
        if state_key in self.states:
            self.current_state_key = state_key
            print(f"[Sim Interaction]: Qubit state vector set to {state_key}")
        else:
            print(f"[Sim Error]: Vector state '{state_key}' is out of bounds.")


# Executable runtime instance sandbox
if __name__ == "__main__":
    simulation = TerminalBlochSphereSimulation()
    
    # 1. Render base view
    simulation.render_ui()
    
    # 2. Simulate user hitting the superposition state buttons
    simulation.set_current_state("|+⟩")
    simulation.render_ui()
