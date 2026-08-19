Harden runtime and artifact isolation as part of correctness

Across successful Harbor tasks, the stable packaging pattern is:

- keep the task under `task/` and declare top-level artifacts;
- use explicit absolute `/app/...` paths in the agent-visible contract;
- pin runtime dependencies;
- keep solution and tests out of the shared image and inspect the built image for leaks;
- run candidate code unprivileged where possible;
- use verifier-owned input/output locations and confirm input immutability;
- run oracle twice at 1.0 and no-op twice at 0.0 with zero exceptions;
- classify Daytona startup, credentials, canceled runs, and `jobs: []` separately from task quality.

These controls are not boilerplate. They prevent a task from passing locally while leaking truth, trusting stale artifacts, or failing before the analytical work begins.

My check list:
1. Read the exact static/QC/AVA/pass result.
2. Reproduce the supported failure or build the smallest direct witness.
3. Make the rule agent-visible if the verifier enforces it.
4. Add the positive and negative/boundary test together.
5. Rerun the narrow check, then Docker and oracle/no-op calibration.
6. Push only the coherent slice and inspect the new hosted rollup.

contract and threat matrix

- Enumerate inputs, outputs, identity, ordering, precision, error behavior, and side effects.
- Map every verifier assertion to agent-visible text or a standard explicitly invoked by that text.
- Add direct positive and negative/equality witnesses for every rule.

Anti-patterns to reject

- Calling local oracle/no-op calibration hosted acceptance.
- Treating a timeout, crash, canceled job, setup failure, or missing binary as proof of difficulty.
- Enforcing a verifier rule that the instruction does not disclose.
- Using only public fixtures or changing only IDs/styles in protected cases.
- Reusing candidate-produced truth or leaving expected outputs in an agent-readable location.
- Testing a threshold without equality and adjacent cases.
- Assuming fixed parity rows, fixed topology layers, fixed category operators, or a fixed output order from public data.
- Accepting one file from a multi-file transaction when another write failed.
- Broadening numerical tolerances without a demonstrated hosted artifact and a guard against collapsed output.
- Adding empty rerun commits or speculative fixes when the actual failure evidence has not been inspected.

QC failures usually indicate one of four problems:

- the verifier enforces a rule that the instruction does not disclose;
- the verifier misses a plausible bypass;
- protected cases do not exercise the claimed professional crux;
- execution/isolation permits stale artifacts, leaked truth, path escape, or candidate influence over expected values.

Treat `qc_eval`, `qc_exec`, and `qc_gate` separately. The exact workflow may vary, so the job artifact is authoritative.

So the Universal repair loop

Use this sequence for any actionable check failure.

1. **Pin the failing SHA.** Confirm the comment, artifact, and run belong to the current `headRefOid`.
2. **Extract one concrete claim.** Rewrite the failure as an observable sentence: “a translated public certificate passes,” “the instruction omits the equality rule,” or “the second output can replace the first without rollback.”
3. **Reproduce it locally.** Materialize the smallest candidate or fixture that demonstrates the claim.
4. **Decide whether the rule is disclosed.** If not, update the agent-visible contract before enforcing it.
5. **Add a witness pair.** Include one valid positive case and one negative, equality, adjacency, or failure-injection case.
6. **Repair the verifier independently.** Compute truth from protected source data or an independent model, not from candidate-owned summaries.
7. **Run the narrow regression.** Confirm the reproducer now fails for the intended reason and the positive case passes.
8. **Run the complete local ladder.** Syntax, TOML, task tests, Docker, semantic mutants, oracle twice, and no-op twice.
9. **Inspect the diff.** Check for hidden requirements, leaked truth, broad permission changes, unpinned dependencies, generated artifacts, and unrelated rewrites.
10. **Publish one coherent commit.** The commit should name the behavior repaired, not merely say “retry checks.”
11. **Verify the new hosted head.** Prior-head success does not transfer to the new SHA.

If the evidence does not support a source change, stop. A neutral rerun should be used only when explicitly authorized and only for a genuine orchestration or fail-closed parser result.
