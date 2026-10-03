# Nvoip App Flatpak

Flatpak manifest for the Nvoip Linux app (`br.com.nvoip.App`), built from the public Linux source package
`nvoip-linux-0.2.9-src.tar.gz` published in the
[`linux-0.2.9` release](https://github.com/Nvoip/nvoip-app-releases/releases/tag/linux-0.2.9) of `Nvoip/nvoip-app-releases`.

- `br.com.nvoip.App.yml`: main manifest (KDE 6.10 runtime + `io.qt.qtwebengine.BaseApp`).
- `dependencies/qtkeychain.yml`: QtKeychain 0.15.0, stores the refresh token in the system keyring.
- `dependencies/pjproject.yml`: audio-only PJSIP 2.17.

## Local Build

```sh
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.kde.Platform//6.10 org.kde.Sdk//6.10 io.qt.qtwebengine.BaseApp//6.10
flatpak-builder --user --install --force-clean build-dir flatpak/br.com.nvoip.App.yml
flatpak run br.com.nvoip.App
```

## New Release

When a new `nvoip-linux-<version>-src.tar.gz` is published in a `linux-<version>` release of `Nvoip/nvoip-app-releases`,
update `url` and `sha256` of the `nvoip` module source in `br.com.nvoip.App.yml`. The `sha256` is the value in the
`.sha256` file published next to the package.

## Flathub

Copy `br.com.nvoip.App.yml` and `dependencies/` to the root of a pull request against the `new-pr` branch of
`flathub/flathub`. The metainfo must pass the Flathub linter (screenshots and the other required fields):

```sh
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest flatpak/br.com.nvoip.App.yml
```
