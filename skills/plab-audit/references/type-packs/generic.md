# Type pack: generic

**Detected by:** nothing else matching. This is the fallback.

**What this covers:** any repository whose type the skill does not recognise. The pack is deliberately shallow, because depth without knowledge of the ecosystem produces confident generic advice, which is the failure mode every other part of this skill is built to avoid.

**The honest position of this pack:** it can appraise a repository, describe its history and hygiene, and compare its declared plans against its state. It cannot tell you whether the code is any good, and it does not pretend to. An audit run under this pack says so in its verdict.

## Tools, in order

### 1. Git history and bus factor

```bash
git rev-list --count HEAD
git log --reverse --format='%ad %h' --date=short | head -1
git log -1 --format='%ad %h' --date=short
git shortlog -sn --all
git tag --sort=-v:refname
git branch -a
git status --short
```

From these: how long the repository has been alive, whether it is still alive, how many people have touched it, whether it releases, and whether anything is in flight.

**A single-author repository is a fact, not a finding.** Contributor onboarding is explicitly unweighted in this corpus's calibration. Report the number and move on; do not recommend a bus-factor remedy nobody asked for.

### 2. Structure and size

```bash
git ls-files | wc -l
git ls-files | sed 's|/.*||' | sort | uniq -c | sort -rn
```

Top-level shape and where the mass sits. Look for the gap between where the files are and where the README says the interesting part is.

### 3. Hygiene

- **`LICENSE`.** Present, and does it match what any manifest claims.
- **`.gitignore`.** Present, and does it actually cover what the repository generates. Check for committed build output, `node_modules`, `__pycache__`, `.env`.
- **Secrets.** Look for committed `.env` files, key material, and tokens in configuration. Report the class of exposure and the file, never the value.
- **Line endings.** `git config --get core.autocrlf` and `git ls-files --eol "*.sh"`. A shell script stored with CRLF fails to execute on a Unix machine, and this corpus has hit that exact failure before.
- **Large files.** Anything unexpectedly large that is tracked rather than generated.

### 4. Manifest sanity

Whatever manifests exist: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.csproj`.

- Do declared versions agree with each other and with the latest tag?
- Does the declared entry point exist?
- Are there scripts or tasks declared that reference files that are gone?

### 5. Whatever the repository ships to check itself

Look in `scripts/`, `Makefile`, `justfile`, `.github/workflows/`, and the scripts block of whatever manifest is present.

**Run what you can and record every exit code.** A repository's own checks are the best available statement of what it believes about itself, and in a generic audit they are frequently the only real tool available.

**Read each script's usage before invoking it.** An argument you guessed produces a false finding, and a false finding in a shallow audit is proportionally more damaging because there is less context around it to correct it.

### 6. CI configuration

Read `.github/workflows/*.yml` or the equivalent.

Two questions, and the second matters more:

- What does CI actually run?
- **Does it enumerate its checks or glob them?** A workflow naming each script individually will not pick up a new one, so a check added later runs locally and never in CI. That is a silent coverage gap and it is easy to miss by reading the scripts directory alone.

## Judgment questions

1. **Can a newcomer run this?** Follow the README's setup instructions literally and note where they stop being true.
2. **What is this repository's unit of work?** Releases, waves, milestones, or nothing. Whatever it is, the appraisal's history section should use it rather than imposing releases on a repository that does not do them.
3. **Where does it record decisions?** If nowhere, say so. It is the most common finding in this pack and the one with the best cost-to-value ratio.
4. **Does the README describe what the repository currently is?** README drift is the default state of an active repository, and the useful form of this finding names the specific stale claim rather than the general condition.
5. **What is declared as next, and does the tree agree?** Same question as every other pack, and the one that most often produces the finding the maintainer actually acts on.

## What to say in the verdict

An audit under this pack states its own shallowness, in the verdict, in a sentence. Something to the effect of: the repository type was not recognised, so this audit covers history, structure, hygiene and declared-versus-actual state, and makes no assessment of the code itself.

**That sentence is required.** A reader who does not know the audit was shallow will read its silence about the code as an absence of problems, which is exactly the inference the coverage statement exists to prevent.

## Snapshot rows for this type

The standard snapshot, plus: top-level directory breakdown, presence and kind of licence, presence of `.gitignore`, whether CI exists and what it runs, and what manifests are present.
