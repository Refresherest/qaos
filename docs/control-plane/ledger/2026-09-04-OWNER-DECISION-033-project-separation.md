# OWNER-DECISION-033 — Main and Supporting Project Separation

2026-09-04. Authority: repository owner explicitly directed separation of the
main QAOS project from the supporting QAOS-OmniRoute project, whose purpose is
to supply resources for building QAOS.

QAOS owns product architecture, contracts, governance, source and durable project
records. QAOS-OmniRoute owns its routing deployment/configuration and supporting
infrastructure operations within its own scope; it is not QAOS architectural
authority. Model Registry authority and verified/validated/designated distinctions
remain unchanged. Shared hosting does not merge ownership or grant cross-project
access. Keep credentials, deployments, changes and work orders separately scoped.

QAOS work does not implicitly authorize OmniRoute configuration, daemon restart,
resource resizing or credential changes. Integration uses explicit bounded
contracts. This decision does not create or relocate repositories, transfer VM
ownership, grant worker access or authorize infrastructure changes.
