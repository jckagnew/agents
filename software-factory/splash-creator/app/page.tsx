"use client";

import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { CreativeBrief, DesignTokens } from "@/lib/schemas";
import type { ProjectSummary, SplashGenerationResult } from "@/lib/services";
import FactoryService from "@/lib/services/factory";
import { DesignTokenPreview } from "@/components/design-token-preview";
import { GuidancePlaceholder } from "@/components/guidance-placeholder";

const toneOptions = [
  { value: "confident", label: "Confident" },
  { value: "premium", label: "Premium" },
  { value: "approachable", label: "Approachable" },
  { value: "playful", label: "Playful" },
  { value: "other", label: "Other (describe below)" }
] as const;

type ToneOption = (typeof toneOptions)[number]["value"];
type StepKey = "project" | "brief" | "guidance" | "review";

type StepDefinition = {
  key: StepKey;
  label: string;
  description: string;
};

const steps: StepDefinition[] = [
  {
    key: "project",
    label: "Select Project",
    description: "Choose a factory project to inherit design language and tokens."
  },
  {
    key: "brief",
    label: "Creative Brief",
    description: "Define tone, headlines, and CTAs to steer the agent."
  },
  {
    key: "guidance",
    label: "Guidance Assets",
    description: "Upload inspiration imagery and notes (coming soon)."
  },
  {
    key: "review",
    label: "Review & Launch",
    description: "Confirm inputs, run the workflow, and monitor progress."
  }
];

interface FormState {
  tone: ToneOption;
  toneOther: string;
  primaryHeadline: string;
  secondaryHeadline: string;
  callToActionPrimary: string;
  callToActionSecondary: string;
  inheritsDesignTokens: boolean;
  keywords: string;
  targetAudience: string;
  goals: string;
}

const initialFormState: FormState = {
  tone: "confident",
  toneOther: "",
  primaryHeadline: "",
  secondaryHeadline: "",
  callToActionPrimary: "",
  callToActionSecondary: "",
  inheritsDesignTokens: true,
  keywords: "",
  targetAudience: "",
  goals: ""
};

export default function SplashCreatorDashboard() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [isLoadingProjects, setIsLoadingProjects] = useState(false);
  const [selectedProjectId, setSelectedProjectId] = useState<string>("");
  const [designTokens, setDesignTokens] = useState<DesignTokens | null>(null);
  const [tokensLoading, setTokensLoading] = useState(false);
  const [formState, setFormState] = useState<FormState>(initialFormState);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [runStatus, setRunStatus] = useState<SplashGenerationResult | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);

  useEffect(() => {
    const loadProjects = async () => {
      setIsLoadingProjects(true);
      try {
        const res = await fetch("/api/projects");
        const data = await res.json();
        setProjects(data.projects ?? []);
      } catch (error) {
        console.error("Failed to load projects", error);
      } finally {
        setIsLoadingProjects(false);
      }
    };

    loadProjects();
  }, []);

  useEffect(() => {
    if (!selectedProjectId) {
      setDesignTokens(null);
      return;
    }

    const loadTokens = async () => {
      setTokensLoading(true);
      try {
        const res = await fetch(`/api/projects/${selectedProjectId}/design`);
        const data = await res.json();
        setDesignTokens(data.designTokens);
      } catch (error) {
        console.error("Failed to load design tokens", error);
        setDesignTokens(null);
      } finally {
        setTokensLoading(false);
      }
    };

    loadTokens();
  }, [selectedProjectId]);

  const selectedProject = useMemo(
    () => projects.find((project) => project.id === selectedProjectId),
    [projects, selectedProjectId]
  );

  const currentStepKey = steps[currentStep].key;
  const isLastStep = currentStep === steps.length - 1;

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const target = event.target as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
    const { name, value, type } = target;
    const checked = "checked" in target ? target.checked : false;

    setFormState((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const canAdvance = (): boolean => {
    switch (currentStepKey) {
      case "project":
        return Boolean(selectedProjectId);
      case "brief":
        return Boolean(formState.primaryHeadline && formState.callToActionPrimary);
      default:
        return true;
    }
  };

  const goNext = () => {
    if (!canAdvance()) {
      return;
    }
    setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
  };

  const goBack = () => {
    setSubmitError(null);
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const launchWorkflow = async () => {
    if (!selectedProject) {
      setSubmitError("Select a project to continue.");
      return;
    }

    if (!formState.primaryHeadline || !formState.callToActionPrimary) {
      setSubmitError("Primary headline and CTA are required.");
      setCurrentStep(1);
      return;
    }

    setSubmitError(null);
    setIsSubmitting(true);

    const keywords = formState.keywords
      ? formState.keywords.split(",").map((word) => word.trim()).filter(Boolean)
      : undefined;
    const goals = formState.goals
      ? formState.goals.split(",").map((goal) => goal.trim()).filter(Boolean)
      : undefined;

    const brief: CreativeBrief = {
      projectId: selectedProject.id,
      projectName: selectedProject.name,
      tone: formState.tone,
      toneOther: formState.tone === "other" ? formState.toneOther : undefined,
      primaryHeadline: formState.primaryHeadline,
      secondaryHeadline: formState.secondaryHeadline || undefined,
      callToActionPrimary: formState.callToActionPrimary,
      callToActionSecondary: formState.callToActionSecondary || undefined,
      targetAudience: formState.targetAudience || undefined,
      goals,
      inheritsDesignTokens: formState.inheritsDesignTokens,
      designTokensOverride: formState.inheritsDesignTokens ? undefined : designTokens ?? undefined,
      guidanceAssets: [],
      keywords,
      references: undefined
    };

    try {
      const res = await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(brief)
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error ?? "Failed to submit brief");
      }

      const payload = (await res.json()) as SplashGenerationResult;
      setRunStatus(payload);
      if (currentStepKey !== "review") {
        setCurrentStep(steps.length - 1);
      }
    } catch (error: any) {
      console.error(error);
      setSubmitError(error.message ?? "Unexpected error");
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStepContent = (): ReactNode => {
    switch (currentStepKey) {
      case "project":
        return (
          <section className="panel form">
            <h2>Select a Project</h2>
            <p className="muted">
              Choose a project to automatically inherit its design tokens, palette, and typography.
            </p>
            <label>
              Project
              <select
                name="project"
                value={selectedProjectId}
                onChange={(event) => setSelectedProjectId(event.target.value)}
                disabled={isLoadingProjects}
              >
                <option value="">Choose…</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </label>
            {selectedProject && (
              <p className="muted">Selected: {selectedProject.name}</p>
            )}
            {!selectedProject && (
              <p className="warning">Select a project to unlock the next step.</p>
            )}
          </section>
        );

      case "brief":
        return (
          <section className="panel form">
            <h2>Creative Brief</h2>
            <p className="muted">
              Define how the splash should feel and the copy it should feature.
            </p>

            <label>
              Tone
              <select name="tone" value={formState.tone} onChange={handleInputChange}>
                {toneOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            {formState.tone === "other" && (
              <label>
                Describe the tone
                <input
                  name="toneOther"
                  value={formState.toneOther}
                  onChange={handleInputChange}
                  placeholder="High-energy enterprise sales acceleration…"
                />
              </label>
            )}

            <label>
              Primary headline <span className="required">*</span>
              <input
                required
                name="primaryHeadline"
                value={formState.primaryHeadline}
                onChange={handleInputChange}
                placeholder="Splendid outreach. Relentless pipeline."
              />
            </label>

            <label>
              Secondary headline
              <input
                name="secondaryHeadline"
                value={formState.secondaryHeadline}
                onChange={handleInputChange}
                placeholder="Optional supporting line"
              />
            </label>

            <label>
              Primary call-to-action <span className="required">*</span>
              <input
                required
                name="callToActionPrimary"
                value={formState.callToActionPrimary}
                onChange={handleInputChange}
                placeholder="Book a demo"
              />
            </label>

            <label>
              Secondary call-to-action
              <input
                name="callToActionSecondary"
                value={formState.callToActionSecondary}
                onChange={handleInputChange}
                placeholder="View playbook"
              />
            </label>

            <label>
              Target audience
              <textarea
                name="targetAudience"
                value={formState.targetAudience}
                onChange={handleInputChange}
                placeholder="e.g. B2B SaaS revenue leaders, SDR managers"
              />
            </label>

            <label>
              Goals (comma separated)
              <input
                name="goals"
                value={formState.goals}
                onChange={handleInputChange}
                placeholder="Drive demos, highlight playbooks, capture emails"
              />
            </label>

            <label>
              Keyword hints (comma separated)
              <input
                name="keywords"
                value={formState.keywords}
                onChange={handleInputChange}
                placeholder="pipeline ritual, collaborative workroom, warm leads"
              />
            </label>

            <label className="inline">
              <input
                type="checkbox"
                name="inheritsDesignTokens"
                checked={formState.inheritsDesignTokens}
                onChange={handleInputChange}
              />
              Inherit design tokens from project (recommended)
            </label>
          </section>
        );

      case "guidance":
        return (
          <section className="panel guidance">
            <h2>Guidance Assets</h2>
            <p className="muted">
              The upcoming uploader will accept inspiration imagery and notes to bias the agent. Until
              then, keep providing tone and keyword hints.
            </p>
            <GuidancePlaceholder />
          </section>
        );

      case "review":
      default:
        return (
          <section className="panel review">
            <h2>Review &amp; Launch</h2>
            <p className="muted">
              Confirm your selections and run the splash workflow. You can return to earlier steps to make
              adjustments at any time.
            </p>

            <dl className="summary">
              <div>
                <dt>Project</dt>
                <dd>{selectedProject?.name ?? "Not selected"}</dd>
              </div>
              <div>
                <dt>Tone</dt>
                <dd>
                  {formState.tone === "other"
                    ? formState.toneOther || "Custom tone"
                    : toneOptions.find((option) => option.value === formState.tone)?.label}
                </dd>
              </div>
              <div>
                <dt>Primary headline</dt>
                <dd>{formState.primaryHeadline || "Not provided"}</dd>
              </div>
              <div>
                <dt>Primary CTA</dt>
                <dd>{formState.callToActionPrimary || "Not provided"}</dd>
              </div>
              <div>
                <dt>Keywords</dt>
                <dd>{formState.keywords || "None"}</dd>
              </div>
              <div>
                <dt>Guidance assets</dt>
                <dd>Uploads coming soon</dd>
              </div>
            </dl>

            {submitError && <p className="error">{submitError}</p>}
            <p className="muted">
              Ready to go? Use the button below to launch the workflow and monitor its progress here.
            </p>

            {runStatus && (
              <div className="status-card">
                <h3>Run submitted</h3>
                <p>Run ID: {runStatus.runId}</p>
                <p>Status: {runStatus.status}</p>
                <p className="muted">
                  Progress polling and approval controls will appear here once the backend orchestration is fully wired up.
                </p>
              </div>
            )}
          </section>
        );
    }
  };

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <h1>Splash Creator</h1>
          <p>Select a project, tailor the experience, and let the agent assemble animated splash screens.</p>
        </div>
      </header>

      <StepIndicator steps={steps} currentStep={currentStep} />

      <section className="grid">
        <div className="left-column">{renderStepContent()}</div>
        <div className="right-column">
          <DesignTokenPreview
            tokens={designTokens}
            projectName={selectedProject?.name}
            isLoading={tokensLoading}
          />
        </div>
      </section>

      <footer className="nav-bar">
        <button type="button" onClick={goBack} disabled={currentStep === 0}>
          Back
        </button>
        {!isLastStep ? (
          <button type="button" onClick={goNext} disabled={!canAdvance()}>
            Next
          </button>
        ) : (
          <button
            type="button"
            onClick={launchWorkflow}
            disabled={isSubmitting || !selectedProjectId || !formState.primaryHeadline || !formState.callToActionPrimary}
          >
            {isSubmitting ? "Submitting…" : "Launch workflow"}
          </button>
        )}
      </footer>

      <style jsx>{`
        .page {
          min-height: 100vh;
          background: radial-gradient(circle at top left, #fdf2f8, #eef2ff);
          padding: 3rem 1.5rem 4rem;
        }

        .page-header {
          max-width: 960px;
          margin: 0 auto 2rem;
          color: #0f172a;
        }

        h1 {
          margin: 0 0 0.5rem;
          font-size: 3rem;
          letter-spacing: -0.03em;
        }

        p {
          margin: 0.35rem 0;
          line-height: 1.6;
        }

        .grid {
          display: grid;
          gap: 2rem;
          max-width: 1100px;
          margin: 0 auto;
          grid-template-columns: 1.2fr 1fr;
        }

        .left-column,
        .right-column {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .panel {
          padding: 1.75rem;
          border-radius: 20px;
          background: #ffffff;
          box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
        }

        .form {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        label {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          font-size: 0.95rem;
          color: #0f172a;
        }

        input,
        select,
        textarea {
          border: 1px solid rgba(15, 23, 42, 0.12);
          border-radius: 10px;
          padding: 0.6rem 0.75rem;
          font-size: 1rem;
          font-family: inherit;
        }

        textarea {
          min-height: 72px;
          resize: vertical;
        }

        .inline {
          flex-direction: row;
          align-items: center;
          gap: 0.6rem;
        }

        .nav-bar {
          display: flex;
          justify-content: center;
          gap: 1rem;
          margin-top: 2rem;
        }

        .nav-bar button {
          padding: 0.8rem 1.8rem;
          border-radius: 999px;
          border: none;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: white;
          font-weight: 600;
          font-size: 1rem;
          cursor: pointer;
        }

        .nav-bar button:disabled {
          cursor: not-allowed;
          opacity: 0.45;
        }

        .muted {
          color: #475569;
        }

        .warning {
          color: #b45309;
          margin: 0;
        }

        .required {
          color: #ef4444;
          margin-left: 0.25rem;
        }

        .status-card {
          margin-top: 1.5rem;
          padding: 1.25rem;
          border-radius: 16px;
          background: #f5f7ff;
          border: 1px solid rgba(99, 102, 241, 0.2);
        }

        .error {
          color: #dc2626;
          font-weight: 600;
        }

        .summary {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin: 1.5rem 0;
        }

        .summary dt {
          font-weight: 600;
          color: #0f172a;
        }

        .summary dd {
          margin: 0.25rem 0 0;
          color: #475569;
        }

        @media (max-width: 1024px) {
          .grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </main>
  );
}

function StepIndicator({ steps, currentStep }: { steps: StepDefinition[]; currentStep: number }) {
  return (
    <ol className="stepper">
      {steps.map((step, index) => {
        const state = index === currentStep ? "current" : index < currentStep ? "completed" : "upcoming";
        return (
          <li key={step.key} className={`stepper-item stepper-item--${state}`}>
            <span className="stepper-index">{index + 1}</span>
            <div className="stepper-copy">
              <span className="stepper-label">{step.label}</span>
              <span className="stepper-description">{step.description}</span>
            </div>
          </li>
        );
      })}

      <style jsx>{`
        .stepper {
          list-style: none;
          padding: 0;
          margin: 0 auto 2.5rem;
          max-width: 1100px;
          display: grid;
          gap: 1rem;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }

        .stepper-item {
          display: flex;
          align-items: flex-start;
          gap: 0.75rem;
          padding: 1rem 1.25rem;
          border-radius: 16px;
          border: 1px solid rgba(15, 23, 42, 0.08);
          background: rgba(255, 255, 255, 0.65);
          box-shadow: 0 12px 20px rgba(15, 23, 42, 0.04);
        }

        .stepper-item--completed {
          border-color: rgba(34, 197, 94, 0.4);
          background: rgba(220, 252, 231, 0.6);
        }

        .stepper-item--current {
          border-color: rgba(99, 102, 241, 0.4);
          background: rgba(224, 231, 255, 0.8);
        }

        .stepper-index {
          width: 2.25rem;
          height: 2.25rem;
          border-radius: 999px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: #ffffff;
        }

        .stepper-item--completed .stepper-index {
          background: linear-gradient(135deg, #22c55e, #4ade80);
        }

        .stepper-label {
          display: block;
          font-weight: 600;
          color: #0f172a;
        }

        .stepper-description {
          display: block;
          color: #475569;
          font-size: 0.85rem;
          margin-top: 0.25rem;
          line-height: 1.5;
        }
      `}</style>
    </ol>
  );
}
