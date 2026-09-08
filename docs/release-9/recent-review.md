# Recent review and draft replies (#167–#190)

Prepared from the saved [recent-evidence.json](recent-evidence.json) snapshot, not freshly fetched.
These are local recommendations and **unposted drafts**, not merged PRs, issue closures or a stable-release announcement.
Historical #1–#166 coverage lives in [historical-review.md](historical-review.md).

## Decisions

| Item | Evidence and decision |
| --- | --- |
| #167 / #168, @JustinUrassa | Correct README workflow-link mismatch. Implemented the same small documentation correction locally. |
| #169 / #170, @JustinUrassa | Whitespace regression idea is useful; original single-case test has poor indentation. Incorporate broader well-formatted coverage, not the patch unchanged. |
| #171 | Snapshot records HTTP 404. No claim about content, author, state, or review. |
| #172, @cangareijo | Ordinals already normalize to o/a with supported legacy backends; no global transliteration-table patch needed. Add regression tests for ordinals and Unicode dashes. |
| #173, @Jo2234 | Closed unmerged badge duplicate. Same issue addressed locally; do not resurrect a duplicate implementation. |
| #174, @BlocksecPHD | Useful broader whitespace examples; consolidate into table-driven tests with #170/#188 and preserve credit. |
| #175 / #176, @peter-bloomfield / Jacobo de Vera (@jdevera) | Confirmed missing regex forwarding. Prefer #176's original focused fix, strengthened with real CLI and artifact tests. Implemented locally, not merged remotely. |
| #177, @jdevera | Release request is valid. Local 9.0.0 milestone is now the deliverable, subject to documented matrix/downstream gates; no date promise. |
| #178, @Gares95 | Closed unmerged. Useful per-reference numeric recovery and Unicode cases; revive intent alongside #181, not a blind cherry-pick. |
| #179, @binggao1230 | Closed by author in favor of #182. Skipping second-pass self-referential rules changes intentional legacy behavior and does not establish universal idempotence. Do not adopt. |
| #180, @patchwright | Closed by author acknowledging #176 priority. Retain regression intent and original contributor credit; no duplicate merge. |
| #181, @CodingFeng101 | Per-match numeric recovery is sound. Integrated shared helper plus surrogate and oversized-reference handling, valid-neighbor tests and decoding-order correction. |
| #182, @binggao1230 | Decline as written. Skipping rules in either pass and sanitizing post replacements can discard explicit caller intent. Arbitrary caller replacements do not have a universal idempotence contract. Use explicit pre/post controls while preserving legacy defaults. |
| #183, @rantkiglorelgmx-lab | Accept clear input validation intent, preserve bytes and bytearray before replacements. Do not import unrelated broad ignore rules. |
| #184, @eeshsaxena | Duplicate CLI forwarding implementation; prefer #176 and consolidate tests. |
| #185 / #186, @santhreal | Accept intent: nonpositive smart_truncate limits are unlimited, empty separators hard-cut. Integrated with token-aware truncation and actual emitted-length budgeting. |
| #187, @chuenchen309 | Accept encoded non-Latin parity goal, not another unconditional transliteration pass over already converted text. Decode before the single existing pass; document apostrophe/output changes. |
| #188, @ltsyk | Useful whitespace regression duplicate; consolidate with #169/#170/#174. |
| #189, @mmaxjr | Useful ordinal regression test, not proof of a required new transliteration rule. Consolidated locally. |
| #190, @oyeong011 | Accept case-sensitive iterator correctness intent. Materialize stopwords once and preserve case semantics. Regression covers lists/generators and normalized matching. |

These decisions distinguish useful reports and tests from unsafe compatibility changes. They do not evaluate contributors
based on AI use or speculate about motivation. Local integration is not the same as upstream merge or release.

## Draft replies for maintainer approval

### #168 / #167 — badge correction

> Thank you for spotting the mismatch. The development candidate now points the badge image and link to the same main workflow. I have kept this as a small documentation correction and credited your report. This has not been published yet.

### #170 / #174 / #188 — consolidate whitespace tests

> Thank you for the edge-case coverage. I am consolidating the overlapping proposals into one table-driven regression covering empty input, spaces, tabs, newlines and Unicode whitespace. There is no runtime fix needed for these cases, but the tests are useful. I do not plan to merge all the duplicate patches separately; your contribution will remain credited.

### #172 / #189 — ordinal indicators

> Thank you for the report and regression test. The current normalization pipeline already converts º and ª to o and a with the legacy backends. I have added explicit coverage, along with the dash examples, rather than changing global transliteration rules. If you still see a different result, please share the exact input, package version and installed backend so we can reproduce it.

### #176 — original CLI fix

> Thank you, Jacobo. The missing regex forwarding is confirmed, and your focused fix is the basis of the local correction. I have added real command-line and installed-package checks so this cannot be hidden by a parameter-only test. The fix is included in the development candidate; it is not yet a published release.

### #184 — duplicate CLI fix

> Thank you for investigating this and supplying tests. #176 already addresses the same forwarding bug, so I will use that earlier contribution and consolidate the regression coverage rather than merge duplicate fixes. This does not diminish the useful reproduction you provided.

### #181 — numeric references; credit #178

> Thank you. Handling invalid references individually is the right direction, and I have incorporated that behavior into the local candidate, with credit to the earlier #178 investigation as well. The regression suite also checks valid neighbors, surrogates, oversized values and Unicode mode. Decoding now happens before transliteration so encoded non-Latin letters behave like literal input. These deliberate output changes are documented for migration.

### #182 — respectful rejection of the proposed contract

> Thank you for investigating replacement interactions and supplying the examples. I am not going to merge this approach as written. Replacement rules are explicit caller instructions, and silently skipping them or re-sanitizing their final output would change behavior that existing applications may rely on. Idempotence is useful for ordinary defaults, but it is not a universal guarantee for arbitrary replacements. The development candidate instead keeps the existing two-pass default and adds explicit pre-only and post-only controls. Your examples are retained as regression cases for that documented contract.

### #183 — input handling

> Thank you for improving the input error. I have kept the focused validation, while preserving both bytes and bytearray and decoding them before applying replacements. I am leaving unrelated ignore-file cleanup out of this release change. The local tests exercise supported input types and clear rejection of unsupported values.

### #185 / #186 — truncate boundaries

> Thank you for the focused reproductions. Both cases are covered in the local candidate: nonpositive limits no longer slice away content, and an empty separator uses a hard cut. I have integrated them with multi-character separator handling and added a final-output length invariant, rather than treating the boundaries independently.

### #187 — decoding order rather than a second pass

> Thank you for identifying the encoded non-Latin case. I have addressed it by decoding entities before the existing transliteration pass, rather than transliterating already-converted text again. This keeps the pipeline simpler and avoids altering backend-generated text twice. Literal-versus-encoded cases are covered, and the migration guide calls out changed results such as encoded apostrophes.

### #190 — iterator stopwords

> Thank you for the iterator reproduction. The candidate materializes stopwords once, so case-sensitive iterators behave like lists without changing the established matching policy. I have added explicit case-sensitive and normalized-token regressions.

### #177 — release timing

> Yes, the accumulated fixes warrant a release. A local 9.0.0 candidate now combines the compatibility-preserving fixes, explicit backend selection, modern packaging and migration notes. I will not promise a publication date until the full interpreter matrix and downstream compatibility review are complete. Existing persisted slugs should not be regenerated automatically.

## Historical contribution acknowledgment

The release approach also revives the useful intent of Klaas Hoekema's separator/README work (#47/#48),
Jacobo de Vera's replacement-stage proposal (#119), Nathan Drezner's dependency clarity and compatibility
examples (#163), Patrick Sodré's installed-command testing (#43), and Kurt McKee's modern test/build work
(#159/#160/#164/#165). The historical review has the per-item evidence and limitations. No historical patch
is represented as merged or copied unless that is established by the saved record.
