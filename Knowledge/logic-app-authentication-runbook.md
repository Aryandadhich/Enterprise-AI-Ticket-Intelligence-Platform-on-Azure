# Logic App Authentication Failure Runbook

## Purpose

This runbook provides investigation and remediation steps for Azure Logic App workflows that fail when authenticating to downstream APIs or services.

## Scope

Use this runbook when a Logic App action fails with one of the following errors:

- HTTP 401 Unauthorized
- HTTP 403 Forbidden
- Invalid authentication token
- Expired access token
- Invalid API key
- OAuth authentication failure

## Initial Triage

Collect the following information before making changes:

- Logic App name
- Azure subscription and resource group
- Workflow name
- Failing action or connector
- Timestamp of the first failure
- Downstream API or service name
- HTTP status code
- Correlation ID, if available
- Recent deployment or configuration changes

## Investigation Procedure

### 1. Verify Workflow Run History

Review the Logic App run history and identify:

- The first failed execution
- The exact action that failed
- The HTTP response code
- The response body
- Whether failures are consistent or intermittent

If the workflow was previously successful and failures started suddenly, compare the last successful run with the first failed run.

### 2. Identify the Authentication Method

Determine which authentication mechanism is used:

- API key
- OAuth 2.0
- Managed Identity
- Basic authentication
- Client certificate
- Service principal

The investigation path depends on the authentication method.

### 3. Check Credential Validity

For API keys, tokens, secrets, or certificates:

- Verify expiration dates.
- Confirm the credential has not been revoked.
- Confirm the configured value matches the current value issued by the provider.
- Verify the credential is being retrieved from the expected Key Vault secret.
- Check whether a recent credential rotation occurred.

Do not expose secret values in logs, tickets, or investigation notes.

### 4. Check Azure Key Vault

If credentials are stored in Azure Key Vault:

- Verify the referenced secret exists.
- Verify the secret version is valid.
- Check the expiration date.
- Review recent secret rotations.
- Confirm the calling identity has permission to retrieve the secret.

### 5. Verify Identity and Permissions

For Managed Identity or service principal authentication:

- Verify the identity exists and is enabled.
- Confirm required Azure RBAC roles are assigned.
- Check whether permissions were recently removed or changed.
- Review Microsoft Entra ID sign-in logs where applicable.

### 6. Check the Downstream API

Confirm with the API owner:

- The API endpoint is operational.
- Authentication requirements have not changed.
- The client/application account is active.
- The required permissions or scopes remain assigned.
- There are no provider-side IP restrictions or security changes.

## Common Root Causes

Typical causes include:

1. Expired API key or access token.
2. Revoked or rotated credentials.
3. Incorrect Key Vault secret reference.
4. Missing API permissions or OAuth scopes.
5. Disabled service principal.
6. Expired client certificate.
7. Vendor-side authentication policy changes.

## Recommended Remediation

Apply the remediation that matches verified evidence:

- Update expired credentials using the approved credential rotation process.
- Restore missing permissions.
- Update the Logic App configuration with the approved credential reference.
- Correct an invalid Key Vault reference.
- Renew certificates before expiration.
- Coordinate with the downstream API owner when authentication requirements have changed.

## Validation

After remediation:

1. Execute a controlled Logic App test.
2. Confirm the previously failing action returns a successful response.
3. Monitor subsequent production workflow runs.
4. Confirm affected business processes recover.
5. Document the confirmed root cause and remediation.

## Escalation

Escalate when:

- Authentication configuration appears correct but failures continue.
- The downstream vendor reports no issue.
- Required credential changes need privileged approval.
- The incident affects a business-critical workflow.