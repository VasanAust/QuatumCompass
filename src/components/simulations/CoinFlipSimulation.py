import random
import time
from typing import List, Dict, Literal, Optional, TypedDict

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class Particle(TypedDict):
    id: int
    x: float
    y: float
    vx: float
    vy: float
    color: str


# ==========================================
# FROM: CoinFlipSimulation.tsx (Console Sim)
# ==========================================
class TerminalCoinFlipSimulation:
    """
    Simulates the animated Quantum Coin Flip simulation, processing a state
    superposition state space vector until captured/triggered by user measurement.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        self.is_spinning = True
        self.result: Optional[Literal["H", "T"]] = None
        self.particles: List[Particle] = []

    def render_ui(self):
        """Renders the physical text frame representing the spinning or collapsed state."""
        print("\n" + "🪙" * 20)
        print(f"🪙  QUANTUM COIN SIMULATION  |  Accent: {self.accent_color}")
        print("🪙" * 20)

        if self.is_spinning:
            # Active spinning superposition state vector representation
            print("         .-------.         ")
            print("        /   (ψ)   \\        ")
            print("       |   H | T   |       <- STATE: SUPERPOSITION")
            print("        \\  (1/2)  /        ")
            print("         '-------'         ")
            print("\n   [💥] The coin is spinning in mid-air!")
            print("   It is BOTH Heads and Tails at the same time.")
            print("   Choose action [1] to Catch the coin and collapse its state.")
        else:
            # Collapsed outcome state distribution vector
            print("         .-------.         ")
            print("        /         \\        ")
            print(f"       |     {self.result}     |       <- MEASURED OUTCOME")
            print("        \\         /        ")
            print("         '-------'         ")
            print(f"\n   ✨ State Collapsed! Outcome: |{self.result}⟩")
            print(f"   Simulated {len(self.particles)} burst particles exploding from contact point.")
            print("   Choose action [2] to Toss the coin back into a superposition.")
        print("🪙" * 20 + "\n")

    def handle_coin_click(self):
        """Toggles state vector collapse, firing mock particle arrays if transitioning to rest."""
        if not self.is_spinning:
            # Reset simulation environment back to default spinning state
            self.is_spinning = True
            self.result = None
            self.particles = []
            print("[Sim Interaction]: Coin tossed back into the air! Superposition re-established.")
            return

        # Stop spin cycle and pick localized state collapse choice
        outcomes: List[Literal["H", "T"]] = ["H", "T"]
        self.result = random.choice(outcomes)
        self.is_spinning = False

        # Simulate dynamic structural canvas boundary burst events
        print("\nCatching coin . . . 🫴")
        time.sleep(0.6)

        self.particles = []
        for i in range(40):
            angle = random.random() * 3.14159 * 2
            speed = 2.0 + random.random() * 5.0
            self.particles.append({
                "id": i,
                "x": 150.0,
                "y": 150.0,
                "vx": random.getrandbits(1) * speed,  # Simplified math vector maps
                "vy": random.getrandbits(1) * speed,
                "color": "gold" if random.random() > 0.5 else self.accent_color
            })


# Executable runtime instance sandbox
if __name__ == "__main__":
    simulation = TerminalCoinFlipSimulation()

    # 1. Show state frame inside superposition phase
    simulation.render_ui()

    # 2. Simulate grabbing the coin, causing state collapse and measuring a base register
    print("Action chosen: [1] Catch and measure the coin...")
    simulation.handle_coin_click()
    simulation.render_ui()

    # 3. Toss it back up
    print("Action chosen: [2] Spin coin again...")
    simulation.handle_coin_click()
    simulation.render_ui()