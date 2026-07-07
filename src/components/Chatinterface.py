import re
import time
from typing import Dict, Literal, List, TypedDict, Optional

# ==========================================
# TYPE DEFINITIONS & MODELS
# ==========================================
KnowledgeLevel = Literal['explorer', 'adventurer', 'scholar', 'researcher']

class Message(TypedDict):
    role: Literal['user', 'ai']
    text: str
    timestamp: float
    citations: Optional[List[Dict[str, str]]]

class Toast(TypedDict):
    id: str
    message: str
    type: Literal['xp', 'badge', 'info']

class ValidationResult(TypedDict):
    pass_: bool
    violation: Optional[str]

class AwardResult(TypedDict):
    approved: bool
    clamped: int


# ==========================================
# FROM: scripts.ts (Core Logic & Guards)
# ==========================================

def extract_clean_response(raw_text: str, level: KnowledgeLevel) -> str:
    """Cleans generated text according to voice signals and removes leakage."""
    if not raw_text or not raw_text.strip():
        return raw_text

    signals: Dict[str, re.Pattern] = {
        'explorer':   re.compile(r'\n(Imagine|Think of|Here\'s the cool|Oh!|Wow|Picture|Remember)[^\n]', re.IGNORECASE),
        'adventurer': re.compile(r'\n(Here\'s what|Fascinating|Try to|Watch|Now|Let\'s)[^\n]', re.IGNORECASE),
        'scholar':    re.compile(r'\n(Before|That\'s|What if|Consider|Precisely|Notice)[^\n]', re.IGNORECASE),
        'researcher': re.compile(r'\n(The|Consider|This|Your|Given|Interestingly)[^\n]', re.IGNORECASE),
    }

    signal = signals.get(level)
    if signal:
        match = signal.search(raw_text)
        if match:
            start_word = match.group(1)
            idx = raw_text.find(start_word, match.start())
            if idx != -1:
                return raw_text[idx:].strip()

    if re.search(r'Step \d+:', raw_text, re.IGNORECASE):
        parts = re.split(r'Step \d+:', raw_text, flags=re.IGNORECASE)
        return parts[-1].strip(" '\"")

    leakage_patterns = [
        r'^The (user|learner|student) (wants|is|has|asked).+$',
        r'^The current (topic|level|curriculum|context).+$',
        r'^I should.+$',
        r'^I will.+$',
        r'^Plan:.+$',
        r'^Step \d+:.+$',
        r'^As per.+$',
        r'^Note:.+$',
    ]

    cleaned_lines = []
    for line in raw_text.splitlines():
        if not any(re.match(p, line, re.IGNORECASE) for p in leakage_patterns):
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def detect_knowledge_level(answers: Dict[str, str]) -> KnowledgeLevel:
    """Evaluates questionnaire answers to compute initial aptitude tier."""
    score = 0
    if answers.get('q1') == 'yes_basic': score += 1
    elif answers.get('q1') == 'yes_studied': score += 2
    elif answers.get('q1') == 'yes_worked': score += 3

    q2_lower = answers.get('q2', '').lower()
    if 'superposition' in q2_lower: score += 2
    if '0 and 1' in q2_lower: score += 1
    if 'amplitude' in q2_lower: score += 2
    if 'bloch' in q2_lower: score += 3

    q3 = answers.get('q3')
    if q3 in ('physics', 'maths'): score += 2
    elif q3 == 'cs': score += 1
    elif q3 == 'researcher': score += 4

    if score <= 2: return 'explorer'
    if score <= 5: return 'adventurer'
    if score <= 8: return 'scholar'
    return 'researcher'


def validate_physics_output(text: str) -> ValidationResult:
    """Scans text for unauthorized quantum mechanics misconceptions."""
    lower = text.lower()
    blocked = [
        'electron splits in two',
        'tries all answers simultaneously',
        'faster than light communication',
        'conscious observer',
        'camera physically disturbs',
        'qubits hold more information',
        'quantum means anything is possible',
    ]
    for phrase in blocked:
        if phrase in lower:
            return {'pass_': False, 'violation': phrase}
    return {'pass_': True, 'violation': None}


def guard_award_points(points: float, level: str) -> AwardResult:
    """Clamps assigned XP points inside level boundaries."""
    limits = {
        'explorer':   (10, 30),
        'adventurer': (20, 50),
        'scholar':    (50, 100),
        'researcher': (10, 150),
    }
    min_val, max_val = limits.get(level, (10, 50))
    clamped = max(min_val, min(round(points), max_val))
    return {'approved': points > 0, 'clamped': clamped}


# ==========================================
# FROM: ChatInterface.tsx (Console UI Layer)
# ==========================================

class TerminalChatInterface:
    def __init__(self, current_topic_title: str, accent_color: str = "PURPLE"):
        self.chat_history: List[Message] = []
        self.toasts: List[Toast] = []
        self.current_topic_title = current_topic_title
        self.accent_color = accent_color
        self.is_typing = False

    def render_ui(self):
        """Renders the terminal equivalent of the React interface framework."""
        # Clear screen helper (optional, uncomment for standalone app feel)
        # print("\033[H\033[2J", end="")
        
        print("\n" + "=" * 60)
        print(f"⚛️  QUANTUM TUTOR | Topic: {self.current_topic_title.upper()}")
        print("=" * 60)

        if not self.chat_history:
            print("\n   [🧭] The tutor is waiting to guide you.")
            print("   Ask \"What is this topic about?\" or say \"Let's start!\" to begin.\n")
        else:
            for msg in self.chat_history:
                timestamp_str = time.strftime('%H:%M', time.localtime(msg['timestamp']))
                if msg['role'] == 'ai':
                    print(f"\n⚛️  Tutor [{timestamp_str}]:")
                    print(f"   {msg['text']}")
                    if msg.get('citations'):
                        cite_list = [f"[{c['title']}]" for c in msg['citations']]
                        print(f"   📚 Citations: {', '.join(cite_list)}")
                else:
                    print(f"\n👤 You [{timestamp_str}]:\n   {msg['text']}")
        
        if self.is_typing:
            print("\n⚛️  Tutor is typing . . .")
            time.sleep(1)

        # Floating XP Toasts overlay simulation
        if self.toasts:
            print("\n" + "-" * 30)
            for toast in self.toasts:
                icon = "✨" if toast['type'] == 'xp' else "🏆"
                print(f"   {icon} {toast['message']}")
            print("-" * 30)
            self.toasts.clear()  # Clear after rendering to simulate ephemeral display

        # Quick Actions display
        print("\n" + "." * 60)
        print("💡 [1] I'm stuck  |  🍎 [2] Give analogy  |  🏁 [3] Complete topic")
        print("." * 60)

    def add_toast(self, message: str, toast_type: Literal['xp', 'badge', 'info']):
        toast_id = str(time.time())
        self.toasts.append({'id': toast_id, 'message': message, 'type': toast_type})

    def trigger_ai_response(self, user_text: str):
        """Simulates response handling, evaluation, and background parsing."""
        self.is_typing = True
        self.render_ui()
        
        # Simulated responses mimicking skillDefinitions.ts profiles
        self.is_typing = False
        ai_raw_text = "\nImagine a spinning coin. Here's the cool part: it's both heads and tails!"
        
        # Run filters from scripts.ts
        cleaned_text = extract_clean_response(ai_raw_text, 'explorer')
        
        # Verify physics safety rules
        safety_check = validate_physics_output(cleaned_text)
        if not safety_check['pass_']:
            cleaned_text = f"Output blocked due to misconception warning: {safety_check['violation']}"

        self.chat_history.append({
            'role': 'ai',
            'text': cleaned_text,
            'timestamp': time.time(),
            'citations': [{'title': 'Quantum Coins 101', 'url': 'https://example.edu'}]
        })

    def handle_input(self, user_input: str):
        """Processes input or mapped quick-actions directly from the client window."""
        if not user_input.strip():
            return

        # Map Quick Action shortcut keys to message text strings
        if user_input.strip() == "1":
            user_input = "I'm stuck on this topic, can you give me a hint?"
        elif user_input.strip() == "2":
            user_input = "Can you explain this with a simpler analogy?"
        elif user_input.strip() == "3":
            user_input = "I understand this topic! Let's check completion and move to next."

        self.chat_history.append({
            'role': 'user',
            'text': user_input,
            'timestamp': time.time()
        })
        
        # Simulate an XP gift for interacting
        xp_status = guard_award_points(25, 'explorer')
        if xp_status['approved']:
            self.add_toast(f"You just earned {xp_status['clamped']} quantum XP! ✨", "xp")

        self.trigger_ai_response(user_input)


# Executable runtime instance sandbox
if __name__ == "__main__":
    interface = TerminalChatInterface(current_topic_title="The Magic Quantum Coin")
    
    # Run a simple 2-turn execution loop to show functional integrity
    interface.render_ui()
    print("\n[System]: Simulating user selecting Quick Action '2'...")
    interface.handle_input("2")
    interface.render_ui()