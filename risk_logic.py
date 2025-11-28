def get_likelihood_level(value):
    levels = {1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'}
    return levels.get(value, 'Unknown')

def get_impact_level(value):
    levels = {1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'}
    return levels.get(value, 'Unknown')

def get_risk_level(value):
    levels = {1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High'}
    return levels.get(value, 'Unknown')

def calculate_overall_likelihood(initiation, impact_likelihood):
    # NIST 800-30 Table G-5: Overall Likelihood
    # This is a simplified matrix interpretation
    # Initiation (rows) x Impact Likelihood (cols)
    
    # Let's use a max-based approach or average rounded up as a proxy for the matrix 
    # if we don't implement the exact 5x5 matrix.
    # However, NIST usually implies:
    # Low x Low = Low
    # High x High = High
    # High x Low = Moderate (roughly)
    
    # Implementing a basic matrix for accuracy
    # Rows: Initiation (1-5), Cols: Impact Likelihood (1-5)
    # Updated Matrix based on standard NIST interpretation
    # Rows: Initiation (1-5), Cols: Impact Likelihood (1-5)
    matrix = [
        [1, 1, 1, 2, 2], # Very Low Initiation
        [1, 2, 2, 3, 3], # Low Initiation
        [1, 2, 3, 3, 4], # Moderate Initiation
        [2, 3, 3, 4, 5], # High Initiation
        [2, 3, 4, 5, 5]  # Very High Initiation
    ]
    
    # Adjust for 0-index
    r = max(0, min(4, int(initiation) - 1))
    c = max(0, min(4, int(impact_likelihood) - 1))
    
    return matrix[r][c]

def calculate_risk(likelihood, impact):
    # NIST 800-30 Table I-2: Level of Risk
    # Likelihood (rows) x Impact (cols)
    
    # Updated Matrix based on standard NIST interpretation
    matrix = [
        [1, 1, 1, 2, 2], # Very Low Likelihood
        [1, 2, 2, 3, 3], # Low Likelihood
        [1, 2, 3, 3, 4], # Moderate Likelihood
        [2, 3, 3, 4, 5], # High Likelihood
        [2, 3, 4, 5, 5]  # Very High Likelihood
    ]
    
    r = max(0, min(4, int(likelihood) - 1))
    c = max(0, min(4, int(impact) - 1))
    
    return matrix[r][c]

def calculate_risk_details(data):
    try:
        l_init = int(data.get('likelihood_initiation', 1))
        l_impact = int(data.get('likelihood_impact', 1))
        impact = int(data.get('impact_level', 1))
        
        overall_likelihood = calculate_overall_likelihood(l_init, l_impact)
        risk_score = calculate_risk(overall_likelihood, impact)
        
        return {
            'threat_source': data.get('threat_source'),
            'threat_event': data.get('threat_event'),
            'capability': data.get('capability'),
            'intent': data.get('intent'),
            'targeting': data.get('targeting'),
            'vulnerability': data.get('vulnerability'),
            'likelihood_initiation': get_likelihood_level(l_init),
            'likelihood_impact': get_likelihood_level(l_impact),
            'overall_likelihood': get_likelihood_level(overall_likelihood),
            'impact_level': get_impact_level(impact),
            'risk_level': get_risk_level(risk_score),
            'risk_score': risk_score,
            'asset_name': data.get('asset_name'),
            'asset_type': data.get('asset_type'),
            'asset_valuation': data.get('asset_valuation'),
            'financial_impact': data.get('financial_impact')
        }
    except (ValueError, TypeError):
        return {
            'risk_level': 'Error',
            'risk_score': 0
        }
