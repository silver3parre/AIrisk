import logging

# Configure logging
logger = logging.getLogger(__name__)

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
        
        # 1. Validate/Process Input based on CURRENT step
        next_step = self.step
        
        if self.step.startswith('PERSONA_'):
            self.persona_answers.append(user_input)
            if self.step == 'PERSONA_1': next_step = 'PERSONA_2'
            elif self.step == 'PERSONA_2': next_step = 'PERSONA_3'
            elif self.step == 'PERSONA_3': next_step = 'PERSONA_4'
            elif self.step == 'PERSONA_4': next_step = 'PERSONA_5'
            elif self.step == 'PERSONA_5': next_step = 'SCOPING_TITLE'
            
        elif self.step == 'SCOPING_TITLE':
            self.data['title'] = user_input
            next_step = 'SCOPING_CATEGORY'
            
        elif self.step == 'SCOPING_CATEGORY':
            self.data['security_categorization'] = user_input
            next_step = 'SCOPING_DESCRIPTION'
            
        elif self.step == 'SCOPING_DESCRIPTION':
            self.data['description'] = user_input
            next_step = 'ASSET_NAME'
            
        elif self.step == 'ASSET_NAME':
            self.data['asset_name'] = user_input
            next_step = 'ASSET_TYPE'
            
        elif self.step == 'ASSET_TYPE':
            self.data['asset_type'] = user_input
            next_step = 'ASSET_VALUATION'
            
        elif self.step == 'ASSET_VALUATION':
            self.data['asset_valuation'] = user_input
            next_step = 'THREAT_SOURCE'
            
        elif self.step == 'THREAT_SOURCE':
            self.data['threat_source'] = user_input
            next_step = 'THREAT_EVENT'
            
        elif self.step == 'THREAT_EVENT':
            self.data['threat_event'] = user_input
            next_step = 'CAPABILITY'
            
        elif self.step == 'CAPABILITY':
            self.data['capability'] = user_input
            next_step = 'INTENT'
            
        elif self.step == 'INTENT':
            self.data['intent'] = user_input
            next_step = 'TARGETING'
            
        elif self.step == 'TARGETING':
            self.data['targeting'] = user_input
            next_step = 'LIKELIHOOD_INITIATION'
            
        elif self.step == 'LIKELIHOOD_INITIATION':
            self.data['likelihood_initiation'] = user_input
            next_step = 'VULNERABILITY'
            
        elif self.step == 'VULNERABILITY':
            self.data['vulnerability'] = user_input
            next_step = 'LIKELIHOOD_IMPACT'
            
        elif self.step == 'LIKELIHOOD_IMPACT':
            self.data['likelihood_impact'] = user_input
            next_step = 'IMPACT_LEVEL'
            
        elif self.step == 'IMPACT_LEVEL':
            self.data['impact_level'] = user_input
            next_step = 'FINANCIAL_IMPACT'
            
        elif self.step == 'FINANCIAL_IMPACT':
            self.data['financial_impact'] = user_input
            next_step = 'BIA_REPUTATION'
            
        elif self.step == 'BIA_REPUTATION':
            self.data['bia_reputation'] = user_input
            next_step = 'BIA_LEGAL'
            
        elif self.step == 'BIA_LEGAL':
            self.data['bia_legal'] = user_input
            next_step = 'BIA_OPERATIONAL'
            
        elif self.step == 'BIA_OPERATIONAL':
            self.data['bia_operational'] = user_input
            next_step = 'BIA_SAFETY'
            
        elif self.step == 'BIA_SAFETY':
            self.data['bia_safety'] = user_input
            next_step = 'COMPLETED'

        self.step = next_step
        return self.generate_response()

    def generate_response(self):
        # Return (text, options_list) based on CURRENT step (which was just updated)
        
        # Persona Questions (Light, professional, understated humor)
        if self.step == 'PERSONA_1':
            return "Hello there. I'm your Risk Assessment Assistant. Before we dive into the scary stuff, let's get to know each other. How would you describe your role? (e.g., 'I fix things', 'I manage people', 'I worry about compliance')", []
        elif self.step == 'PERSONA_2':
            return "Interesting. And when you're working on a project, do you prefer the big picture or the nitty-gritty details?", ["Big Picture", "Details", "Both"]
        elif self.step == 'PERSONA_3':
            return "Noted. How do you handle deadlines? Are you a 'plan everything weeks ahead' person or a 'thrive in the chaos of the last minute' type?", ["Planner", "Chaos Surfer"]
        elif self.step == 'PERSONA_4':
            return "We all have our methods. Now, if this application were a car, would it be a reliable sedan, a flashy sports car, or an armored tank?", ["Sedan", "Sports Car", "Tank"]
        elif self.step == 'PERSONA_5':
            return "Last one: Coffee, Tea, or 'Don't talk to me until I've had my energy drink'?", ["Coffee", "Tea", "Energy Drink"]
            
        # Scoping
        elif self.step == 'SCOPING_TITLE':
            return "Alright, calibration complete. I think we'll get along just fine. Let's start the assessment. What shall we call this masterpiece of risk analysis?", []
        elif self.step == 'SCOPING_CATEGORY':
            return f"'{self.data.get('title')}' it is. How would you categorize the security level? Low, Moderate, or High?", ["Low", "Moderate", "High"]
        elif self.step == 'SCOPING_DESCRIPTION':
            return "And in a few words, what does this system actually do? (The 'Elevator Pitch', if you will)", []
            
        # Asset
        elif self.step == 'ASSET_NAME':
            return "Let's talk assets. What is the specific thing we are protecting today? (e.g., Customer Database, The Mainframe)", []
        elif self.step == 'ASSET_TYPE':
            return "Got it. And what type of asset is that?", ["Data", "Software", "Hardware", "Service"]
        elif self.step == 'ASSET_VALUATION':
            return "If you had to put a price tag on it, what's the estimated value? (Just a number, no currency symbols needed)", []
            
        # Threat
        elif self.step == 'THREAT_SOURCE':
            return "Now for the antagonists. Who are we worried about? (e.g., Hacktivists, Insiders, Nation States)", ["Hacker", "Insider", "Competitor", "Nation State"]
        elif self.step == 'THREAT_EVENT':
            return "And what are they trying to do? (e.g., Phishing, DDoS, Stealing Secrets)", []
        elif self.step == 'CAPABILITY':
            return "How capable is this adversary? From 'Script Kiddie' (Very Low) to 'State Sponsored' (Very High).", ["Very Low", "Low", "Moderate", "High", "Very High"]
        elif self.step == 'INTENT':
            return "How motivated are they? Is this accidental (Very Low) or are they on a mission (Very High)?", ["Very Low", "Low", "Moderate", "High", "Very High"]
        elif self.step == 'TARGETING':
            return "Are they targeting YOU specifically, or just casting a wide net?", ["Very Low (Broad)", "Moderate (Specific)", "Very High (Persistent)"]
            
        # Likelihood
        elif self.step == 'LIKELIHOOD_INITIATION':
            return "Given all that, how likely are they to actually try something? (1-5)", ["1", "2", "3", "4", "5"]
        elif self.step == 'VULNERABILITY':
            return "What is the weak link? The vulnerability they might exploit? (e.g., Unpatched Server, Weak Passwords)", []
        elif self.step == 'LIKELIHOOD_IMPACT':
            return "If they try, how likely are they to succeed? (1-5)", ["1", "2", "3", "4", "5"]
            
        # Impact
        elif self.step == 'IMPACT_LEVEL':
            return "If they succeed, how bad is it? (1-5)", ["1", "2", "3", "4", "5"]
        elif self.step == 'FINANCIAL_IMPACT':
            return "Can you estimate the financial loss in dollars? (Rough guess is fine)", []
            
        # BIA
        elif self.step == 'BIA_REPUTATION':
            return "Almost done. What about reputational damage?", ["None", "Low", "Moderate", "High", "Critical"]
        elif self.step == 'BIA_LEGAL':
            return "Legal consequences?", ["None", "Low", "Moderate", "High"]
        elif self.step == 'BIA_OPERATIONAL':
            return "How long would operations be down?", ["None", "< 1 hour", "1-24 hours", "1-7 days", "> 1 week"]
        elif self.step == 'BIA_SAFETY':
            return "Finally, any safety concerns?", ["None", "Low", "Moderate", "High"]
            
        elif self.step == 'COMPLETED':
            return "Excellent work. I have all the data I need. I'm compiling the report now...", ["View Dashboard"]
            
        return "I'm not sure what comes next.", []
