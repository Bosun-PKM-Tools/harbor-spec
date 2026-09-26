---
title: Harden UUIDv7 Envelope Validation Gates
task_state: active
priority: p1
recurrence_rule: FREQ=WEEKLY;BYDAY=WE
$pkm:
  id: urn:uuid:01932b10-a002-7c22-9b02-00000000c203
  realm: trice
  created_at: '2026-09-23T18:00:00Z'
  updated_at: '2026-09-23T18:00:00Z'
  relations:
    assignedToContact: urn:yeoman:contact:01932b10-b001-7c11-8a01-00000000c291
    actionItemDerivedFrom: urn:trice:task:01932b10-b002-7c22-9b02-00000000c292
---

# Harden UUIDv7 Envelope Validation Gates

Acid-test Trice task note (Realm 03 / Archetype 4 Stage-Gate Manifest).

## Task Execution
Enforce lowercase RFC 9562 UUIDv7 URN patterns on `$pkm.id` across envelope and archetype schemas.

## Transcluded Requirements
![[trice/projects/schema-hardening#deliverables]]

## Status Tracking
- State: `active`
- Priority: `p1`
- Recurrence: `FREQ=WEEKLY;BYDAY=WE`
^trice-uuidv7-gates
