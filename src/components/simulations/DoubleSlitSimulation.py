import random
import time
from typing import List, TypedDict

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
class MovingParticle(TypedDict):
    id: int
    x: float
    y: float
    target_y: float
    progress: float

class ScreenDot(TypedDict):
    id: int
    x: float
    y: float


# ==========================================
# FROM: DoubleSlitSimulation.tsx (Console Sim)
# ==========================================
class TerminalDoubleSlitSimulation:
    """
    Simulates the structural physics engine behind the Double-Slit Experiment,
    toggling between multi-band wave patterns and collapsed double-band particle distributions.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        self.is_observed = False
        self.flying_particles: List[MovingParticle] = []
        self.screen_dots: List[ScreenDot] = []
        self.counter = 0

    def get_random_target_y(self, observed: bool) -> float:
        """Computes statistical target distribution values depending on active observation."""
        if observed:
            # Particle distribution: Collapses into two distinct classical slits bands
            return 50.0 + (random.random() - 0.5) * 15.0 if random.random() > 0.5 else 100.0 + (random.random() - 0.5) * 15.0
        else:
            # Wave distribution: Intertwines into multi-band diffraction peaks (25, 50, 75, 100, 125)
            r = random.random()
            if r < 0.1:   peaks = 25.0
            elif r < 0.35: peaks = 50.0
            elif r < 0.65: peaks = 75.0
            elif r < 0.9:  peaks = 100.0
            else:          peaks = 125.0
            return peaks + (random.random() - 0.5) * 8.0

    def handle_toggle_detector(self):
        """Switches observation toggle flags, purging previous trace logs."""
        self.is_observed = not self.is_observed
        self.flying_particles.clear()
        self.screen_dots.clear()
        print(f"[Sim Interaction]: Quantum Detector turned {'ON 👁️ (Particle Collapse)' if self.is_observed else 'OFF 🚫 (Wave Superposition)'}")

    def fire_particle_stream(self):
        """Simulates sequential coordinate delta updates across a complete lifecycle loop."""
        print("\nFiring beam of quantum matter grains . . . 🌌