---
name: wsl-proxy-fix
description: Fix WSL git proxy connection errors (Failed to connect to 127.0.0.1 port 7890)
author: ericyangbit
version: 1.0.0
tags: [wsl, git, proxy, networking, troubleshooting]
---

# WSL Git Proxy Fix Skill

## Overview
This skill helps diagnose and fix git proxy connection errors in WSL (Windows Subsystem for Linux) environments. Common error: "Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused".

## Problem Description
When using git in WSL, you may encounter proxy-related connection errors even when no proxy should be active. This happens because:
1. Proxy configurations may be set in git config (global or local)
2. Environment variables may contain proxy settings
3. HTTPS git URLs may fail authentication in WSL
4. Residual proxy settings from Windows may interfere

## Quick Start

### 1. Run the Fix Script
```bash
# Make the script executable
chmod +x tools/wsl-proxy-fix.sh

# Diagnose the problem
./tools/wsl-proxy-fix.sh --diagnose

# Auto-fix all issues
./tools/wsl-proxy-fix.sh --auto

# Clean proxy configurations
./tools/wsl-proxy-fix.sh --clean

# Switch to SSH protocol
./tools/wsl-proxy-fix.sh --ssh

# Test GitHub connection
./tools/wsl-proxy-fix.sh --test
```

### 2. Manual Fix Commands
If you prefer manual fixes:

```bash
# Clear git proxy configurations
git config --global --unset http.proxy
git config --global --unset https.proxy
git config --local --unset http.proxy
git config --local --unset https.proxy

# Clear environment variables
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# Switch from HTTPS to SSH protocol
git remote set-url origin git@github.com:user/repo.git

# Test connection without proxy
git -c http.proxy= -c https.proxy= push
```

## Detailed Fix Procedures

### Scenario 1: "Failed to connect to 127.0.0.1 port 7890"
This error indicates git is trying to use a proxy server at 127.0.0.1:7890, but no proxy is running there.

**Solution:**
```bash
# Clear all proxy configurations
./tools/wsl-proxy-fix.sh --clean

# Or manually:
git config --global --unset http.proxy
git config --global --unset https.proxy
unset http_proxy https_proxy
```

### Scenario 2: "Could not read Username for 'https://github.com'"
This error occurs when using HTTPS URLs without proper authentication.

**Solution:**
```bash
# Switch to SSH protocol
./tools/wsl-proxy-fix.sh --ssh

# Or manually:
git remote set-url origin git@github.com:user/repo.git
```

### Scenario 3: SSH authentication fails
This happens when SSH keys are not properly configured.

**Solution:**
```bash
# Check SSH keys
ls -la ~/.ssh/

# Test SSH connection
ssh -T git@github.com

# Generate new SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"
```

## Diagnosis Commands

Check what's causing the issue:

```bash
# 1. Check git proxy settings
git config --global http.proxy
git config --global https.proxy
git config --local http.proxy
git config --local https.proxy

# 2. Check environment variables
env | grep -i proxy

# 3. Check remote URL
git config --get remote.origin.url

# 4. Test network connectivity
curl -I https://github.com
timeout 10s git ls-remote https://github.com/git/git.git
```

## Common WSL Proxy Issues

### Issue 1: Windows Proxy Settings Interference
Windows proxy settings can sometimes leak into WSL.

**Fix:**
```bash
# Add to ~/.bashrc or ~/.zshrc
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
```

### Issue 2: Git Credential Manager Issues
Git credential manager may not work properly in WSL.

**Fix:**
```bash
# Use SSH instead of HTTPS
git remote set-url origin git@github.com:user/repo.git

# Or configure credential helper
git config --global credential.helper store
```

### Issue 3: DNS Resolution Problems
WSL may have DNS issues resolving github.com.

**Fix:**
```bash
# Check DNS resolution
nslookup github.com

# Try using IP directly (temporary)
git config --global url."https://140.82.121.4/".insteadOf "https://github.com/"
```

## Preventive Measures

Add these to your shell configuration (~/.bashrc or ~/.zshrc):

```bash
# Clear proxy settings on shell startup
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY 2>/dev/null

# Alias for proxy-free git
alias gitnp='git -c http.proxy= -c https.proxy='

# Function to switch git remote to SSH
git-ssh() {
  local remote_url
  remote_url=$(git config --get remote.origin.url 2>/dev/null)
  if [[ -z "$remote_url" ]]; then
    echo "Error: No remote origin configured"
    return 1
  fi
  
  if [[ "$remote_url" == https://github.com/* ]]; then
    local repo_path="${remote_url#https://github.com/}"
    repo_path="${repo_path%.git}"
    local ssh_url="git@github.com:${repo_path}.git"
    git remote set-url origin "$ssh_url"
    echo "Switched to SSH: $ssh_url"
  elif [[ "$remote_url" == https://gitlab.com/* ]]; then
    local repo_path="${remote_url#https://gitlab.com/}"
    repo_path="${repo_path%.git}"
    local ssh_url="git@gitlab.com:${repo_path}.git"
    git remote set-url origin "$ssh_url"
    echo "Switched to SSH: $ssh_url"
  else
    echo "Cannot convert URL: $remote_url"
    echo "Manual command: git remote set-url origin git@host:user/repo.git"
  fi
}
```

## The Fix Script

The `tools/wsl-proxy-fix.sh` script provides a comprehensive solution:

```bash
#!/bin/bash
# WSL Git Proxy Fix Script
# Features:
# 1. Diagnose proxy configurations
# 2. Clean proxy settings
# 3. Switch to SSH protocol
# 4. Test network connectivity
# 5. Auto-fix all issues
```

Available options:
- `--diagnose`: Show all proxy-related configurations
- `--clean`: Remove proxy settings from git and environment
- `--ssh`: Convert HTTPS remote URLs to SSH
- `--test`: Test GitHub connectivity
- `--auto`: Run all fixes automatically

## Integration with Claude Code

To use this skill with Claude Code:

1. **Direct script usage**: Claude can run the fix script for you
2. **Manual commands**: Claude can provide the exact commands needed
3. **Diagnosis**: Claude can help interpret error messages

Example Claude interaction:
```
User: "git push fails with proxy error"
Claude: "Run: ./tools/wsl-proxy-fix.sh --diagnose"
Claude: "Then run: ./tools/wsl-proxy-fix.sh --auto"
```

## References

### Git Proxy Documentation
- [Git Config Documentation](https://git-scm.com/docs/git-config)
- [Git Protocols](https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)

### WSL Networking
- [WSL Networking Overview](https://learn.microsoft.com/en-us/windows/wsl/networking)
- [WSL and Proxy Servers](https://learn.microsoft.com/en-us/windows/wsl/networking#accessing-a-windows-server-from-wsl)

### SSH Configuration
- [GitHub SSH Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [SSH Key Generation](https://www.ssh.com/academy/ssh/keygen)

## Troubleshooting Guide

### If the script doesn't work:

1. **Check script permissions**:
   ```bash
   chmod +x tools/wsl-proxy-fix.sh
   ```

2. **Run with bash explicitly**:
   ```bash
   bash tools/wsl-proxy-fix.sh --diagnose
   ```

3. **Check git version**:
   ```bash
   git --version
   ```

4. **Check WSL version**:
   ```bash
   wsl --version
   ```

### If SSH still doesn't work:

1. **Check SSH agent**:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

2. **Verify GitHub SSH access**:
   ```bash
   ssh -T git@github.com
   ```

3. **Add SSH key to GitHub**:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # Copy and add to GitHub SSH keys
   ```

## Version History

- **v1.0.0** (2026-04-21): Initial release with diagnosis, cleaning, SSH switching, and testing features

## License

This skill is provided as-is under MIT License. Use at your own risk.

## Support

For issues with this skill:
1. Check the troubleshooting guide above
2. Review the script output for clues
3. Consult WSL and git documentation
4. Ask Claude for help with specific error messages