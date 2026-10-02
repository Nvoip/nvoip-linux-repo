# Nvoip App Flatpak

Flatpak manifest for the Nvoip Linux app (`br.com.nvoip.App`), built from
[`Nvoip/nvoip-softphone`](https://github.com/Nvoip/nvoip-softphone) at tag `linux-0.2.8`.

- `br.com.nvoip.App.yml`: main manifest (KDE 6.10 runtime + `io.qt.qtwebengine.BaseApp`).
- `dependencies/qtkeychain.yml`: QtKeychain 0.15.0, stores the refresh token in the system keyring.
- `dependencies/pjproject.yml`: audio-only PJSIP 2.17, same options as `scripts/bootstrap-pjsip-linux.sh` in the softphone repo.

## Local Build

```sh
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.kde.Platform//6.10 org.kde.Sdk//6.10 io.qt.qtwebengine.BaseApp//6.10
flatpak-builder --user --install --force-clean build-dir flatpak/br.com.nvoip.App.yml
flatpak run br.com.nvoip.App
```

`nvoip-softphone` is a private repository, so `flatpak-builder` clones it with the machine's Git credentials.

## New Release

1. Update `tag` and `commit` of the `nvoip-softphone` source in `br.com.nvoip.App.yml`.
2. Make sure the `<release>` in `installer/linux/br.com.nvoip.App.metainfo.xml` matches the `CMakeLists.txt` version (CMake fails otherwise).

## Flathub

Copy `br.com.nvoip.App.yml` and `dependencies/` to the root of a pull request against the `new-pr` branch of
`flathub/flathub`. Before that:

- The source must be public: Flathub builders cannot fetch the private `nvoip-softphone` repository.
- The metainfo must pass the Flathub linter (`<developer>`, screenshots and the other required fields):

```sh
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest flatpak/br.com.nvoip.App.yml
```
