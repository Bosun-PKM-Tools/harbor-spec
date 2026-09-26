---
title: "NMEA2000 Micro-Gateway Hardware Spec"
date: 2026-09-25
$pkm:
  id: "urn:uuid:01923000-0046-7000-8000-000000000001"
  realm: "breadboard"
  archetype: "catalog_dossier"
  type: "breadboard:HardwareSpec"
  created_at: "2026-09-25T00:00:00Z"
  updated_at: "2026-09-25T00:00:00Z"
  relations: []
$breadboard:
  project_name: "Isolated NMEA2000 to USB-C Broker"
  mcu_architecture: "rp2040"
  operating_voltage: 3.3
  schematic_cas: "urn:cas:sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  firmware_cas: "urn:cas:sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
  bus_protocols:
    - "can"
    - "nmea2000"
    - "usb"
---

# NMEA2000 Micro-Gateway Hardware Spec

Optoisolated CAN transceiver schematic, GPIO wiring pinouts, and embedded firmware digest.
