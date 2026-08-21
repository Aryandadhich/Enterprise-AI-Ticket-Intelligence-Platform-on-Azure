# Database Connection Failure Runbook

## Purpose

This runbook provides investigation steps for application failures caused by database connectivity problems.

## Common Symptoms

- Connection timeout
- Login failure
- Authentication failure
- Connection refused
- Connection pool exhaustion
- Database unavailable
- TLS or certificate errors

## Initial Information Required

Collect:

- Application name
- Database server name
- Database name
- Environment
- First failure timestamp
- Error message
- Number of affected users
- Recent application or infrastructure changes

## Investigation Procedure

### 1. Confirm Database Availability

Check:

- Database service health
- Availability status
- CPU and memory utilization
- Active connections
- Storage capacity
- Platform service health notifications

### 2. Check Application Connectivity

Verify:

- Connection string configuration.
- Database hostname.
- Port number.
- Network routing.
- DNS resolution.
- Firewall rules.

Do not expose database passwords or connection strings in tickets.

### 3. Investigate Authentication

Check:

- Database user status.
- Password or secret expiration.
- Managed Identity permissions.
- Recent credential rotations.

### 4. Review Connection Pooling

Check for:

- Connection pool exhaustion.
- Long-running queries.
- Connections not being released.
- Sudden traffic increases.

### 5. Review Recent Changes

Investigate:

- Application deployments.
- Database configuration changes.
- Network changes.
- Firewall changes.
- Credential rotation.

## Common Root Causes

- Expired credentials.
- Firewall or network restrictions.
- Database outage.
- Connection pool exhaustion.
- Incorrect connection configuration.
- DNS resolution failure.
- Resource capacity exhaustion.

## Recommended Remediation

Only perform remediation after confirming the cause.

Possible actions:

- Restore approved network access.
- Correct connection configuration.
- Rotate expired credentials.
- Resolve connection leaks.
- Scale database resources.
- Fail over according to the approved recovery procedure.

## Validation

Confirm:

1. Application connections succeed.
2. Error rates return to normal.
3. Business transactions complete successfully.
4. No abnormal connection growth occurs.

## Escalation

Escalate to the database or platform team when infrastructure-level changes or privileged access are required.