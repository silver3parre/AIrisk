import logging

# Configure logging
logger = logging.getLogger(__name__)

# Configuration for the Chat Flow
CHAT_FLOW = {
    'PERSONA_1': {
        'next': 'PERSONA_2',
        'prompt': "Hello there. I'm your Risk Assessment Assistant. Before we dive into the scary stuff, let's get to know each other. How would you describe your role? (e.g., 'I fix things', 'I manage people', 'I worry about compliance')",
        'options': [],
        'save_list': 'persona_answers'
    },
    'PERSONA_2': {
        'next': 'PERSONA_3',
        'prompt': "Interesting. And when you're working on a project, do you prefer the big picture or the nitty-gritty details?",
        'options': ["Big Picture", "Details", "Both"],
        'save_list': 'persona_answers'
    },
    'PERSONA_3': {
        'next': 'PERSONA_4',
        'prompt': "Noted. How do you handle deadlines? Are you a 'plan everything weeks ahead' person or a 'thrive in the chaos of the last minute' type?",
        'options': ["Planner", "Chaos Surfer"],
        'save_list': 'persona_answers'
    },
    'PERSONA_4': {
        'next': 'PERSONA_5',
        'prompt': "We all have our methods. Now, if this application were a car, would it be a reliable sedan, a flashy sports car, or an armored tank?",
        'options': ["Sedan", "Sports Car", "Tank"],
        'save_list': 'persona_answers'
    },
    'PERSONA_5': {
        'next': 'SCOPING_TITLE',
        'prompt': "Last one: Coffee, Tea, or 'Don't talk to me until I've had my energy drink'?",
        'options': ["Coffee", "Tea", "Energy Drink"],
        'save_list': 'persona_answers'
    },
    'SCOPING_TITLE': {
        'next': 'SCOPING_CATEGORY',
        'prompt': "Alright, calibration complete. I think we'll get along just fine. Let's start the assessment. What shall we call this masterpiece of risk analysis?",
        'options': [],
        'save_field': 'title'
    },
    'SCOPING_CATEGORY': {
        'next': 'SCOPING_DESCRIPTION',
        'prompt': lambda data: f"'{data.get('title')}' it is. How would you categorize the security level? Low, Moderate, or High?",
        'options': ["Low", "Moderate", "High"],
        'save_field': 'security_categorization'
    },
    'SCOPING_DESCRIPTION': {
        'next': 'ASSET_NAME',
        'prompt': "And in a few words, what does this system actually do? (The 'Elevator Pitch', if you will)",
        'options': [],
        'save_field': 'description'
    },
    'ASSET_NAME': {
        'next': 'ASSET_TYPE',
        'prompt': "Let's talk assets. What is the specific thing we are protecting today? (e.g., Customer Database, The Mainframe)",
        'options': [],
        'save_field': 'asset_name'
    },
    'ASSET_TYPE': {
        'next': 'ASSET_VALUATION',
        'prompt': "Got it. And what type of asset is that?",
        'options': ["Data", "Software", "Hardware", "Service"],
        'save_field': 'asset_type'
    },
    'ASSET_VALUATION': {
        'next': 'THREAT_SOURCE',
        'prompt': "If you had to put a price tag on it, what's the estimated value? (Just a number, no currency symbols needed)",
        'options': [],
        'save_field': 'asset_valuation'
    },
    'THREAT_SOURCE': {
        'next': 'THREAT_EVENT',
        'prompt': "Now for the antagonists. Who are we worried about? (e.g., Hacktivists, Insiders, Nation States)",
        'options': ["Hacker", "Insider", "Competitor", "Nation State"],
        'save_field': 'threat_source'
    },
    'THREAT_EVENT': {
        'next': 'CAPABILITY',
        'prompt': "And what are they trying to do? (e.g., Phishing, DDoS, Stealing Secrets)",
        'options': [],
        'save_field': 'threat_event'
    },
    'CAPABILITY': {
        'next': 'INTENT',
        'prompt': "How capable is this adversary? From 'Script Kiddie' (Very Low) to 'State Sponsored' (Very High).",
        'options': ["Very Low", "Low", "Moderate", "High", "Very High"],
        'save_field': 'capability'
    },
    'INTENT': {
        'next': 'TARGETING',
        'prompt': "How motivated are they? Is this accidental (Very Low) or are they on a mission (Very High)?",
        'options': ["Very Low", "Low", "Moderate", "High", "Very High"],
        'save_field': 'intent'
    },
    'TARGETING': {
        'next': 'LIKELIHOOD_INITIATION',
        'prompt': "Are they targeting YOU specifically, or just casting a wide net?",
        'options': ["Very Low (Broad)", "Moderate (Specific)", "Very High (Persistent)"],
        'save_field': 'targeting'
    },
    'LIKELIHOOD_INITIATION': {
        'next': 'VULNERABILITY',
        'prompt': "Given all that, how likely are they to actually try something? (1-5)",
        'options': ["1", "2", "3", "4", "5"],
        'save_field': 'likelihood_initiation'
    },
    'VULNERABILITY': {
        'next': 'LIKELIHOOD_IMPACT',
        'prompt': "What is the weak link? The vulnerability they might exploit? (e.g., Unpatched Server, Weak Passwords)",
        'options': [],
        'save_field': 'vulnerability'
    },
    'LIKELIHOOD_IMPACT': {
        'next': 'IMPACT_LEVEL',
        'prompt': "If they try, how likely are they to succeed? (1-5)",
        'options': ["1", "2", "3", "4", "5"],
        'save_field': 'likelihood_impact'
    },
    'IMPACT_LEVEL': {
        'next': 'FINANCIAL_IMPACT',
        'prompt': "If they succeed, how bad is it? (1-5)",
        'options': ["1", "2", "3", "4", "5"],
        'save_field': 'impact_level'
    },
    'FINANCIAL_IMPACT': {
        'next': 'BIA_REPUTATION',
        'prompt': "Can you estimate the financial loss in dollars? (Rough guess is fine)",
        'options': [],
        'save_field': 'financial_impact'
    },
    'BIA_REPUTATION': {
        'next': 'BIA_LEGAL',
        'prompt': "Almost done. What about reputational damage?",
        'options': ["None", "Low", "Moderate", "High", "Critical"],
        'save_field': 'bia_reputation'
    },
    'BIA_LEGAL': {
        'next': 'BIA_OPERATIONAL',
        'prompt': "Legal consequences?",
        'options': ["None", "Low", "Moderate", "High"],
        'save_field': 'bia_legal'
    },
    'BIA_OPERATIONAL': {
        'next': 'BIA_SAFETY',
        'prompt': "How long would operations be down?",
        'options': ["None", "< 1 hour", "1-24 hours", "1-7 days", "> 1 week"],
        'save_field': 'bia_operational'
    },
    'BIA_SAFETY': {
        'next': 'COMPLETED',
        'prompt': "Finally, any safety concerns?",
        'options': ["None", "Low", "Moderate", "High"],
        'save_field': 'bia_safety'
    },
    'COMPLETED': {
        'next': None,
        'prompt': "Excellent work. I have all the data I need. I'm compiling the report now...",
        'options': ["View Dashboard"],
        'save_field': None
    }
}

class ChatSession:
    def __init__(self, session_data=None):
        if session_data is None:
            session_data = {}
        
        self.step = session_data.get('step', 'PERSONA_1')
        self.data = session_data.get('data', {})
        self.persona_answers = session_data.get('persona_answers', [])
        self.history = session_data.get('history', []) # List of {sender: 'bot'/'user', text: '...'}

    def to_dict(self):
        return {
            'step': self.step,
            'data': self.data,
            'persona_answers': self.persona_answers,
            'history': self.history
        }

    def add_message(self, sender, text, options=None):
        self.history.append({'sender': sender, 'text': text, 'options': options})

    def get_last_message(self):
        if self.history:
            return self.history[-1]
        return None

    def handle_input(self, user_input):
        # Log the input for debugging
        logger.info(f"Handling input for step {self.step}: {user_input}")
        
        # Get current step config
        current_config = CHAT_FLOW.get(self.step)
        
        if not current_config:
            return "Error: Unknown step.", []

        # Save Input
        if 'save_list' in current_config:
            self.persona_answers.append(user_input)
        elif 'save_field' in current_config and current_config['save_field']:
            self.data[current_config['save_field']] = user_input
            
        # Move to next step
        next_step = current_config.get('next')
        if next_step:
            self.step = next_step
        
        return self.generate_response()

    def generate_response(self):
        # Get current step config
        config = CHAT_FLOW.get(self.step)
        
        if not config:
            return "I'm not sure what comes next.", []
            
        # Determine prompt
        prompt = config.get('prompt')
        if callable(prompt):
            response_text = prompt(self.data)
        else:
            response_text = prompt
            
        options = config.get('options', [])
        
        return response_text, options
