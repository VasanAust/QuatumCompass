"""
TYPES DEFINITIONS (Equivalent to types.ts)

Provides static typing structures, literal validations, and record layouts 
for state engines and action dispatches across the terminal runtime ecosystem.
"""

from typing import List, Dict, Literal, TypedDict, Union, Optional, Any

# ==========================================
# 1. CORE DATA STRUCTURE MODELS
# ==========================================

class Citation(TypedDict):
    title: str
    url: str

class ChatMessage(TypedDict):
    role: Literal['user', 'ai']
    text: str
    timestamp: int  # Unix epoch milliseconds/seconds
    citations: Optional[List[Citation]]

class ToastNotification(TypedDict):
    id: str
    message: str
    type: Literal['xp', 'badge', 'info']

class AppState(TypedDict):
    screen: Literal['api_setup', 'assessment', 'learning', 'level_complete', 'settings']
    apiKey: str
    level: Optional[Literal['explorer', 'adventurer', 'scholar', 'researcher']]
    assessmentAnswers: Dict[str, str]
    assessmentStep: int
    currentTopicIndex: int
    completedTopicIds: List[str]
    earnedBadgeIds: List[str]
    xp: int
    chatHistory: List[ChatMessage]
    activeSimulation: Optional[str]
    isTyping: bool
    sessionMessageCount: int
    toasts: List[ToastNotification]


# ==========================================
# 2. REDUCER ACTION UNION SCHEMA
# ==========================================

class AppAction(TypedDict, total=False):
    """
    Simulates TypeScript's Discriminated Union Action Types using a 
    standard configuration dictionary container layout.
    """
    type: Literal[
        'SET_API_KEY',
        'SET_LEVEL',
        'SUBMIT_ASSESSMENT_ANSWER',
        'NEXT_ASSESSMENT_STEP',
        'PREV_ASSESSMENT_STEP',
        'SET_SCREEN',
        'SELECT_TOPIC',
        'COMPLETE_TOPIC',
        'AWARD_XP',
        'AWARD_BADGE',
        'ADD_CHAT_MESSAGE',
        'CLEAR_TOASTS',
        'REMOVE_TOAST',
        'RESET_PROGRESS',
        'LOAD_PERSISTED_STATE'
    ]
    payload: Any  # Contextual values mapped dynamically by action handlers