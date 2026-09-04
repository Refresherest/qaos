# OWNER-DECISION-027 — Staged Trusted Project

2026-09-04. Authority: Qaasim April, repository owner.
The owner selects WO-130 Option A and approves its full documented contracts,
including the prerequisite publication gate and refusal-based recovery boundary.

The approved template is text_stats_project_v1: exactly stats.py, app.py,
test_stats.py and README.md, with repository-owned contents and existing approved
text-statistics/CLI semantics. One project remains one Task in the existing Plan.
Use a separate versioned python_project identity/directory-only intent, the
restricted single-component directory naming rule in WO-130, separate
empty-default enabled_python_projects and explicit python_project_workspace.
File/template permissions do not grant project permission.

Build and verify in an owned same-filesystem staging directory before one
no-replace publication operation. Existing destinations must never be overwritten
or adopted. Prove the supported OS/filesystem primitive, including empty-target
and competing-publisher refusal, before implementation proceeds. Stop if the
primitive cannot be proven; copy/merge or a completion-marker substitute is not
authorized. Final member-set/digest checks precede recorded completion.

WO-130's cleanup, residual-stage, crash-gap and recovery rules apply in full.
Cleanup is limited to the current owned confined stage; failures are reported.
No automatic abandoned-stage cleanup/adoption. If publication succeeds but state
completion does not, recovery refuses the existing destination even if hashes
match. No implied transaction between filesystem publication and JSON state, or
power-loss/hostile-filesystem/cross-platform guarantee. Explicit recovery with
permission may rebuild in a new stage only when the destination is absent.

Separate bounded work orders must establish the primitive evidence and then
implement/test the approved project contract. Preserve old behavior and verify
faults, corruption, permissions, cleanup, collisions, regression and active data
as specified by WO-130. No arbitrary code, provider/model work, installation,
Git capability, UI, QAOS CLI, external deployment or Content OS expansion.
