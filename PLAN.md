### **Comprehensive Plan (v6): The Design-First Software Factory**

#### **1. Overall Intent**
The mission of the Design-First Software Factory is to create a sophisticated, auditable, and user-centric workflow that accelerates the journey from idea to production-ready code. By enforcing a "design-approved before code" principle and leveraging AI for key steps, the factory will reduce ambiguity, minimize rework, and ensure the final product aligns perfectly with a validated design.

#### **2. Workflow Service Tiers**
*   **Express Tier:** A fully-automated path where the user provides initial requirements and is notified upon final completion.
*   **Concierge Tier:** A collaborative path with explicit user approval steps for key stages like prompt engineering and design review.

#### **3. Platform & Core Architecture**
*   **Platform Strategy:** The factory itself, and all applications it generates, will be built using the **Expo framework**. This ensures a single React Native codebase can target iOS, Android, and the **Web**, providing a seamless experience on phones, tablets, and desktop browsers. The backend will be managed by **Supabase**.
*   **Core Architecture Blueprint:** All Expo development will adhere to the following principles: a shared `src/` codebase with platform-specific adapters, an optional `/platform-overrides` directory activated by build-time flags, platform-aware design tokens, and CI enforcement.

#### **4. Division of Labor**
*   **Gemini (Orchestrator):** Manages the overall project, delegates tasks, and handles communication.
*   **Codex (Backend Specialist):** Responsible for all backend development (Supabase schema, Edge Functions, service integrations).
*   **Cursor (Frontend/UI Specialist):** Responsible for building the user-facing Expo application.

#### **5. Phased Execution Plan**
*   **Phase 1: Project Foundation & Architecture**
    *   **Task 1.1 (Cursor):** Initialize a new **Expo project** (`design-first-software-factory`) and set up the directory structure according to the **Core Architecture Blueprint**.
    *   **Task 1.2 (Codex):** Set up the Supabase project and design the `schema.sql`.
*   **Phase 2: Intake & Auditable Prompt Engineering**
    *   **Task 2.1 (Cursor):** Build the multi-platform intake UI within the Expo app.
    *   **Task 2.2 (Codex):** Implement the backend logic for intake, LLM processing, and prompt generation.
    *   **Task 2.3 (Cursor):** Build the Expo UI for prompt review and approval.
*   **Phase 3: Visual Design Generation (Stitch → Figma)**
    *   **Task 3.1 (Codex):** Implement the backend Edge Function to orchestrate the Stitch-to-Figma pipeline.
    *   **Task 3.2 (Cursor):** Implement the UI to trigger design generation and display the resulting Figma link.
*   **Phase 4: Design Validation & Code Generation**
    *   **Task 4.1 (Cursor):** Build the UI for the final review and approval of the Figma design.
    *   **Task 4.2 (Codex):** Implement the backend validation script.
    *   **Task 4.3 (Codex):** Implement the logic to generate a starter **Expo application**, including scaffolding for testing (Jest/Detox).
*   **Phase 5: Project Packaging & Handoff**
    *   **Task 5.1 (Codex):** Implement the backend service to bundle the final project. The `README.md` will include a "Post-Handoff Checklist".
    *   **Task 5.2 (Cursor):** Create the final download screen in the Expo app.
