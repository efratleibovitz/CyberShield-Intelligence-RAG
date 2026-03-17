# Global Development Instructions

## Communication Protocols
- **RULE-ALERT-01**: Every 'Critical' severity alert MUST trigger an SMS to the Security Manager and log to the blockchain ledger.
- **RULE-AUTH-02**: All authentication tokens must expire within 15 minutes of inactivity.

## UI Design System
- **Critical alerts color**: `#FF0000` (Bright Red).
- **Warning alerts color**: `#FFA500` (Orange).
- **Safe status**: `#00FF00` (Neon Green).

## Development Style
- Use asynchronous functions for all network scanning tasks.
- Mandatory code review for any changes to the firewall configuration scripts.