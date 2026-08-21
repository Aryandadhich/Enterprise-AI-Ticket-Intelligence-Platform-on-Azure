# Previous Incident: Vendor API Authentication Failure

## Incident ID

INC-2026-00421

## Date

2026-05-18

## Priority

P2 - High

## Summary

A production Azure Logic App integration began failing when calling an external vendor API. The failing action returned HTTP 401 Unauthorized.

The workflow had been operating successfully before the incident. No Logic App code deployment occurred immediately before the failures began.

## Business Impact

Order processing workflows could not complete for approximately 180 business users.

A manual workaround was available but required operations staff to process affected transactions individually.

## Investigation

The investigation confirmed:

- Azure Logic App platform health was normal.
- Network connectivity to the vendor endpoint was successful.
- The vendor API endpoint was reachable.
- The API consistently returned HTTP 401.
- The Logic App authentication configuration used an API key stored in Azure Key Vault.
- The Key Vault secret referenced by the workflow had passed its scheduled rotation date.

The vendor confirmed that the previous API key had been revoked after the rotation deadline.

## Root Cause

The production API key used by the Logic App had expired and was revoked by the vendor.

The credential rotation process updated the new API key in Key Vault, but the Logic App configuration continued referencing an outdated secret version.

## Resolution

1. The integration team retrieved the current approved API credential.
2. The credential was stored as a new Key Vault secret version.
3. The Logic App secret reference was updated.
4. A controlled workflow execution was performed.
5. The API call returned HTTP 200.
6. Production workflows were monitored for 30 minutes.

## Preventive Actions

- Review all API credential expiration dates.
- Alert 30 days before credential expiration.
- Use versionless Key Vault secret references where supported and appropriate.
- Add credential rotation validation to the deployment pipeline.
- Document ownership for third-party API credentials.

## Lessons Learned

The incident was initially suspected to be a Logic App platform failure.

Evidence showed that the failure was authentication-related and caused by an outdated Key Vault secret reference.

Future investigations should compare the last successful workflow run with the first failed run and verify credential rotation history early in the investigation.