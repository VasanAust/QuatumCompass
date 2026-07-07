import re
from typing import Dict, Literal, TypedDict, Optional

# Define Type aliases for the different persona voice levels
KnowledgeLevel = Literal['explorer', 'adventurer', 'scholar', 'researcher']

class ValidationResult(TypedDict):
    pass_: bool  # 'pass' is a reserved keyword in Python, so using 'pass_'
    violation: Optional[str]

class AwardResult(TypedDict):
    approved: bool
    clamped: int


def extract_clean_response(raw_text: str, level: KnowledgeLevel) -> str:
    """
    Cleans up the generated text by finding valid voice signals, removing step markers,
    or filtering out line-by-line model leakage based on the learner's knowledge level.
    """
    if not raw_text or not raw_text.strip():
        return raw_text

    # Voice signal patterns per level
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
            # Replicate the substring extraction logic from the original JS/TS index-matching rule
            start_word = match.group(1)
            # Find the true starting index of that matched phrase inside the original string
            idx = raw_text.find(start_word, match.start())
            if idx != -1:
                return raw_text[idx:].strip()

    # Strip Step X: structure
    if re.search(r'Step \d+:', raw_text, re.IGNORECASE):
        parts = re.split(r'Step \d+:', raw_text, flags=re.IGNORECASE)
        # Grab the last item and strip out leading/trailing quote characters
        return parts[-1].strip(" '\"")

    # Line-by-line leakage removal
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
    # Split by lines to emulate the multiline (`m`) and global (`g`) replacement in Python
    for line in raw_text.splitlines():
        should_remove = False
        for pattern in leakage_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                should_remove = True
                break
        if not should_remove:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def detect_knowledge_level(answers: Dict[str, str]) -> KnowledgeLevel:
    """
    Evaluates questionnaire answers to compute an aptitude score and returns
    the appropriate knowledge level tier.
    """
    score = 0

    # Q1: Have you heard of quantum computing?
    q1 = answers.get('q1')
    if q1 == 'yes_basic':
        score += 1
    elif q1 == 'yes_studied':
        score += 2
    elif q1 == 'yes_worked':
        score += 3

    # Q2: What is a qubit?
    q2_lower = answers.get('q2', '').lower()
    if 'superposition' in q2_lower:
        score += 2
    if '0 and 1' in q2_lower:
        score += 1
    if 'amplitude' in q2_lower:
        score += 2
    if 'bloch' in q2_lower:
        score += 3

    # Q3: Background
    q3 = answers.get('q3')
    if q3 in ('physics', 'maths'):
        score += 2
    elif q3 == 'cs':
        score += 1
    elif q3 == 'researcher':
        score += 4

    if score <= 2:
        return 'explorer'
    if score <= 5:
        return 'adventurer'
    if score <= 8:
        return 'scholar'
    return 'researcher'


def validate_physics_output(text: str) -> ValidationResult:
    """
    Scans the given text for unauthorized quantum mechanics misconceptions.
    """
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
    """
    Ensures assigned XP values stay within the strict boundaries dictated by 
    the gamification profile rules of the user's level tier.
    """
    limits = {
        'explorer':   (10, 30),
        'adventurer': (20, 50),
        'scholar':    (50, 100),
        'researcher': (10, 150),
    }
    
    min_val, max_val = limits.get(level, (10, 50))
    # Round to closest integer to mirror JS Math.round behavior
    rounded_points = round(points)
    clamped = max(min_val, min(rounded_points, max_val))
    
    return {'approved': points > 0, 'clamped': clamped}