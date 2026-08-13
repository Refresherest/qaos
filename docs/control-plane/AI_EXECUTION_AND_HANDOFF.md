# AI Execution and Handoff Protocol

## Required loop

`READ -> UNDERSTAND -> VERIFY -> PLAN -> EXECUTE -> TEST -> RECORD -> HAND OFF`

Before editing, an AI must read the authority policy, current state, relevant
ADRs, and the latest baseline. It must distinguish verified facts from
assumptions and preserve unrelated working-tree changes.

## Controlled work

A change needs a work order with scope, authority, acceptance criteria,
verification command, and rollback/recovery notes. Implement only that scope.
If evidence contradicts the work order, stop and create a contradiction record.

After each change, run the applicable checks, record exact commands and
results, update current state, and create a handoff record. Never report a
check as passing without running it in the recorded checkout.

## Handoff minimum

- repository path, commit, branch, and complete working-tree state;
- completed work order IDs and artifact paths;
- commands run, outputs/results, and unrun checks;
- open findings, contradictions, risks, and explicit next action;
- no secrets, access tokens, or copied private conversation content.
