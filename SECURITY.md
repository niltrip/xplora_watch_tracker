# Security Policy

## Supported Versions

Only the latest released version of this integration is supported with security updates. Please ensure you are running the most recent version available via HACS before reporting a security issue.

## Reporting a Vulnerability

If you discover a security vulnerability in this integration, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Open a [private security advisory](../../security/advisories/new) on this repository, or contact the maintainer directly via GitHub.
3. Include as much detail as possible: steps to reproduce, potential impact, and any suggested fixes.

If the issue is confirmed, a fix will be implimented and a new release will be published as soon as possible.

## Known Security Considerations

- **MD5 password hashing**: The Xplora cloud API requires passwords to be hashed with MD5 client-side before authentication. This is a requirement of Xplora's API and is outside the control of this integration. All communication occurs over HTTPS, and credentials are stored using Home Assistant's encrypted config entry storage.
- **API credentials**: This integration uses a public API key/secret pair shared by all Xplora client applications (not user-specific secrets). These are not sensitive credentials in the traditional sense.
- **User credentials**: Your Xplora email and password are stored only within Home Assistant's local, encrypted configuration storage and are never transmitted anywhere other than directly to Xplora's API over HTTPS.

## Scope

This policy covers the `xplora_watch_tracker` custom integration code only. It does not cover:
- Security of the Xplora cloud API itself
- Security of your Home Assistant installation
- Third-party dependencies (this integration has no external Python dependencies beyond `aiohttp`, which ships with Home Assistant)
