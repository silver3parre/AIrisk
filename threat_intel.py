"""
Threat Intelligence Mapping Module
Maps Asset Types to common Threat Events based on MITRE ATT&CK and other frameworks.
"""

THREAT_INTEL_MAPPING = {
    "Data": [
        {"id": "T1041", "name": "Exfiltration Over C2 Channel", "description": "Adversary stealing data over command and control channel."},
        {"id": "T1486", "name": "Data Encrypted for Impact (Ransomware)", "description": "Encrypting data to interrupt availability."},
        {"id": "T1005", "name": "Data from Local System", "description": "Collecting sensitive data from local files."},
        {"id": "T1565", "name": "Data Manipulation", "description": "Altering data to mislead or cause errors."}
    ],
    "Software": [
        {"id": "T1190", "name": "Exploit Public-Facing Application", "description": "Exploiting a vulnerability in an internet-facing app."},
        {"id": "T1543", "name": "Create or Modify System Process", "description": "Creating a malicious service or daemon."},
        {"id": "T1059", "name": "Command and Scripting Interpreter", "description": "Abusing command shells (PowerShell, Bash) to execute code."},
        {"id": "T1574", "name": "Hijack Execution Flow", "description": "Intercepting function calls or loading malicious DLLs."}
    ],
    "Hardware": [
        {"id": "T1200", "name": "Hardware Additions", "description": "Introducing new hardware (e.g., keyloggers) into the system."},
        {"id": "T1499", "name": "Endpoint Denial of Service", "description": "Exhausting resources to crash the system."},
        {"id": "T1091", "name": "Replication Through Removable Media", "description": "Malware spreading via USB drives."},
        {"id": "T1571", "name": "Non-Standard Port", "description": "Communicating over unexpected ports to evade detection."}
    ],
    "Service": [
        {"id": "T1498", "name": "Network Denial of Service", "description": "Flooding the network to degrade service availability."},
        {"id": "T1557", "name": "Man-in-the-Middle", "description": "Intercepting communications between services."},
        {"id": "T1078", "name": "Valid Accounts", "description": "Compromising user credentials to access the service."},
        {"id": "T1133", "name": "External Remote Services", "description": "Abusing VPNs or RDP to access the network."}
    ]
}

def get_suggested_threats(asset_type):
    """
    Returns a list of suggested threats based on the asset type.
    """
    return THREAT_INTEL_MAPPING.get(asset_type, [])
