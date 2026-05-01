#!/usr/bin/env python3
from __future__ import annotations

import gzip
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DEB_DIR = ROOT / "apt/pool/main/n/nvoip-pabx-provisioner"
RPM_DIR = ROOT / "yum/packages/noarch"


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_gzip(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wb", compresslevel=9) as fh:
        fh.write(content.encode("utf-8"))


def latest_package(path: Path, pattern: str) -> Path:
    packages = sorted(path.glob(pattern))
    if not packages:
        raise SystemExit(f"Missing package matching {path / pattern}")
    return packages[-1]


def package_version(deb_path: Path) -> str:
    name = deb_path.name
    return name.split("_", 2)[1]


def build_apt() -> None:
    deb_path = latest_package(DEB_DIR, "nvoip-pabx-provisioner_*_all.deb")
    version = package_version(deb_path)
    size = deb_path.stat().st_size
    rel = deb_path.relative_to(ROOT / "apt").as_posix()
    packages = f"""Package: nvoip-pabx-provisioner
Version: {version}
Architecture: all
Maintainer: Nvoip <dev@nvoip.com.br>
Filename: {rel}
Size: {size}
SHA256: {digest(deb_path, "sha256")}
Section: admin
Priority: optional
Description: Provisionador oficial Nvoip para trunks SIP em PABX Linux
 Configura trunk SIP Nvoip em Asterisk, FreePBX, Issabel, FreeSWITCH e FusionPBX.

"""
    packages_path = ROOT / "apt/dists/stable/main/binary-all/Packages"
    write(packages_path, packages)
    write_gzip(packages_path.with_suffix(".gz"), packages)

    rel_packages = packages_path.relative_to(ROOT / "apt/dists/stable").as_posix()
    rel_packages_gz = packages_path.with_suffix(".gz").relative_to(ROOT / "apt/dists/stable").as_posix()
    release = f"""Origin: Nvoip
Label: Nvoip
Suite: stable
Codename: stable
Version: 1.0
Architectures: all
Components: main
Description: Nvoip Linux Repository
Date: {datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")}
SHA256:
 {digest(packages_path, "sha256")} {packages_path.stat().st_size} {rel_packages}
 {digest(packages_path.with_suffix(".gz"), "sha256")} {packages_path.with_suffix(".gz").stat().st_size} {rel_packages_gz}
"""
    write(ROOT / "apt/dists/stable/Release", release)


def build_yum() -> None:
    rpm_path = latest_package(RPM_DIR, "nvoip-pabx-provisioner-*-1.noarch.rpm")
    version = rpm_path.name.removeprefix("nvoip-pabx-provisioner-").removesuffix("-1.noarch.rpm")
    size = rpm_path.stat().st_size
    rel = rpm_path.relative_to(ROOT / "yum").as_posix()
    primary = f"""<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://linux.duke.edu/metadata/common" packages="1">
  <package type="rpm">
    <name>nvoip-pabx-provisioner</name>
    <arch>noarch</arch>
    <version epoch="0" ver="{version}" rel="1"/>
    <checksum type="sha256" pkgid="YES">{digest(rpm_path, "sha256")}</checksum>
    <summary>Provisionador oficial Nvoip para trunks SIP em PABX Linux</summary>
    <description>Configura trunk SIP Nvoip em Asterisk, FreePBX, Issabel, FreeSWITCH e FusionPBX.</description>
    <packager>Nvoip</packager>
    <url>https://github.com/Nvoip/nvoip-pabx-provisioner</url>
    <time file="{int(rpm_path.stat().st_mtime)}" build="{int(rpm_path.stat().st_mtime)}"/>
    <size package="{size}" installed="{size}" archive="{size}"/>
    <location href="{escape(rel)}"/>
    <format>
      <rpm:license xmlns:rpm="http://linux.duke.edu/metadata/rpm">MIT</rpm:license>
      <rpm:vendor xmlns:rpm="http://linux.duke.edu/metadata/rpm">Nvoip</rpm:vendor>
      <rpm:group xmlns:rpm="http://linux.duke.edu/metadata/rpm">Applications/System</rpm:group>
      <rpm:buildhost xmlns:rpm="http://linux.duke.edu/metadata/rpm">github.com</rpm:buildhost>
      <rpm:sourcerpm xmlns:rpm="http://linux.duke.edu/metadata/rpm">nvoip-pabx-provisioner-{version}-1.src.rpm</rpm:sourcerpm>
      <rpm:header-range xmlns:rpm="http://linux.duke.edu/metadata/rpm" start="0" end="0"/>
    </format>
  </package>
</metadata>
"""
    primary_path = ROOT / "yum/repodata/primary.xml"
    write(primary_path, primary)
    write_gzip(primary_path.with_suffix(".xml.gz"), primary)

    repomd = f"""<?xml version="1.0" encoding="UTF-8"?>
<repomd xmlns="http://linux.duke.edu/metadata/repo">
  <revision>{int(datetime.now(timezone.utc).timestamp())}</revision>
  <data type="primary">
    <checksum type="sha256">{digest(primary_path.with_suffix(".xml.gz"), "sha256")}</checksum>
    <open-checksum type="sha256">{digest(primary_path, "sha256")}</open-checksum>
    <location href="repodata/primary.xml.gz"/>
    <timestamp>{int(datetime.now(timezone.utc).timestamp())}</timestamp>
    <size>{primary_path.with_suffix(".xml.gz").stat().st_size}</size>
    <open-size>{primary_path.stat().st_size}</open-size>
  </data>
</repomd>
"""
    write(ROOT / "yum/repodata/repomd.xml", repomd)


def main() -> int:
    build_apt()
    build_yum()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
