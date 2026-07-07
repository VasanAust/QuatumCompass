from typing import Literal

# ==========================================
# FROM: XPBar.tsx (Console UI Component)
# ==========================================
class TerminalXPBar:
    """
    Simulates the visual progression status bar layout, converting raw metrics
    into rank tiers, level milestones, and clean terminal loading indicators.
    """
    def __init__(self, xp: int, level: Literal['explorer', 'adventurer', 'scholar', 'researcher'], accent_color: str = "PURPLE"):
        self.xp = xp
        self.level = level
        self.accent_color = accent_color
        
        # Level label mapping configuration matrices
        self.level_labels = {
            "explorer": "Quantum Explorer",
            "adventurer": "Quantum Adventurer",
            "scholar": "Quantum Scholar",
            "researcher": "Quantum Researcher",
        }

    def render_ui(self):
        """Renders the horizontal widget containing level tiers, progress bars, and stats."""
        # Calculate localized internal rank milestones mirroring the React framework
        xp_in_current_level = self.xp % 300
        progress_percent = min(100, (xp_in_current_level / 300) * 100)
        current_rank = (self.xp // 300) + 1

        # Build terminal text-art loading bar (20 characters wide)
        bar_width = 20
        filled_chars = int((progress_percent / 100) * bar_width)
        empty_chars = bar_width - filled_chars
        progress_bar_str = f"[{'█' * filled_chars}{'░' * empty_chars}]"

        print("\n" + "═" * 60)
        print(f"🧭  STREAM: {self.level_labels[self.level].upper()} (Rank {current_rank})")
        print("─" * 60)
        
        # Display progressive metadata alignment metrics
        print(f"   Progress: {progress_bar_str}  {xp_in_current_level} / 300 XP ({int(progress_percent)}%)")
        print(f"   Total Score: {self.xp} XP ✨")
        print("═" * 60 + "\n")


# Executable runtime instance sandbox
if __name__ == "__main__":
    # Simulate a user possessing 450 total XP inside the Adventurer module tier
    xp_widget = TerminalXPBar(xp=450, level="adventurer")
    xp_widget.render_ui()