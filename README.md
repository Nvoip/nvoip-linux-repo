# Nvoip Linux Repository

Static APT and YUM/DNF repository for Nvoip Linux packages.

## APT

```sh
echo "deb [trusted=yes] https://nvoip.github.io/nvoip-linux-repo/apt stable main" | sudo tee /etc/apt/sources.list.d/nvoip.list
sudo apt update
sudo apt install nvoip-pabx-provisioner
```

## YUM/DNF

```sh
sudo tee /etc/yum.repos.d/nvoip.repo >/dev/null <<'EOF'
[nvoip]
name=Nvoip Linux Repository
baseurl=https://nvoip.github.io/nvoip-linux-repo/yum
enabled=1
gpgcheck=0
EOF

sudo dnf install nvoip-pabx-provisioner
```

Use `yum` instead of `dnf` on older RPM-based distributions.

## Repository Layout

- `apt/`: Debian/Ubuntu repository metadata and `.deb` package files.
- `yum/`: RHEL/CentOS/Fedora/Rocky/AlmaLinux repository metadata and `.rpm` package files.

Run `scripts/build-repo.py` after adding or replacing packages.
