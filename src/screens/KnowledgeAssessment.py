import time
from typing import Dict, Literal, Callable, Any

# ==========================================
# FROM: KnowledgeAssessment.tsx (Console Engine)
# ==========================================
class TerminalKnowledgeAssessment:
    """
    Onboarding questionnaire module. Guides learners through introductory 
    diagnostic steps and scores responses to configure the core tutor stream.
    """
    def __init__(self, on_level_determined: Callable[[str], None]):
        self.on_level_determined = on_level_determined
        
        # Internal workflow parameters matching the React layout state hooks
        self.step = 1
        self.answers: Dict[str, str] = {
            "q1": "",
            "q2": "",
            "q3": "",
        }
        self.is_analyzing = False
        self.final_level: Optional[Literal['explorer', 'adventurer', 'scholar', 'researcher']] = None

        # Data option collections
        self.q1_options = [
            {"label": "No, never heard of it", "value": "never"},
            {"label": "I've heard of it briefly", "value": "yes_basic"},
            {"label": "I've read some articles/books", "value": "yes_studied"},
            {"label": "I've studied or worked with it actively", "value": "yes_worked"},
        ]

        self.q3_options = [
            {"label": "None in particular / General knowledge seeker", "value": "none"},
            {"label": "Physics background", "value": "physics"},
            {"label": "Mathematics background", "value": "maths"},
            {"label": "Computer Science or Engineering background", "value": "cs"},
            {"label": "Active Quantum researcher or graduate student", "value": "researcher"},
        ]

        self.level_details = {
            "explorer": {"name": "Quantum Explorer", "color": "Cyan", "desc": "Perfect for beginners. Focuses on simple conceptual stories without rigorous mathematics."},
            "adventurer": {"name": "Quantum Adventurer", "color": "Purple", "desc": "Ideal for curious thinkers. Explores real probability values and wave intuition models."},
            "scholar": {"name": "Quantum Scholar", "color": "Blue", "desc": "Advanced track. Implements standard Dirac bra-ket notations and algebraic Born rules."},
            "researcher": {"name": "Quantum Researcher", "color": "Gold", "desc": "Expert level seminar style. Investigates pure matrix matrices, density fields, and operators."},
        }

    def run_assessment_loop(self):
        """Drives the text console view state steps until a final stream rating is locked."""
        while self.final_level is None:
            if self.step == 1:
                self._prompt_q1()
            elif self.step == 2:
                self._prompt_q2()
            elif self.step == 3:
                self._prompt_q3()
            elif self.step == 4:
                self._process_analysis()

        # Step 5: Final Confirmation View Screen
        print("\n" + "🎓" * 20)
        print("🎉  ASSESSMENT REGISTRATION COMPLETE!")
        print("🎓" * 20)
        details = self.level_details[self.final_level]
        print(f"   Stream Assigned : {details['name'].upper()} ({details['color']})")
        print(f"   Profile Details : {details['desc']}")
        print("-" * 55)
        print("   [✓] Custom explanations configured.")
        print("   [✓] Level-appropriate simulations cached.")
        print("   [✓] Tutor persona initialized.")
        print("-" * 55)
        
        input("Press Enter to launch quantum gateway workspace module...")
        self.on_level_determined(self.final_level)

    def _prompt_q1(self):
        print("\n" + "🎓" * 20)
        print("📝  STEP 1 of 3: Familiarity Check")
        print("🎓" * 20)
        print("   Have you ever encountered Quantum Computing or Mechanics before?")
        for idx, opt in enumerate(self.q1_options, 1):
            print(f"     [{idx}] {opt['label']}")
        
        choice = input("\nSelect index option: ").strip()
        if choice in ["1", "2", "3", "4"]:
            self.answers["q1"] = self.q1_options[int(choice) - 1]["value"]
            self.step = 2
        else:
            print("[Input Warning]: Invalid selection index.")

    def _prompt_q2(self):
        print("\n" + "🎓" * 20)
        print("📝  STEP 2 of 3: Conceptual Intuition Check")
        print("🎓" * 20)
        print("   In your own words, what does the term 'Superposition' mean to you?")
        print("   (Feel free to type whatever comes to mind, or hit Enter to skip)")
        
        user_text = input("\n✍️  Your definition: ").strip()
        self.answers["q2"] = user_text if user_text else "skipped"
        self.step = 3

    def _prompt_q3(self):
        print("\n" + "🎓" * 20)
        print("📝  STEP 3 of 3: Academic Background Channel")
        print("🎓" * 20)
        print("   What