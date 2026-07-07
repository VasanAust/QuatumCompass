import time
from typing import Dict, TypedDict

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class StarCoordinates(TypedDict):
    x: float
    y: float


# ==========================================
# FROM: EntanglementStarsSimulation.tsx
# ==========================================
class TerminalEntanglementStarsSimulation:
    """
    Simulates the Entanglement Stars layout engine, calculating immediate 
    mirrored twin state vectors across spatial boundaries when a user drags Star A.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        
        # Initial positions matching the React container defaults
        self.star_a: StarCoordinates = {"x": 60.0, "y": 70.0}   # Purple Draggable Star (Left Half)
        self.star_b: StarCoordinates = {"x": 220.0, "y": 70.0}  # Teal Entangled Mirror Star (Right Half)
        self.is_dragging = False
        self.is_teal_pulsing = False

    def move_star_a(self, new_x: float, new_y: float):
        """
        Updates Star A's coordinates within valid boundaries and immediately 
        calculates the entangled state vector transformation for Star B.
        """
        # Clamp Left Half Bound constraints: X ranges [15, 130], Y ranges [15, 125]
        clamped_x = max(15.0, min(new_x, 130.0))
        clamped_y = max(15.0, min(new_y, 125.0))

        self.star_a = {"x": clamped_x, "y": clamped_y}
        self.is_dragging = True

        # Quantum Entanglement state calculation:
        # Mirror Star A coordinates over the center line partition (X = 140)
        mirrored_x = 280.0 - clamped_x
        mirrored_y = clamped_y  # Vertically identical mapping

        # Replicate the 50ms propagation delay and glow response trigger
        print(f"\n[Moving Star A] -> Position: ({clamped_x:.1f}, {clamped_y:.1f})")
        print("⚡ Collating entangled state over space thread partition...")
        time.sleep(0.05)  # 50ms simulation delay

        self.star_b = {"x": mirrored_x, "y": mirrored_y}
        self.is_teal_pulsing = True
        self.is_dragging = False

    def render_ui(self):
        """Generates a text-art representation of the connected non-separable state particles."""
        print("\n" + "⭐" * 20)
        print(f"✨  ENTANGLEMENT STARS SIMULATION  |  Thread: ACTIVE")
        print("⭐" * 20)

        # Print layout coordinates tracking positional synchronicity
        print(f"   🟣 Star A (You)     : Axis X={self.star_a['x']:<5.1f}  Axis Y={self.star_a['y']:.1f}")
        print(f"   🟢 Star B (Twin)    : Axis X={self.star_b['x']:<5.1f}  Axis Y={self.star_b['y']:.1f}")
        
        if self.is_teal_pulsing:
            print("   ✨ Status           : [🟢 Star B Pulsed with Energy Glow!]")
            self.is_teal_pulsing = False  # Clear ephemeral flag on frame paint
        else:
            print("   ✨ Status           : Synchronized")

        print("\n   [Canvas Space Grid Map]")
        print("   ├─ [🟣 A] " + "." * 15 + " (Quantum Thread Connection) " + "." * 15 + " [🟢 B] ─┤")
        print("-" * 55)
        print("   Options: [1] Shift Star A Left  |  [2] Shift Star A Right")
        print("⭐" * 20 + "\n")


# Executable runtime instance sandbox
if __name__ == "__main__":
    simulation = TerminalEntanglementStarsSimulation()

    # 1. Render initial rest state layout
    simulation.render_ui()

    # 2. Simulate dragging Star A deeper into the left boundary quadrant
    print("Action chosen: [1] Shift Star A Left (X=30, Y=85)...")
    simulation.move_star_a(30.0, 85.0)
    simulation.render_ui()