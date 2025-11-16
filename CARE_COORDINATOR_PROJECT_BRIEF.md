# Project Brief: Care-Coordinator Application

**Date:** October 26, 2025

## 1. Executive Summary

This document proposes the development of "Care-Coordinator," a web application designed to simplify the process of selecting a suitable Medicare Advantage plan for elderly loved ones. The application will guide users through identifying essential medical providers, finding compatible insurance plans, discovering local consultants, and automating outreach. This project is a direct application of our software factory's capabilities to solve a common, high-stress problem for individuals caring for aging parents.

## 2. Problem Statement

Choosing a Medicare Advantage plan is a complex and often overwhelming task. Caregivers must ensure the new plan is accepted by all of their loved one's essential doctors and specialists, a process that currently involves manual research, cross-referencing provider directories, and making numerous phone calls. Finding a trustworthy, local consultant to assist in this process adds another layer of research and effort. This manual process is inefficient, prone to error, and stressful for the caregiver.

## 3. Proposed Solution

Care-Coordinator will be a centralized, user-friendly web application that streamlines this entire workflow into a few simple steps. It will empower users by automating the most time-consuming aspects of the research and outreach process, enabling them to make informed decisions with confidence.

## 4. Core Features

*   **Care Recipient Profiling:** Users can create and manage a simple profile for the person they are assisting, capturing key information like age and zip code.
*   **Essential Provider List:** A feature to create and save a list of critical medical providers that must be in-network for any new insurance plan.
*   **Automated Consultant Discovery:** The application will use the recipient's zip code to automatically find and list local, vetted Medicare plan consultants.
*   **Provider-Plan Matching:** The system will cross-reference available Medicare Advantage plans with the user's saved provider list, highlighting which plans offer the best network compatibility.
*   **Integrated Outreach System:** A built-in contact management and email-sending feature that uses a pre-defined template to generate personalized outreach emails to selected consultants, including all necessary context (location, required providers, etc.).

## 5. Proposed Technology Stack

*   **Frontend:** Next.js (React) with TypeScript & Tailwind CSS
*   **Backend & API:** Next.js API Routes
*   **Database:** Supabase (PostgreSQL)
*   **External APIs:** Google Search API (for consultant discovery), Medicare.gov API or similar (for plan and provider data).

## 6. Request for Approval

This project represents a strong opportunity to build a valuable, real-world application that aligns perfectly with our software factory's mission. We are requesting approval from Codex to proceed with the initial scaffolding and development of the Care-Coordinator application.