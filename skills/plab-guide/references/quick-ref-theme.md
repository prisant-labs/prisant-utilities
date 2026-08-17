# Quick-Reference Theme Reference

How to edit the visual style of the quick-reference HTML and PDF artifacts. All visual configuration lives in a `:root` block at the top of the locked HTML template; this file documents what each variable does and how edits propagate.

## Use when

- You want to change the accent color, fonts, font sizes, spacing, or backgrounds of the quick reference
- You're tuning print-ink usage or contrast
- A future generation should inherit a style change you make now
- A specific bundle's HTML needs a one-off override

## Where the styles live

There is **one source-of-truth file**:

| File | Role |
|------|------|
| `skills/plab-guide/assets/templates/quick-reference-template_v1-technical-white.html` | Canonical locked template, copied into each generated bundle |

The skill copies this template into each new bundle when generating, so edits propagate to **future** generations only. Already-generated bundles keep the styles they were built with; update them by hand or regenerate.

### The `:root` block

All variables live in a single `:root { ... }` block inside the `<style>` tag at the top of every quick-reference HTML. The block is grouped into 9 sections with comment dividers:

1. PAGE SETUP
2. TYPOGRAPHY: FONTS
3. TYPOGRAPHY: SIZES
4. TYPOGRAPHY: LINE HEIGHTS
5. TYPOGRAPHY: WEIGHTS / TRACKING
6. COLORS: PALETTE (most-edited section)
7. COLORS: BORDERS
8. COLORS: BACKGROUNDS (controls fills and ink usage)
9. SPACING + ACCENT RULE WEIGHTS

Every downstream rule uses `var(--name)`, so editing a variable changes every rule that references it.

## Common edits

| To do this | Edit this variable | From | To (example) |
|------------|-------------------|------|--------------|
| Change brand color | `--accent` | `#1f4b87` | `#2d6a4f` (green) |
| Switch body font to Inter | `--font-body` | `"Segoe UI", "Helvetica Neue", Arial, sans-serif` | `"Inter", "Segoe UI", ...` |
| Make body text larger for printability | `--size-body` | `8pt` | `9pt` |
| Restore the v1 `.card.ref` tint | `--bg-card-ref` | `transparent` | `#f0f4f9` |
| Restore the v1 `.card.summary` tint | `--bg-card-summary` | `transparent` | `#e1e8f0` |
| Restore the v1 lede tint | `--bg-lede` | `transparent` | `#f5f7fa` |
| Drop the masthead band fill | `--bg-masthead` | `#f5f7fa` | `transparent` |
| Drop table zebra alternation | `--bg-row-even` | `#e8edf2` | `transparent` |
| Drop step-row zebra | `--bg-step-row-even` | `#e8edf2` | `transparent` |
| Drop code-block tint | `--bg-code-block` | `#e8edf2` | `transparent` |
| Tighten card padding | `--card-padding` | `5px 8px 5px 8px` | `4px 7px 4px 7px` |
| Reduce inter-card gap | `--grid-gap` | `5px` | `4px` |
| Thicker masthead left rule | `--rule-masthead-left` | `4px solid var(--accent)` | `6px solid var(--accent)` |

## Full variable reference

### Page setup

| Variable | What it controls |
|----------|-----------------|
| `--page-margin` | `@page` margin (US Letter assumed). Top-bottom + left-right. |

### Typography: fonts

| Variable | What it controls |
|----------|-----------------|
| `--font-body` | Body font for all prose. Use a system-available stack to avoid PDF font-substitution issues. |
| `--font-mono` | Monospace font for inline `<code>`, `<pre>`, masthead icon, masthead meta, step-row numbering, and `.kbd` chips. |

### Typography: sizes

All sizes are in `pt` for print fidelity. There are 12 named sizes; each element class has its own.

| Variable | Element |
|----------|---------|
| `--size-body` | Default body and lede |
| `--size-masthead-icon` | Big icon glyph in the masthead |
| `--size-masthead-title` | Page title |
| `--size-masthead-sub` | Page subtitle (uppercase tracked) |
| `--size-masthead-meta` | Version / page-count meta in the masthead |
| `--size-card-h2` | Card section header (uppercase tracked) |
| `--size-card-h3` | Card sub-section heading |
| `--size-card-body` | Card paragraph text |
| `--size-card-tag` | Right-aligned tag inside a card's H2 |
| `--size-table` | Table cell text |
| `--size-table-th` | Table header (uppercase tracked) |
| `--size-mono-inline` | Inline `<code>` |
| `--size-mono-block` | `<pre>` code blocks |
| `--size-step-row` | Numbered step rows |
| `--size-aside` | Card footer aside (italic) |
| `--size-kbd` | Keyboard-key chips |

### Typography: line heights

| Variable | Element |
|----------|---------|
| `--lh-body` | Default body |
| `--lh-card-text` | Card paragraphs and list items |
| `--lh-pre` | Code blocks |
| `--lh-aside` | Card footer asides |
| `--lh-lede` | Lede paragraph |
| `--lh-meta` | Masthead meta |
| `--lh-masthead-title` | Masthead title (kept tight) |

### Typography: weights and tracking

| Variable | Default | Use |
|----------|---------|-----|
| `--weight-strong` | `700` | Bolded text in prose |
| `--weight-bold` | `800` | Card H2 |
| `--tracking-uppercase` | `0.16em` | Card H2 letter-spacing |
| `--tracking-sub` | `0.2em` | Masthead sub letter-spacing |
| `--tracking-th` | `0.1em` | Table header letter-spacing |

### Colors: palette

This is the most-edited section. Change four values and the rest of the document follows.

| Variable | Default | Use |
|----------|---------|-----|
| `--accent` | `#1f4b87` | Primary brand color. Used for masthead title rule, card H2 text, lede left rule, code keyword, table header text, all accent indicators. |
| `--text` | `#0e131c` | Main text. |
| `--text-muted` | `#2a3442` | Secondary text (e.g., masthead meta, card tags). |
| `--text-subdued` | `#4a5260` | Tertiary text (e.g., code comments inside `<pre>`). |

### Colors: borders

| Variable | Default | Use |
|----------|---------|-----|
| `--border` | `#c8d1de` | Default card and element border. |
| `--border-strong` | `#a8b3c2` | Keyboard-chip borders. |
| `--border-subtle` | `#d8dee5` | Table cell separators. |

### Colors: backgrounds (controls ink usage)

The most consequential section for print cost and contrast. Defaults are calibrated to minimize ink while preserving functional fills.

| Variable | Default | What it fills |
|----------|---------|---------------|
| `--bg-page` | `#ffffff` | Page background. |
| `--bg-card` | `#ffffff` | Default card background. |
| `--bg-masthead` | `#f5f7fa` | Page header band. Set to `transparent` to drop the fill. |
| `--bg-row-even` | `#e8edf2` | Alternating table rows (zebra). Set to `transparent` to drop. |
| `--bg-step-row-even` | `#e8edf2` | Alternating step-row rows. |
| `--bg-code-inline` | `#e8edf2` | Inline `<code>`. |
| `--bg-code-block` | `#e8edf2` | `<pre>` code blocks. |
| `--bg-kbd` | `#f5f7fa` | Keyboard-key chips. |
| `--bg-lede` | `transparent` | Lede paragraph. v2 default: no fill. Restore with `#f5f7fa`. |
| `--bg-aside` | `transparent` | Card footer aside. v2 default: no fill. |
| `--bg-card-ref` | `transparent` | `.card.ref` (lookup tables). v2 default: no fill. Restore with `#f0f4f9`. |
| `--bg-card-summary` | `transparent` | `.card.summary` (closing banner). v2 default: no fill. Restore with `#e1e8f0`. |

### Spacing

| Variable | Default | Effect |
|----------|---------|--------|
| `--grid-gap` | `5px` | Gap between cards in the 6-column grid. |
| `--card-padding` | `5px 8px 5px 8px` | Inside-card padding. |
| `--masthead-padding` | `7px 10px` | Masthead band padding. |
| `--masthead-margin-bottom` | `8px` | Space below the masthead. |
| `--lede-padding` | `7px 10px` | Lede paragraph padding. |
| `--lede-margin-bottom` | `10px` | Space below the lede. |

### Accent rule weights

These are full `border` shorthand values; edit weight and style here, and the color comes from `--accent`.

| Variable | Default | Use |
|----------|---------|-----|
| `--rule-masthead-left` | `4px solid var(--accent)` | Masthead's left accent. The thickest accent rule on the page. |
| `--rule-lede-left` | `2.5px solid var(--accent)` | Lede's left accent. |
| `--rule-aside-left` | `2px solid var(--accent)` | Aside's left rule. |
| `--rule-pre-left` | `2px solid var(--accent)` | Code-block left rule. |
| `--rule-card-h2-bottom` | `1.5px solid var(--accent)` | Card H2 underline. |
| `--rule-th-bottom` | `1px solid var(--accent)` | Table header underline. |
| `--rule-card-ref-left` | `2.5px solid var(--accent)` | `.card.ref` left highlight. Replaces the old fill. |
| `--rule-card-summary-top` | `2.5px solid var(--accent)` | `.card.summary` top highlight. Replaces the old fill. |

## Functional vs decorative fills

When deciding whether to keep a background fill, use this lens:

**Functional (keep on by default):**
- Table row zebra - improves legibility on long tables
- Step-row zebra - improves legibility on long step lists
- Code-block / inline-code tint - distinguishes code from prose
- KBD chips - signals a keyboard key, not regular text
- Masthead band - structural page header, similar to a chapter title

**Decorative (off by default in v2; flip back on if you want them):**
- `.card.ref` background - a category indicator that already has a left rule
- `.card.summary` background - a closing-banner emphasis that already has a top rule
- `.lede` background - the left rule already marks the lede
- `.aside` background - the left rule already marks the aside

The principle: if removing the fill loses information, it was functional. If removing it just makes the page lighter, it was decorative.

## How to test a change

1. Edit the `:root` block in the source-of-truth template (or a specific bundle's HTML).
2. Re-render the PDF: `scripts/render-pdf.sh path/to/quick-reference.html`.
3. Verify the result is exactly 2 pages (gate G-8). The script prints `pages: N` and exits 3 on overflow.
4. Open the PDF and visually check: contrast against text, accent-color readability, font-substitution issues.

For inheritance verification: re-run the skill against a small fixture (e.g., `glow`) and confirm the new bundle inherits your edit.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|-------------|-------------|-----|
| Editing CSS rules outside the `:root` block | Changes don't propagate; future generations revert | Define a new variable, then use it in the rule |
| Hardcoding a hex color in a rule | Same as above; bypasses the inheritance pattern | Add a variable to `:root`, reference via `var()` |
| Setting `--accent` to a low-contrast color | Card H2 / table headers / accent rules become unreadable | Test against `--text` (`#0e131c`) on `--bg-card` (`#ffffff`) for legibility |
| Increasing `--size-body` past `9pt` | Cards exceed their height budget; PDF overflows to 3 pages | Tighten `--card-padding` or drop a card to compensate |
| Using a non-system body font without a fallback | Chrome substitutes; rendering can look wrong on different machines | Always include 3-4 fallback families in `--font-body` |
| Setting `--page-margin` below `0.25in` | Some printers can't print to the edge; content gets clipped | Stay above `0.25in` for print safety |
| Editing one bundle's HTML and expecting future generations to inherit | Future bundles copy from the template, not from a generated HTML | Edit the template (`assets/templates/quick-reference-template_v1-technical-white.html`) |
| Removing functional fills (`--bg-row-even`, `--bg-code-inline`) | Loses legibility on tables and code | Only remove if you've validated the result |

## Migration: v1 (with fills) → v2 (no fills)

If you're updating an old v1-style HTML to the v2 default, set these variables to `transparent`:

```css
--bg-card-ref: transparent;
--bg-card-summary: transparent;
--bg-lede: transparent;
--bg-aside: transparent;
```

And remove the `<div class="footer">…</div>` from the body markup (the `.footer` CSS rule no longer exists in the v2 stylesheet).

Both source-of-truth templates are already on v2; the migration applies only if you have an older bundle you want to bring up to date.

## Source-of-truth files (where to edit)

For changes that should propagate to future generations, edit:

- `skills/plab-guide/assets/templates/quick-reference-template_v1-technical-white.html`

The skill copies from that file during generation. If you maintain a parallel theme variant (e.g., a "dark" theme), name it explicitly: `quick-reference-template_v1-dark.html`, etc.

## See also

- `references/quick-ref-html-patterns.md` - card catalog and layout patterns (what cards to put on each page; this file is purely about visual style)
- `references/pdf-toolchain.md` - browser detection and rendering troubleshooting
- `scripts/render-pdf.sh` - local headless-Chrome renderer
