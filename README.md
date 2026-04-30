# Nvoip Linux Repository

Static APT and YUM/DNF repository for Nvoip Linux packages.

## APT, Signed

```sh
curl -fsSL https://nvoip.github.io/nvoip-linux-repo/keys/nvoip-linux-repo.asc | sudo gpg --dearmor -o /usr/share/keyrings/nvoip-linux-repo.gpg
echo "deb [signed-by=/usr/share/keyrings/nvoip-linux-repo.gpg] https://nvoip.github.io/nvoip-linux-repo/apt stable main" | sudo tee /etc/apt/sources.list.d/nvoip.list
sudo apt update
sudo apt install nvoip-pabx-provisioner
```

## APT, Quick Test

```sh
echo "deb [trusted=yes] https://nvoip.github.io/nvoip-linux-repo/apt stable main" | sudo tee /etc/apt/sources.list.d/nvoip.list
sudo apt update
sudo apt install nvoip-pabx-provisioner
```

## YUM/DNF, Signed

```sh
sudo rpm --import https://nvoip.github.io/nvoip-linux-repo/keys/nvoip-linux-repo.asc
sudo tee /etc/yum.repos.d/nvoip.repo >/dev/null <<'EOF'
[nvoip]
name=Nvoip Linux Repository
baseurl=https://nvoip.github.io/nvoip-linux-repo/yum
enabled=1
gpgcheck=0
repo_gpgcheck=1
gpgkey=https://nvoip.github.io/nvoip-linux-repo/keys/nvoip-linux-repo.asc
EOF

sudo dnf install nvoip-pabx-provisioner
```

Use `yum` instead of `dnf` on older RPM-based distributions.

## YUM/DNF, Quick Test

```sh
sudo tee /etc/yum.repos.d/nvoip.repo >/dev/null <<'EOF'
[nvoip]
name=Nvoip Linux Repository
baseurl=https://nvoip.github.io/nvoip-linux-repo/yum
enabled=1
gpgcheck=0
repo_gpgcheck=0
EOF

sudo dnf install nvoip-pabx-provisioner
```

## Repository Layout

- `apt/`: Debian/Ubuntu repository metadata and `.deb` package files.
- `yum/`: RHEL/CentOS/Fedora/Rocky/AlmaLinux repository metadata and `.rpm` package files.

Run `scripts/build-repo.py` after adding or replacing packages.

## Signing

Public key fingerprint:

```text
CD67 B8D5 D698 768D EC52  0513 338B CDDA 2361 D614
```

Signed files:

- `apt/dists/stable/InRelease`
- `apt/dists/stable/Release.gpg`
- `yum/repodata/repomd.xml.asc`
