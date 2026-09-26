---
title: "Overnight HRV and Nocturnal Recovery Session"
date: 2026-09-25
$pkm:
  id: "urn:uuid:01923000-0013-7000-8000-000000000001"
  realm: "pratique"
  archetype: "dual_track_telemetry"
  type: "pratique:BiometricStream"
  created_at: "2026-09-25T00:00:00Z"
  updated_at: "2026-09-25T00:00:00Z"
  relations: []
$pratique:
  telemetry_sink: "data/telemetry/2026-09-25-hrv-sleep.parquet"
  observation_type: "vital_signs"
  fhir_resource_type: "Observation"
  sampling_rate_hz: 1.0
  summary_metrics:
    mean_resting_hr: 52.4
    hrv_rmssd_ms: 68.2
    blood_pressure_systolic: 118
    blood_pressure_diastolic: 76
---

# Overnight HRV and Nocturnal Recovery Session

Human context log accompanying the high-density PPG raw stream stored in local columnar Parquet format.
