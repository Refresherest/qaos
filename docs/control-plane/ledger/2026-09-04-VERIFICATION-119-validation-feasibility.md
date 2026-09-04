# VERIFICATION-119 — Isolated Validation Feasibility

2026-09-04; repository baseline ed208e6. Assessment complete; execution readiness
NOT established. No isolation/control probes ran. This is not a security audit.

## Observed local inventory

| Check | Observation |
| --- | --- |
| Win32_OperatingSystem | Windows 11 Pro, 10.0.22631; registry DisplayVersion 23H2, UBR 6199. |
| Win32_ComputerSystem | HypervisorPresent=False; physical RAM 17,126,481,920 bytes. |
| Win32_Processor | 8 logical processors; firmware virtualization, SLAT and VM monitor extensions=True. |
| OS DEP availability | True. Processor DEP property was blank; use OS property evidence. |
| C: volume | NTFS, 255,090,225,152 bytes total; 78,135,406,592 bytes free at check. |
| PATH lookup | wsl.exe found; docker, podman, WindowsSandbox, vmrun, VBoxManage not found. Not proof of absence everywhere. |
| Known install paths | Docker Desktop, RedHat Podman and System32 WindowsSandbox executable paths not present. |
| Selected services | No rows for vmcompute, vmms, com.docker.service, WslService or LxssManager. |
| Optional features via CIM | Hyper-V-All, VirtualMachinePlatform, WSL and Containers-DisposableClientVM each InstallState=2 (disabled). |
| WSL status | wsl --status exit 50, no usable status; list --verbose yielded usage rather than a working distribution listing. No distribution was launched. |

Exact read-only command forms used (only selected properties retained):

```powershell
Get-Command docker,podman,wsl,WindowsSandbox,vmrun,VBoxManage -ErrorAction SilentlyContinue | Select-Object Name,Source
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber
Get-CimInstance Win32_ComputerSystem | Select-Object HypervisorPresent,TotalPhysicalMemory
Get-CimInstance Win32_Processor | Select-Object VirtualizationFirmwareEnabled,SecondLevelAddressTranslationExtensions,NumberOfLogicalProcessors
Get-CimInstance Win32_Processor | Select-Object VMMonitorModeExtensions,DataExecutionPrevention_Available,VirtualizationFirmwareEnabled,SecondLevelAddressTranslationExtensions
Get-CimInstance Win32_OperatingSystem | Select-Object DataExecutionPrevention_Available
Get-CimInstance Win32_Service -Filter "Name='vmcompute' OR Name='vmms' OR Name='com.docker.service' OR Name='WslService' OR Name='LxssManager'" | Select-Object Name,State
Get-CimInstance Win32_OptionalFeature -Filter "Name='Microsoft-Hyper-V-All' OR Name='VirtualMachinePlatform' OR Name='Microsoft-Windows-Subsystem-Linux' OR Name='Containers-DisposableClientVM'" | Select-Object Name,InstallState
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' | Select-Object DisplayVersion,CurrentBuild,UBR
Get-Volume -DriveLetter C | Select-Object FileSystem,SizeRemaining,Size
wsl --status
wsl --list --verbose
```

Test-Path was also applied only to C:/Program Files/Docker/Docker/Docker Desktop.exe,
C:/Program Files/RedHat/Podman/podman.exe and C:/Windows/System32/WindowsSandbox.exe.
No credential configuration, environment values or unrelated user files inspected.

Initial sandboxed CIM queries returned Access denied; approved unsandboxed read-only
queries succeeded. An initial Get-WindowsOptionalFeature call used an unsupported
array parameter; corrected per-feature calls still required administrator elevation.
Unsandboxed execution did not grant an administrator token. CIM feature status
resolved that inventory question without enabling anything. WSL output included
UTF-16 null characters; these were removed for status readability, not treated as
evidence of a running runtime. Native status exit captured separately.

## Documentation versus observed capability

Microsoft lists Windows 11 Pro, SLAT, VM monitor extensions, firmware virtualization,
DEP and sufficient RAM among Hyper-V prerequisites. Observed properties support
a conditional local VM recommendation, not proof that enablement/boot will work.
[Hyper-V requirements](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements)

Microsoft defines Win32_OptionalFeature InstallState 2 as disabled.
[CIM feature states](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-optionalfeature)

Windows 11 Pro 23H2 reached end of support in November 2025. This is a prerequisite
blocker for the proposed untrusted-code host: move to an applicable supported,
patched release before establishing this boundary. Upgrade availability and device
compatibility have not been assessed; no update was initiated.
[Microsoft lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/windows-11-home-and-pro)

Windows Sandbox documents configurable networking, clipboard, mapped folders and
memory. Its defaults include networking and clipboard sharing; default launch is
not the proposed policy. The reviewed .wsb settings do not establish the full
per-job resource/evidence contract below. It is therefore not selected as a drop-in
automated runner merely because its name contains Sandbox.
[Sandbox configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)

## Platform recommendation and unresolved prerequisites

Recommend a dedicated disposable Hyper-V VM route on a supported host, with a
minimal guest/runtime and no candidate-time network adapter or host shares. This
is a design recommendation, NOT an installed/approved runner or proven isolation.
Use a reviewed guest image and reproducible reset; guest choice, image provenance,
licensing, exact controls and artifact transport need a setup-plan decision.
The current trusted Windows/NTFS builder remains separate and unchanged.

Alternatives: Windows Sandbox may suit a manual smoke but lacks an established
full runner contract here; Docker/Podman need installation and policy evaluation
(none ready was found); a separate host could avoid upgrading this workstation,
but no remote environment, account, budget or security evidence was inspected.

Costs: no spend incurred or cloud account contacted. Local compute avoids a new
cloud job by design, not a guarantee of zero cost: guest licensing, downloads,
disk use and maintenance must be resolved. Current RAM/free disk are only a snapshot.
Provisional evaluation envelope: one VM, 2 vCPU, 4 GiB RAM, bounded 16 GiB guest disk;
capacity/cleanup and host headroom must be measured before acceptance. No GPU.
Admin access and likely feature/OS restarts require owner scheduling and consent.

## Proposed contract and existing-domain ownership (not implemented)

Candidate bytes and provenance belong with existing Artifact ownership; hashes
must identify immutable bytes, not artifact title alone. Requirements/independent
acceptance belong to the approved work order/planner contract. Objective/task IDs
remain canonical; validation results belong in existing QueueItem.result evidence,
not a parallel task/status registry. Runtime integration should be a separately
opted-in capability; do not widen python_file/python_project accepted source.
Current Artifact lacks the proposed digest/provenance fields; any schema evolution
requires an explicit later contract decision, not implicit migration here.

Proposed request: protocol version, objective/task correlation, candidate member
manifest with relative names/sizes/SHA-256, independently supplied acceptance bundle
digest, approved runtime-image identity and numeric limit profile. Reject traversal,
duplicates, links, unknown fields and oversized bundles before transfer. No arbitrary
host paths, credentials, shell commands or candidate-selected verifier entrypoint.

Proposed response: candidate/test/image digests, policy version, run correlation,
completion/timeout/policy-error outcome, independent test verdicts, bounded stdout/
stderr with truncation flags, resource-limit evidence and cleanup outcome. Guest
claims alone cannot establish host policy or approval. Exported data is untrusted:
bounded size, strict parsing, no auto-import/execution, no automatic artifact promotion.
The transfer mechanism must not expose a writable host mount to candidate code;
its exact design is a setup-plan stop condition, not an assumed solution.

## Proposed control gates and independently authored tests

All controls below are UNVERIFIED. Numeric targets are proposed, not imposed.

| Control | Acceptance / bounded negative test after separate authorization |
| --- | --- |
| No candidate network | Verify absent guest adapter and attempt a bounded connection to a controlled test endpoint; no public scanning. |
| No credentials | Minimal environment allowlist; synthetic host sentinel is absent from guest. Never use a real secret as a probe. |
| No host files | No repo/home shares, clipboard or guest integration file redirection; synthetic outside-input canary inaccessible. |
| Immutable inputs | Read-only staged candidate/tests; attempted test mutation denied; trusted digest check detects tampering. |
| Confined writes | Candidate writes only disposable guest scratch, proposed 256 MiB quota; bounded excess write terminates/refuses without host changes. |
| CPU/memory | Host-enforced VM caps plus reviewed guest job limits; bounded allocation/CPU fixture, no uncontrolled exhaustion. |
| Process limit | Proposed 32 processes; capped fixture exceeds by one; descendants cannot escape the job. |
| Time/tree termination | Proposed 30-second candidate limit plus boot deadline; one child fixture is terminated with parent and VM disposal. |
| Output bounds | Proposed 1 MiB per stream, enforced during production, not only readback; bounded oversized fixture truncates/terminates. |
| Storage/reset | Fixed maximum guest storage and fresh reset; canary absent on next run; stop on cleanup failure or orphan VM. |
| Evidence/promotion | Changed bundle digest or forged result rejected; test pass does not grant publication permission. |

CPU/process/disk/output limits require mechanisms beyond a VM's existence. If any
required mechanism is missing or cannot be independently tested, fail closed.
Do not substitute direct host execution, broad shared mounts or inherited environment.
Platform documentation is not proof these controls are configured on this machine.

## Staged implementation gate and decision request

1. Owner selects supported local-host preparation or supplies another host for
   read-only assessment. First produce a maintenance/setup plan: backup/rollback,
   OS compatibility/update path, admin access, restart window and resource budget.
   This selection alone is not authorization to upgrade, restart or enable features.
2. Obtain explicit approval for the exact host/guest setup, downloads/licensing,
   limit mechanisms and safe transfer design. Missing details block provisioning.
3. Only then provision under its own work order and run a harmless fixed smoke.
4. After configuration review, separately approve bounded negative fixtures. Record
   observed enforcement and cleanup; unresolved control means NOT READY.
5. Integrate a separately scoped validation capability only after gate acceptance.
   Model generation and publication/revision authority remain later decisions.

Recommended next choice: local supported-host preparation PLAN (no host changes).
Alternative: user-designated separate host for read-only inventory. Stop here for
direction. No remote access, guest setup, model connection or execution authorized.

Scope verification: source interfaces inspected (Artifact, ActionExecutor, QueueItem)
and prior trusted-runner evidence reconciled. No product/tests/active data modified;
no runtime regression claim. JSON/whitespace checks apply to records. Unrelated
dirty skills and untracked config/drafts/tools/test directories preserved.
