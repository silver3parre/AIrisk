# Ain't all Risky Bizz

A guided, qualitative risk assessment tool for modern threats, based on NIST SP 800-30 Rev 1.

## Features

*   **NIST 800-30 Compliant**: Utilizes standard tables and scales for consistent risk evaluation.
*   **Adversarial Focus**: Tailored for assessing risks from active threat actors (hackers, insiders, nation-states).
*   **Zero Trust Alignment**: Automatically applies "Assume Breach" principles, elevating risk scores for insider threats.
*   **Supply Chain Risk Management (SCRM)**: Identifies and tags risks originating from vendors and suppliers.
*   **Business Impact Analysis (BIA)**: Evaluates Reputation, Legal, Operational, and Safety impacts.
*   **Cyber Risk Quantification (CRQ)**: Estimates potential financial loss for better decision-making.
*   **Role-Based Access Control (RBAC)**:
    *   **Viewer**: Read-only access to dashboard and reports.
    *   **Analyst**: Create, scope, and complete assessments.
    *   **Admin**: Full access including assessment deletion.
*   **Tailored Scoping**: Pre-assessment scoping phase to define security categorization and system boundaries.

## Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Application**:
    ```bash
    python app.py
    ```
3.  **Access the App**:
    Open your browser and navigate to `http://localhost:5000`.

## Usage

1.  **Login**: Use one of the predefined roles (e.g., `analyst` / `Analyst`).
2.  **Start Assessment**: Click "Start Assessment" to begin.
3.  **Scope**: Define the assessment title, security categorization, and system description.
4.  **Identify Asset**: Define the primary asset at risk.
5.  **Assess Risks**: Follow the wizard to identify threat sources, events, vulnerabilities, and impacts.
6.  **Review Results**: View the calculated risk score and detailed report.

## License

[MIT License](LICENSE)
