# NIST 800-30 Risk Assessment Application

A web-based guided risk assessment tool based on NIST Special Publication 800-30 Revision 1. This application guides users through the process of identifying threats, vulnerabilities, and impacts to calculate a semi-quantitative risk score.

## Features

- **Asset-Centric Assessment**: Start with asset identification (name, type, valuation) to contextualize risk.
- **Guided Assessment Wizard**: 11-step process guiding through threat identification, vulnerability analysis, and impact assessment.
- **Business Impact Analysis (BIA)**: Evaluate potential damage across reputation, legal/regulatory, operational, and safety areas.
- **Cyber Risk Quantification (CRQ)**: Estimate financial impact of identified risks.
- **NIST 800-30 Compliance**: Utilizes standard tables and semi-quantitative scales (1-5) for likelihood and impact.
- **Assessment Dashboard**: View, manage, and save completed risk assessments.
- **Visual Risk Calculation**: Automatically calculates overall likelihood and risk level based on user inputs.
- **Clean Interface**: Modern, responsive design for a professional user experience.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Production**: Gunicorn, Docker, GitHub Actions

## Setup and Installation

### Local Development
1.  **Clone the repository**.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize Database**:
    ```bash
    flask db upgrade
    ```
4.  **Run the Application**:
    ```bash
    python app.py
    ```

### Production Deployment (Docker)
1.  **Build the Image**:
    ```bash
    docker build -t risk-app .
    ```
2.  **Run the Container**:
    ```bash
    docker run -d -p 5000:5000 \
      -e SECRET_KEY="your-production-secret-key" \
      -e FLASK_ENV="production" \
      risk-app
    ```
    *Note: The container automatically runs database migrations on startup.*

## Usage

1.  Click **Start Assessment** from the home page.
2.  Follow the 11-step wizard:
    - **Step 1**: Identify Asset (name, type, valuation)
    - **Step 2**: Identify Adversarial Threat Source
    - **Step 3**: Identify Threat Event (with optional suggested threats)
    - **Step 4**: Assess Adversary Capability
    - **Step 5**: Assess Adversary Intent
    - **Step 6**: Assess Adversary Targeting
    - **Step 7**: Determine Likelihood of Initiation
    - **Step 8**: Identify Vulnerability
    - **Step 9**: Determine Likelihood of Adverse Impact
    - **Step 10**: Determine Impact Level + Business Impact Analysis
    - **Step 11**: Review
3.  View the **Risk Assessment Result** page to see the calculated risk level, asset profile, threat analysis, and business impact.
4.  **Save Assessment** to persist results for future reference.
5.  Access the **Dashboard** to view and manage all saved assessments.

## Customization

- **Risk Logic**: Modify `risk_logic.py` to adjust the risk calculation matrices.
- **Styling**: Edit `static/style.css` to change the look and feel.
