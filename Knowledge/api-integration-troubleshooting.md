# API Integration Troubleshooting Guide

## Purpose

This guide provides a structured approach for investigating failures between enterprise applications and external or internal APIs.

## Common Symptoms

- HTTP 400 Bad Request
- HTTP 401 Unauthorized
- HTTP 403 Forbidden
- HTTP 404 Not Found
- HTTP 429 Too Many Requests
- HTTP 500 Internal Server Error
- HTTP 502 Bad Gateway
- HTTP 503 Service Unavailable
- Connection timeout
- TLS or certificate validation failure

## Investigation Workflow

### Step 1: Identify the Failure Boundary

Determine where the failure occurs:

- Calling application
- Integration layer
- API gateway
- Network
- Authentication provider
- Downstream API

Do not assume the downstream service is the root cause without evidence.

### Step 2: Capture Evidence

Collect:

- Timestamp
- Correlation ID
- Request ID
- HTTP status code
- Error message
- Target endpoint
- Response headers when available

Sensitive information must be removed before sharing logs externally.

### Step 3: Review Recent Changes

Check for:

- Application deployments
- Infrastructure changes
- Credential rotations
- Firewall changes
- API version changes
- Vendor maintenance

### Step 4: Interpret HTTP Status Codes

401 typically indicates authentication failure.

403 indicates that authentication may be valid but authorization is insufficient.

429 indicates rate limiting or throttling.

5xx errors generally indicate server-side or gateway failures, but the exact failing component must be confirmed using logs and monitoring data.

### Step 5: Isolate the Failure

Test the API independently using an approved test client.

Compare:

- A known successful request
- A failing request

Check differences in:

- Authentication headers
- Request body
- API version
- Endpoint
- Network path

## Resolution Principles

- Do not rotate credentials without confirming credential-related evidence.
- Prefer reversible changes.
- Validate fixes in a controlled manner.
- Record the confirmed root cause.
- Monitor after remediation.