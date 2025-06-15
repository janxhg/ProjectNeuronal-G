# Cerebral Cognitive Architecture

**A bio-inspired neural simulator for exploring complex event detection and cognitive processes.**

This repository contains the source code for a proprietary research project aimed at building a novel cognitive architecture inspired by the human brain. The simulator is designed to test hypotheses about how neural circuits can learn to recognize complex, time-dependent patterns and integrate them into higher-order events.

---

## Vision & Roadmap

The long-term vision is to develop a foundational model for Artificial General Intelligence (AGI) that operates on principles observed in neurobiology. This project serves as the initial phase, focusing on fundamental microcircuits for sequence and event detection.

The roadmap is divided into several phases:
1.  **Phase 0: Foundational Circuits (Current)** - Implement and validate core neural detectors for temporal sequences (G1), inverted/contextual sequences (G2), and event integration (G3).
2.  **Phase 1: Sensory & Motor Integration** - Develop modules for processing simulated sensory input and generating motor commands.
3.  **Phase 2: Higher-Order Cognition** - Explore the integration of memory, attention, and basic reasoning modules.

---

## Core Concepts

The current simulation is built around three key neural groups:

*   **G1 (Sequence Detector):** A group of neurons trained to fire in response to specific temporal sequences of stimuli (e.g., `1->2->3`).
*   **G2 (Inverted Sequence Detector):** A neuron that learns to detect a sequence that is the reverse of another, demonstrating contextual understanding (e.g., detecting `B->A` after being presented with `A` and `B`).
*   **G3 (Event Integrator):** A higher-order neuron that learns to fire only when two separate, specific events (represented by the firing of G1 and G2 neurons) occur in a precise temporal relationship. This represents a rudimentary form of event binding and complex feature detection.

---

## Current Status

-   [x] **Simulator Core:** A functional biological neural network simulator is in place.
-   [x] **G1 Training & Testing:** G1 detectors for 6 permutations of 3 stimuli are successfully trained and validated.
-   [x] **G2 Training & Testing:** The G2 detector for inverted sequences (`B->A`) is successfully trained and validated.
-   [ ] **G3 Training & Testing:** In progress.
-   [x] **Logging & Debugging:** Robust logging is implemented for tracing simulation flow and results.

---

## Tech Stack

*   **Language:** Python 3
*   **Core Libraries:**
    *   `numpy` for numerical operations.
    *   `matplotlib` for data visualization and plotting results.

---

## License

Copyright (c) 2025 Joaquín Stürtz. All Rights Reserved.

The content of this repository is private and confidential. Unauthorized copying, distribution, or use of this software, via any medium, is strictly prohibited.
