import math
from typing import Dict, Any

# ==========================================
# FROM: WaveSliderSimulation.tsx (Console Sim)
# ==========================================
class TerminalWaveSliderSimulation:
    """
    Simulates the structural physics engine behind wave superposition,
    calculating phase offsets from 0 to 2π and rendering resultant wave dynamics.
    """
    def __init__(self, accent_color: str = "PURPLE"):
        self.accent_color = accent_color
        self.phase_offset = 0.0  # Ranges from 0 to 2*pi

    def get_interference_status(self) -> Dict[str, str]:
        """Evaluates phase alignment vectors to classify active constructive/destructive boundaries."""
        # Normalize offset into fractions of pi
        pi_mod = self.phase_offset % (2 * math.pi)
        
        # Check boundary rules matching React interface limits
        if pi_mod < 0.15 or pi_mod > (2 * math.pi - 0.15):
            return {
                "label": "CONSTRUCTIVE INTERFERENCE",
                "desc": "Ripples line up perfectly! Peaks double in height, making a louder/brighter wave.",
                "color": "GREEN"
            }
        elif math.pi - 0.25 <= pi_mod <= math.pi + 0.25:
            return {
                "label": "DESTRUCTIVE INTERFERENCE",
                "desc": "Peaks meet troughs! The waves completely cancel each other out into perfect stillness.",
                "color": "RED"
            }
        else:
            return {
                "label": "PARTIAL INTERFERENCE",
                "desc": "Waves are out of alignment, creating mixed combinations of shifting amplitudes.",
                "color": "YELLOW"
            }

    def set_phase_offset(self, val: float):
        """Updates phase angle and clips inside the 0 to 2π execution loop boundaries."""
        self.phase_offset = max(0.0, min(val, 2 * math.pi))
        print(f"[Sim Interaction]: Phase Offset shifted to {self.phase_offset:.2f} rad ({(self.phase_offset / math.pi):.2f}π)")

    def render_ui(self):
        """Renders text graphs plotting the output interference results."""
        interference = self.get_interference_status()

        print("\n" + "🌊" * 20)
        print(f"🌊  WAVE SUPERPOSITION SLIDER  |  Phase: {(self.phase_offset / math.pi):.2f}π")
        print("🌊" * 20)

        # Draw a horizontal ASCII representation of the Combined Output wave (Width 30)
        width = 30
        amplitude_scale = 1.0 + math.cos(self.phase_offset) # Max 2, Min 0
        
        print("   --- Combined Superposition Output Graph ---")
        for row in range(5, -6, -2): # Scan vertically down line tracks
            row_chars = []
            for col in range(width):
                # Sample wave equations across column timeline domains
                radian = (col / width) * math.pi * 4
                # Wave 1 + Wave 2 with phase offset offset adjustments
                y_val = math.sin(radian) + math.sin(radian + self.phase_offset)
                
                if abs(y_val * 2 - row) < 1.0:
                    row_chars.append("█")
                else:
                    row_chars.append(" ")
            print(f"   {row:2d} │ " + "".join(row_chars))
        print("      " + "─" * width)
        
        print(f"\n   ✨ Condition : [{interference['label']}] ({interference['color']})")
        print(f"   📢 Details   : {interference['desc']}")
        print("-" * 50)
        print("   Options: [1] Set Phase to 0 (Constructive) | [2] Set Phase to π (Destructive)")
        print("🌊"