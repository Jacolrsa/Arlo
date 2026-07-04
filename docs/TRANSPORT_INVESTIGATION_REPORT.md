# MeshCore Home Assistant Transport Investigation Report

**Project:** MeshCore Home Assistant Integration

**Purpose**

Determine where routing decisions are made for direct messages transmitted from Home Assistant and identify the most appropriate location for any future transport improvements.

---

# Investigation Scope

The investigation traced the complete transmission path from Arlo through the Home Assistant integration into the MeshCore Python SDK.

The objective was to determine:

- Complete send_message call flow
- Parameters passed between layers
- Location of routing decisions
- Route caching behaviour
- Support for direct/flood/path discovery
- Whether stale routes explain observed field behaviour
- Whether any fix belongs in:
  - Arlo
  - Home Assistant Integration
  - MeshCore Python SDK
  - MeshCore Firmware

No source code modifications were performed.

---

# Architecture Overview

Transmission path:

Arlo
    ↓
messages.reply()
    ↓
messenger.send_direct()
    ↓
Home Assistant Service
meshcore.send_message
    ↓
services.py
    ↓
MeshCoreAPI
    ↓
meshcore.commands.send_msg()
    ↓
MeshCore Python SDK
    ↓
Connection Layer
(BLE / TCP / Serial)
    ↓
MeshCore Firmware
    ↓
Mesh Network

---

# Layer Responsibilities

## Layer 1 - Arlo

Responsibilities

- Receive messages
- Execute commands
- Build replies
- Call meshcore.send_message

Routing:
None

Route cache:
None

Network knowledge:
None

Conclusion:
Arlo is transport-independent.

---

## Layer 2 - Home Assistant Integration

Primary service:

meshcore.send_message

Behaviour:

- Resolves destination contact
- Accepts node_id or pubkey_prefix
- Looks up contact
- Calls

meshcore.commands.send_msg(contact, message)

Routing:
None

Route cache:
None

Path selection:
None

Transport logic:
None

Conclusion:

The Home Assistant integration does not decide how packets travel through the mesh.

---

## Layer 3 - MeshCore Python SDK

Primary function:

commands.send_msg()

Behaviour:

Constructs protocol packet containing:

- destination
- timestamp
- retry attempt
- message text

Then transmits the packet.

No routing calculations occur.

No neighbour calculations occur.

No mesh topology calculations occur.

---

# Retry Logic

The SDK provides:

send_msg_with_retry()

Behaviour:

1. Send message
2. Wait for ACK
3. Retry
4. After configurable retries:

reset_path(destination)

5. Retry again

This is significant.

The SDK can request that the firmware discard the existing route.

---

# Path Discovery

The SDK exposes:

send_path_discovery()

and

send_path_discovery_sync()

These invoke the firmware path discovery command.

Path discovery is therefore:

NOT automatic inside the SDK.

The SDK merely requests it.

---

# Contact Database

Each contact contains fields such as:

out_path

out_path_len

out_path_hash_mode

These are maintained by the firmware.

The SDK only reads these values.

It does not compute them.

---

# Event System

The SDK maintains a comprehensive asynchronous event dispatcher.

Events include:

ACK

PATH_UPDATE

ADVERTISEMENT

CONTACT_MSG

CHANNEL_MSG

TRACE

STATUS

DISCOVER

NEIGHBOURS

These events report network state.

They do not make routing decisions.

---

# Connection Layer

BLE

TCP

Serial

All transports perform only:

- framing
- packet transmission
- packet reception

No routing occurs here.

---

# Field Test Analysis

Observed behaviour:

Node A communicates successfully.

Destination node moves.

Replies continue following old route.

Replies fail.

Destination returns to original location.

Replies immediately succeed.

---

This behaviour is consistent with:

A stale stored route inside the firmware.

It is NOT consistent with:

- Home Assistant bug
- Arlo bug
- Python SDK bug

because none of those layers contain routing algorithms.

---

# Investigation Findings

Question:

Where does routing occur?

Answer:

Inside MeshCore firmware.

---

Question:

Does Home Assistant cache routes?

Answer:

No.

---

Question:

Does Arlo cache routes?

Answer:

No.

---

Question:

Does the Python SDK calculate routes?

Answer:

No.

---

Question:

Can the SDK request route reset?

Answer:

Yes.

reset_path()

---

Question:

Can the SDK request path discovery?

Answer:

Yes.

send_path_discovery()

---

Question:

Does the SDK automatically discover routes before every message?

Answer:

No.

---

Question:

Does the SDK automatically flood when no path exists?

Answer:

Only after retry logic requests reset_path().

---

Question:

Can stale routes explain field behaviour?

Answer:

Yes.

The observed behaviour exactly matches a stale route remaining valid inside the firmware until:

- route reset
or
- new path discovery
or
- destination returns to previous route.

---

# Likely Root Cause

Most probable location:

MeshCore firmware routing table.

Reason:

The firmware owns:

- contact paths
- path updates
- forwarding
- routing
- neighbour knowledge

Every upper software layer simply forwards packets.

---

# Investigation Confidence

Arlo:

★★★★★
Very high confidence.

No routing logic exists.

---

Home Assistant Integration:

★★★★★
Very high confidence.

No routing logic exists.

---

MeshCore Python SDK:

★★★★☆
High confidence.

Controls retries and can request route reset.

Does not calculate routes.

---

MeshCore Firmware:

★★★☆☆

Moderate confidence.

Not yet inspected directly.

However all evidence points here.

---

# Recommendations

## Recommendation 1

Do not modify Arlo.

Reason:

Arlo is correctly transport-independent.

---

## Recommendation 2

Do not modify Home Assistant send_message.

Reason:

It correctly delegates transmission.

---

## Recommendation 3

Consider exposing additional SDK transport controls through Home Assistant in the future.

Examples:

- reset_path
- path_discovery
- transport_mode
- flood_mode

These would be enhancements rather than bug fixes.

---

## Recommendation 4

Investigate MeshCore firmware routing implementation.

Specifically:

- route lifetime
- path invalidation
- stale route detection
- automatic path rediscovery
- ACK failure behaviour

This is the most likely location of the underlying issue.

---

# Final Conclusion

The investigation successfully traced the complete message path from Arlo to the MeshCore Python SDK.

No routing decisions are made in:

- Arlo
- Home Assistant Integration
- MeshCore Python SDK transport layer

Routing appears to be owned by the MeshCore firmware.

The observed field behaviour is consistent with stale routing information being retained by the firmware after a node changes location.

Based on the available evidence, any permanent fix is most likely to belong in the MeshCore firmware.

No evidence was found that Arlo or the Home Assistant integration are responsible for the observed routing behaviour.