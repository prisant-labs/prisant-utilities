# Type pack: tauri

**Detected by:** `src-tauri/` or `tauri.conf.json`.

**What this covers:** a Tauri desktop application. A Rust backend, a web frontend, a capability-scoped bridge between them, and a signed update channel. Each of those four is a distinct attack surface and a distinct source of findings.

**This is a full pack, by maintainer ruling of 2026-09-19.** Both design briefs scoped it as a stub that would declare its tool list without running it. It is not a stub, and the degradation behaviour that a stub would have demonstrated is instead the obligation in every section below: a tool that cannot run is reported with its failure, never padded with generic advice about Rust.

**Grounded against:** the structure of `repo-sync-tool`, read 2026-09-20 for shape rather than audited. A Tauri v2 application: `$schema` of `https://schema.tauri.app/config/2`, a `capabilities/` directory, `app.security.csp`, an `updater` plugin block, and per-environment config variants alongside the base config.

## Tools, in order

### 1. Toolchain availability, first and recorded

```bash
cargo --version
node --version
```

Record both, present or absent, **before running anything else**. Everything in section 2 depends on `cargo`, and an audit that discovers its absence halfway through has already written findings it cannot support.

**If `cargo` is absent, that is not a failed audit.** It is a partial audit with a named gap, and the correct output is: every attempted command recorded with its failure, no Rust-specific finding asserted without tool backing, and an explicit sentence in `appraise.md` stating the Rust surface was not assessed. **Padding with generic Rust advice fails this obligation rather than partially satisfying it.**

### 2. The Rust surface

| Command | What it finds | On failure |
|---|---|---|
| `cargo clippy --all-targets --all-features -- -D warnings` | Lint and correctness | Record exit code and stderr; assert nothing about Rust quality |
| `cargo audit` | Known vulnerabilities in the dependency tree | If `cargo-audit` is not installed, that is the gap, distinct from finding zero vulnerabilities |
| `cargo fmt --check` | Formatting drift | Low value alone; useful as a signal about CI coverage |
| `cargo tree --duplicates` | Duplicated transitive dependencies | Informational unless binary size is a stated concern |

Note whether the repository is a workspace. A `crates/` directory beside `src-tauri/` means the Rust code is split, and `--workspace` belongs on the commands above.

**`cargo audit` reporting nothing and `cargo audit` not being installed are different results.** Never let the coverage statement collapse them.

### 3. The frontend surface

```bash
npm audit --json    # or pnpm audit --json, or yarn npm audit
```

Match the tool to the lockfile: `package-lock.json`, `pnpm-lock.yaml` or `yarn.lock`. Running the wrong one produces either an error or a misleading clean result.

Check that `build.beforeBuildCommand` and `build.frontendDist` in `tauri.conf.json` agree with what the frontend tooling actually produces. A `frontendDist` pointing at a directory the build does not emit produces an application that bundles nothing, and it fails at package time rather than at build time.

### 4. Capabilities, which is where Tauri v2 security lives

Read `src-tauri/capabilities/*.json` in full. This is the permission system: each capability grants a set of commands to a set of windows.

Ask:

- **Is any capability granted to more windows than need it?** A capability scoped to `"windows": ["*"]` is the Tauri equivalent of a wildcard grant.
- **Does any permission carry a scope, and is the scope tight?** Filesystem and shell permissions take path and command scopes. An unscoped `fs` permission grants the whole disk.
- **Are there permissions granted for a feature that no longer exists?** Cross-check against the commands actually registered in the Rust `invoke_handler`.

A capability file is short and a capability finding is high-consequence. Read it rather than sampling it.

### 5. Content Security Policy

`app.security.csp` and `app.security.devCsp` in `tauri.conf.json`.

- **A `null` or absent `csp` disables the protection entirely.** That is a finding, and its severity depends on whether the frontend renders any content the user did not author.
- **`devCsp` being looser than `csp` is normal.** Confirm the loosening is confined to `devCsp`, because a development allowance that leaked into the production key ships.
- Look for `'unsafe-inline'` and `'unsafe-eval'` in the production `csp` and ask what requires them.

### 6. The updater, and its keys

If `plugins.updater` is present:

- **Read `pubkey` and look at it, do not just confirm it exists.** A placeholder, a comment, or a string naming an unfinished effort is a real and common state in a pre-release application, and it means the update channel is not yet trustworthy. Report what the value actually is.
- **Check `endpoints`.** Plain HTTP is a finding. A URL pointing at a host that does not exist yet is a different finding and belongs in the appraisal's declared-versus-actual section rather than as a defect.
- **Per-environment config variants** such as `tauri.updater-prod.conf.json` beside the base config are a deliberate pattern. Read each, and check that the production variant is the one carrying the production values. A prod config carrying dev values is the failure this pattern exists to prevent and also the one it makes easy.

### 7. Bundle and signing

- `bundle.icon`: confirm every declared icon file exists. A missing icon fails packaging late.
- `bundle.targets`: compare against the platforms the repository's CI actually builds.
- Signing identity for macOS, and the Windows certificate configuration. **Absent signing in a pre-release application is expected and worth stating once**, not worth a Critical finding.
- `bundle.windows.webviewInstallMode`: this decides what happens on a machine with no WebView2 runtime, and the default is frequently not what the maintainer assumed.

## Judgment questions

1. **Where is the trust boundary, and is it drawn once?** Every `#[tauri::command]` is a hole in it. Count them, and ask whether the capability file and the command set agree.
2. **What does the Rust side do with input from the frontend?** Path handling and shell invocation are where a desktop application becomes a local privilege problem.
3. **Is the frontend rendering anything it did not author?** If yes, the CSP findings move up in severity and the answer belongs in the verdict.
4. **Does the repository build on the platform it targets?** A Windows-targeted application whose CI builds only on Linux is untested where it ships. Check for shell scripts with CRLF line endings, which is the specific Windows failure this corpus has hit before.
5. **Is the update channel real yet, and does the repository say so?** A placeholder key is fine in a pre-release. A placeholder key with no statement anywhere that it is a placeholder is a finding.

## Snapshot rows for this type

Beyond the standard snapshot: Tauri major version from `$schema`, product name and identifier, whether the Rust side is a workspace and how many crates, count of `#[tauri::command]` handlers, count of capability files, whether `csp` is set, whether an updater is configured and whether its pubkey looks real, bundle targets, and the availability of `cargo` and the frontend package manager.
