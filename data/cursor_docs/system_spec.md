# Cyber-Shield System Specifications

## Networking & Firewall
- **Environment**: Distributed server architecture across 3 regions.
- **Firewall Rule #1**: Allow Port `443` (HTTPS) only.
- **Firewall Rule #2**: Automatically block Port `80` (HTTP).
- **DEC-NET-09**: Port `22` (SSH) is restricted to Internal VPN IPs only.

## Data Retention
- Logs are stored in an S3 Bucket for exactly 90 days. 
- After 90 days, logs are archived to Glacier for 5 years (Regulatory requirement).