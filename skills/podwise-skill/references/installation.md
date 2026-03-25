---
name: podwise-installation
description: "Instructions for installing and configuring the Podwise CLI. Load this when the user needs to set up Podwise for the first time or troubleshoot their installation."
---

## Installation

#### Homebrew (macOS)

```bash
brew tap hardhackerlabs/podwise-tap
brew install podwise
```

#### Automatic Script

Run the following command to install the latest version of `podwise`:

```bash
curl -sL https://raw.githubusercontent.com/hardhackerlabs/podwise-cli/main/install.sh | sh
```

#### Manual (Binary)

1. Download the latest binary for your OS and architecture from [GitHub Releases](https://github.com/hardhackerlabs/podwise-cli/releases).
2. Unpack the archive (e.g., `tar -xzf podwise_linux_amd64.tar.gz`).
3. Move the `podwise` binary to a directory in your PATH, for example:
   ```bash
   mv podwise /usr/local/bin/
   ```
4. Make sure it's executable: `chmod +x /usr/local/bin/podwise`.

#### From Source

If you have Go installed, you can build and install the binary directly from the source:

```bash
git clone https://github.com/hardhackerlabs/podwise-cli.git
cd podwise-cli
go build -o podwise .
# Move the binary to a directory in your PATH, e.g.,
mv podwise /usr/local/bin/
```

## Configuration

Authorize the CLI in your browser and let it save the API key automatically:

```bash
# Open the browser authorization flow
podwise auth

# Verify connection
podwise config show
```

If you already have an API key, you can still set it manually:

```bash
podwise config set api_key your-sk-xxxx
```

The configuration is stored at `~/.config/podwise/config.toml`.

## Quick Verification

Run:

```bash
podwise --help
podwise config show
```

If the install is healthy, `podwise --help` should print command usage and `podwise config show` should display the config path and API key status.

## Troubleshooting

- If `podwise --help` fails, ensure the installation path is in your `$PATH`
- If API key is invalid, re-run `podwise config set api-key` with a fresh key from podwise.ai
- For full documentation, visit [docs.podwise.ai](https://docs.podwise.ai)
