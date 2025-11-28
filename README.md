# NIST 800-30 Risk Assessment Application

A web-based guided risk assessment tool based on NIST Special Publication 800-30 Revision 1. This application guides users through the process of identifying threats, vulnerabilities, and impacts to calculate a semi-quantitative risk score.

## Features

- **Guided Assessment Wizard**: Step-by-step process to identify threat sources, events, and vulnerabilities.
- **NIST 800-30 Compliance**: Utilizes standard tables and semi-quantitative scales (1-5) for likelihood and impact.
- **Visual Risk Calculation**: Automatically calculates overall likelihood and risk level based on user inputs.
- **Clean Interface**: Modern, responsive design for a professional user experience.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript

## Setup and Installation

1.  **Clone or Download** the repository.
2.  **Install Dependencies**:
    ```bash
    pip install flask flask-sqlalchemy
    ```
3.  **Run the Application**:
    ```bash
    python app.py
    ```
4.  **Access the App**:
    Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

1.  Click **Start Assessment** from the home page.
2.  Follow the 6-step wizard:
    - Identify Threat Source
    - Identify Threat Event
    - Identify Vulnerability
    - Determine Likelihood of Initiation
    - Determine Likelihood of Adverse Impact
    - Determine Impact Level
3.  View the **Risk Assessment Result** page to see the calculated risk level.

## Customization

- **Risk Logic**: Modify `risk_logic.py` to adjust the risk calculation matrices.
- **Styling**: Edit `static/style.css` to change the look and feel.
# AIrisk
# AIrisk
