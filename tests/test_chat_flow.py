import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_logic import ChatSession, CHAT_FLOW

def test_chat_flow():
    print("Starting Chat Flow Test...")
    cs = ChatSession()
    
    # 1. Persona Phase
    steps = ['PERSONA_1', 'PERSONA_2', 'PERSONA_3', 'PERSONA_4', 'PERSONA_5']
    for step in steps:
        assert cs.step == step, f"Expected {step}, got {cs.step}"
        response, options = cs.handle_input("Test Answer")
        print(f"[{step}] Response: {response[:50]}...")
        
    # 2. Scoping Phase
    assert cs.step == 'SCOPING_TITLE'
    cs.handle_input("My Test App")
    assert cs.data['title'] == "My Test App"
    
    assert cs.step == 'SCOPING_CATEGORY'
    cs.handle_input("High")
    assert cs.data['security_categorization'] == "High"
    
    # 3. Fast forward through others
    inputs = {
        'SCOPING_DESCRIPTION': 'A test app',
        'ASSET_NAME': 'The Database',
        'ASSET_TYPE': 'Data',
        'ASSET_VALUATION': '1000000',
        'THREAT_SOURCE': 'Hacker',
        'THREAT_EVENT': 'Hacking',
        'CAPABILITY': 'High',
        'INTENT': 'High',
        'TARGETING': 'High',
        'LIKELIHOOD_INITIATION': '5',
        'VULNERABILITY': 'Weak Password',
        'LIKELIHOOD_IMPACT': '5',
        'IMPACT_LEVEL': '5',
        'FINANCIAL_IMPACT': '50000',
        'BIA_REPUTATION': 'High',
        'BIA_LEGAL': 'High',
        'BIA_OPERATIONAL': 'High',
        'BIA_SAFETY': 'None'
    }
    
    for step, input_val in inputs.items():
        print(f"Current Step: {cs.step}")
        assert cs.step == step, f"Expected {step}, got {cs.step}"
        cs.handle_input(input_val)
        
    assert cs.step == 'COMPLETED'
    print("Chat Flow Test Passed!")

if __name__ == "__main__":
    test_chat_flow()
