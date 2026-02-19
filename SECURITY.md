# Security Guide

## Overview
This document provides security guidelines for managing secrets and credentials in this project.

## ⚠️ Never Commit Credentials

**NEVER** commit the following to version control:
- API keys
- Passwords
- Access tokens
- Private keys
- Database credentials
- Docker registry credentials
- Kubernetes secrets with actual values

## Handling Secrets in Different Contexts

### 1. GitHub Actions Workflows
All sensitive data should be stored in GitHub Secrets:

```yaml
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**To add a GitHub Secret:**
1. Go to your repository Settings
2. Navigate to Secrets and Variables → Actions
3. Click "New repository secret"
4. Add your secret name and value

### 2. Kubernetes Secrets
Kubernetes secrets should be created using `kubectl` commands, not committed as YAML manifests:

```bash
# Create a Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=cc-ms-k8s-training.common.repositories.cloud.sap \
  --docker-username=<your-username> \
  --docker-password=<your-password>

# Create a generic secret
kubectl create secret generic my-secret \
  --from-literal=api-key=<your-api-key>
```

If you must include secrets in YAML for automation, use:
- External secret management tools (e.g., Sealed Secrets, External Secrets Operator)
- Environment-specific secret injection during CI/CD

### 3. Local Development
For local development, use environment variables:

1. Create a `.env` file (already in `.gitignore`):
```bash
GROQ_API_KEY=your_api_key_here
DATABASE_PASSWORD=your_password_here
```

2. Load environment variables in your application:
```python
import os
api_key = os.environ.get("GROQ_API_KEY")
```

### 4. Docker Compose
For Docker Compose, use environment files:

```yaml
services:
  app:
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
```

## Scanning for Exposed Credentials

### Regular Scans
We recommend running security scans regularly:

```bash
# Using git-secrets (install first)
git secrets --scan

# Using truffleHog
trufflehog git file://. --only-verified

# Using gitleaks
gitleaks detect --source .
```

### Pre-commit Hooks
Consider setting up pre-commit hooks to prevent credential commits:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
# Add gitleaks or similar tools
pre-commit install
```

## What Was Fixed

### Issue: Exposed Docker Registry Credentials
**Location:** `k8s/app.yaml` (line 7)

**Problem:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
data:
  .dockerconfigjson: ewoJImF1dGhzIjogewoJCSJjYy1tcy1rOHMtdHJhaW5pbmcuY29tbW9uLnJlcG9zaXRvcmllcy5jbG91ZC5zYXAiOiB7CgkJCSJhdXRoIjogIlkyeGhkV1JsT2pseFVqVm9ZbWh0TjBSNmR6WkNUbHBqVWtaMiIKCQl9Cgl9LAoJInN0YWNrT3JjaGVzdHJhdG9yIjogInN3YXJtIgp9
```

This base64-encoded secret contained:
- Username: `claude`
- Password: `9qR5hbhm7Dzw6BNZcRFv`

**Solution:**
Removed the hardcoded secret and added instructions to create it securely using kubectl.

## Immediate Actions Required

If credentials were exposed in git history:

1. **Revoke compromised credentials immediately**
   - Change the Docker registry password
   - Rotate any exposed API keys
   - Update all affected secrets in GitHub Secrets

2. **Clean git history (if needed)**
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   # WARNING: This rewrites history
   git filter-repo --path k8s/app.yaml --invert-paths
   ```

3. **Update all environments**
   - Recreate Kubernetes secrets with new credentials
   - Update GitHub repository secrets
   - Notify team members of credential changes

## Best Practices Summary

✅ **DO:**
- Use environment variables for secrets
- Store secrets in GitHub Secrets for CI/CD
- Create Kubernetes secrets via kubectl
- Add `.env` files to `.gitignore`
- Use secret scanning tools
- Review code for credentials before committing
- Rotate credentials regularly

❌ **DON'T:**
- Commit credentials to version control
- Share secrets via email or chat
- Hardcode credentials in source code
- Use weak or default passwords
- Reuse credentials across environments

## Contact

If you discover exposed credentials:
1. Report immediately to the repository maintainers
2. Do not share the credentials publicly
3. Follow the immediate action steps above

## References

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Kubernetes Secrets Best Practices](https://kubernetes.io/docs/concepts/configuration/secret/)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
