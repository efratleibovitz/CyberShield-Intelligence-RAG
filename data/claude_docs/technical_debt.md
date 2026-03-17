# Technical Debt & Security Audit

## Performance Issues
- The current **SQL Injection** scanner is inefficient. 
- *Action*: Optimize Regex patterns in the next sprint.

## Encryption Gaps
- Customer database is currently using plain text for non-sensitive fields.
- *Requirement*: Upgrade to **AES-256** encryption for all PII (Personally Identifiable Information).