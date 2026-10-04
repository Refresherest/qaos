# WO-176 — Local Pilot Deployment Bridge

2026-10-04; baseline `8e365d0`; branch `feat/operational-builder-chain`.
Authority: owner approval of DECISION-REQUEST-023 options 1A, 2A and 3A.
Status: COMPLETE — LOCAL ONLY; independently accepted with notes in
VERIFICATION-127. No live deployment authority.

## Objective and architecture

Implement and independently verify an explicitly opt-in, fixed-pin worker pilot
broker entrypoint plus a targeted installer/rollback for the `python-single`
launcher and the locally verified protocol revision required for the pilot's
second fixed runtime. Preserve the last-verified synthetic transport, restricted identity,
sudoers, administrative SSH and canonical QAOS domains. The broker and launcher
are worker infrastructure projections, not Artifact, QueueItem or model authority.

## In scope

- Keep the broker's no-pilot default. Enable only from a root-owned, exact fixed
  local control file, with fixed launcher/image/policy/fixture digests compiled
  into reviewed code. Invalid control-file metadata or bytes fail closed.
- Provide a local, reviewable installation/rollback program with fixed paths,
  source/installed digest and metadata gates, recoverable backups of the exact
  pre-upgrade broker and protocol, atomic replacement, and a timed rollback armed before
  changing the live broker/launcher/enablement. Rollback removes only this
  pilot's exact files and restores the original broker and protocol; it must not
  remove or rewrite the synthetic launcher, transport key, user, authorized
  keys, sudoers, SSH settings or broad Docker/worker state.
- Tests cover disabled/invalid/valid broker opt-in, fixed pins, pilot and
  synthetic compatibility, install refusal and exact targeted rollback using
  local fixtures. Run focused, relevant and full regression tests where
  practical, compilation/static checks and independent review.

## Non-goals and stop condition

No live worker, OCI, network, key, Docker, model, candidate, QueueItem or QAOS
product-domain mutation. Do not transfer or execute code. Do not implement a
real one-shot dispatcher or claim durable attempt ownership; WO-175 identifies
that as a separate CSA/owner decision. No auto-retry, publication, promotion or
model governance transition.

Complete only after implementation, tests, source/architecture inspection,
independent review and exact handoff evidence. Then STOP for attempt-authority
architecture and fresh live-account/worker authorization; do not run installer.

## Handoff

The local bridge is complete under the selected 1A/2A/3A boundary. Its exact
installer and rollback script has not been staged or run on the worker. The
subsequent live gate must independently pin the staged script digest, verify
present account/worker state, and address rollback across a reboot; the armed
15-minute timer alone does not provide reboot persistence. Durable attempt
ownership remains a separate CSA/owner decision before any real dispatch.
