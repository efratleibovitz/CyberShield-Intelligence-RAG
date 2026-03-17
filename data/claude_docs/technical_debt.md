# Technical Debt & Security Audit Log

## Active Warnings
- **WARN-SEC-01 (Severity: HIGH)**: The current **SQL Injection** scanner uses outdated Regex patterns. Risk of bypass is high.
- **WARN-AUTH-04 (Severity: CRITICAL)**: Non-sensitive customer fields are in plain text. Must be addressed immediately.

## Performance Issues
- Optimization of Regex patterns is scheduled for Sprint 4 (April 2026).

## Encryption Requirements
- **Standard**: All PII (Personally Identifiable Information) MUST be upgraded to **AES-256** encryption.
- **Deadline**: 2026-05-01.