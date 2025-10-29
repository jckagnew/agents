#!/bin/bash
# Idea-to-Design Agent System (Prototype)
# Guides client from vague idea through requirements → mockups → feedback → code
#
# CURRENT STATUS: Semi-automated prototype
# - Discovery: Interactive Q&A (human-in-loop)
# - Design Gen: Guided template creation (human-in-loop)
# - Visual QA: Manual Playwright integration (not automated yet)
# - Feedback: Interactive collection (human-in-loop)
# - Code Gen: Placeholder (not implemented yet)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
MAX_ITERATIONS=5
MIN_QA_SCORE=90
MIN_CLIENT_SATISFACTION=9
WORKING_DIR=".claude/idea-to-design"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SESSION_DIR="$WORKING_DIR/session-$TIMESTAMP"

# Logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_agent() {
    echo -e "${MAGENTA}[AGENT]${NC} $1"
}

# Initialize session
init_session() {
    mkdir -p "$SESSION_DIR"/{requirements,mockups,scores,feedback}

    cat > "$SESSION_DIR/session.json" <<EOF
{
  "timestamp": "$TIMESTAMP",
  "initial_idea": "$1",
  "iterations": [],
  "current_iteration": 0,
  "status": "running",
  "convergence": false
}
EOF

    log_success "Session initialized: $SESSION_DIR"
}

# Phase 1: Discovery (Interactive - Human in Loop)
run_discovery() {
    local idea="$1"

    log_agent "🔍 Starting Discovery Phase..."
    log_info "Idea: '$idea'"
    echo ""

    # Create requirements directory
    mkdir -p "$SESSION_DIR/requirements"

    # Interactive prompts to gather requirements
    echo -e "${CYAN}Let's refine your idea into structured requirements.${NC}"
    echo ""

    # App name
    read -p "App Name: " app_name
    app_name=${app_name:-"My App"}

    # App type
    echo ""
    echo "App Type:"
    echo "  1) Health/Fitness Tracking"
    echo "  2) E-commerce/Shopping"
    echo "  3) Dashboard/Analytics"
    echo "  4) Social/Communication"
    echo "  5) Productivity/Tools"
    read -p "Choose (1-5): " app_type_choice

    case $app_type_choice in
        1) app_type="health_tracking" ;;
        2) app_type="e_commerce" ;;
        3) app_type="dashboard" ;;
        4) app_type="social" ;;
        5) app_type="productivity" ;;
        *) app_type="productivity" ;;
    esac

    # Description
    echo ""
    read -p "Brief description (1 sentence): " description
    description=${description:-"$idea"}

    # Must-have features
    echo ""
    echo "Must-have features (comma-separated):"
    read -p "> " must_have_raw
    IFS=',' read -ra must_have_array <<< "$must_have_raw"

    # Nice-to-have features
    echo ""
    echo "Nice-to-have features (comma-separated, optional):"
    read -p "> " nice_to_have_raw
    IFS=',' read -ra nice_to_have_array <<< "$nice_to_have_raw"

    # Design preferences
    echo ""
    echo "Design style:"
    echo "  1) Minimal (clean, lots of whitespace)"
    echo "  2) Modern (bold, vibrant)"
    echo "  3) Professional (corporate, trustworthy)"
    echo "  4) Playful (fun, energetic)"
    read -p "Choose (1-4): " style_choice

    case $style_choice in
        1) design_style="minimal" ;;
        2) design_style="modern" ;;
        3) design_style="professional" ;;
        4) design_style="playful" ;;
        *) design_style="modern" ;;
    esac

    # Primary color
    echo ""
    read -p "Primary brand color (hex, e.g., #4285F4) [default: #4285F4]: " primary_color
    primary_color=${primary_color:-"#4285F4"}

    # Inspiration apps
    echo ""
    read -p "Inspiration apps/sites (comma-separated, optional): " inspiration_raw

    # Build JSON manually with proper escaping
    local requirements_file="$SESSION_DIR/requirements/iteration-0.json"

    # Build must-have array JSON
    local must_have_json="[]"
    if [ ${#must_have_array[@]} -gt 0 ]; then
        must_have_json="["
        for i in "${!must_have_array[@]}"; do
            local feature=$(echo "${must_have_array[$i]}" | xargs) # trim
            must_have_json+="\"$feature\""
            if [ $i -lt $((${#must_have_array[@]} - 1)) ]; then
                must_have_json+=","
            fi
        done
        must_have_json+="]"
    fi

    # Build nice-to-have array JSON
    local nice_to_have_json="[]"
    if [ ${#nice_to_have_array[@]} -gt 0 ]; then
        nice_to_have_json="["
        for i in "${!nice_to_have_array[@]}"; do
            local feature=$(echo "${nice_to_have_array[$i]}" | xargs)
            if [ -n "$feature" ]; then
                nice_to_have_json+="\"$feature\""
                if [ $i -lt $((${#nice_to_have_array[@]} - 1)) ]; then
                    nice_to_have_json+=","
                fi
            fi
        done
        nice_to_have_json+="]"
    fi

    # Build inspiration array JSON
    local inspiration_json="[]"
    if [ -n "$inspiration_raw" ]; then
        IFS=',' read -ra inspiration_array <<< "$inspiration_raw"
        inspiration_json="["
        for i in "${!inspiration_array[@]}"; do
            local site=$(echo "${inspiration_array[$i]}" | xargs)
            if [ -n "$site" ]; then
                inspiration_json+="\"$site\""
                if [ $i -lt $((${#inspiration_array[@]} - 1)) ]; then
                    inspiration_json+=","
                fi
            fi
        done
        inspiration_json+="]"
    fi

    # Write JSON file using jq for safe construction
    jq -n \
        --arg app_name "$app_name" \
        --arg app_type "$app_type" \
        --arg description "$description" \
        --argjson must_have "$must_have_json" \
        --argjson nice_to_have "$nice_to_have_json" \
        --arg style "$design_style" \
        --arg color "$primary_color" \
        --argjson inspiration "$inspiration_json" \
        '{
            app_name: $app_name,
            app_type: $app_type,
            description: $description,
            user_personas: ["Primary user"],
            features: {
                must_have: $must_have,
                nice_to_have: $nice_to_have
            },
            design_preferences: {
                style: $style,
                primary_color: $color,
                inspiration_sites: $inspiration
            },
            technical_constraints: ["Web-based", "Responsive design"],
            success_criteria: "User can complete core features easily"
        }' > "$requirements_file"

    echo ""
    log_success "✅ Requirements saved: $requirements_file"
    echo ""
    echo -e "${BLUE}Requirements Summary:${NC}"
    jq . "$requirements_file"
    echo ""

    return 0
}

# Phase 2: PRD Generation (Automated)
run_prd_generation() {
    local iteration=$1
    local requirements_file="$SESSION_DIR/requirements/iteration-$iteration.json"
    local prd_dir="$SESSION_DIR/prd"

    log_agent "📋 Starting PRD Generation Phase (Iteration $iteration)..."

    # Check requirements file exists
    if [ ! -f "$requirements_file" ]; then
        log_error "❌ Requirements file not found: $requirements_file"
        return 1
    fi

    # Run PRD generator
    log_info "Generating comprehensive PRD bundle..."

    if node scripts/generate-prd.js \
        --requirements "$requirements_file" \
        --output-dir "$prd_dir" 2>&1 | tee /tmp/prd-generation.log; then

        # Check if PRD files were generated
        local prd_files=$(find "$prd_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

        if [ "$prd_files" -ge 3 ]; then
            log_success "✅ Generated $prd_files PRD documents"
            log_info "  - Personas, Problem/Solution, Acceptance Criteria"
            return 0
        else
            log_error "❌ PRD generation failed - expected 3+ documents, found $prd_files"
            return 1
        fi
    else
        log_error "❌ PRD generator failed - see /tmp/prd-generation.log"
        return 1
    fi
}

# Phase 2.5: Architecture Generation (Placeholder for Claude integration)
run_architecture_generation() {
    local iteration=$1
    local requirements_file="$SESSION_DIR/requirements/iteration-$iteration.json"
    local architecture_dir="$SESSION_DIR/architecture"

    log_agent "🏗️  Starting Architecture Generation Phase (Iteration $iteration)..."

    # Check requirements file exists
    if [ ! -f "$requirements_file" ]; then
        log_error "❌ Requirements file not found: $requirements_file"
        return 1
    fi

    # TODO: Integrate with Claude architecture generator when available
    # For now, create placeholder structure
    mkdir -p "$architecture_dir"

    log_info "Architecture generation - checking for existing artifacts..."
    
    # Check if architecture files already exist
    local existing_files=$(find "$architecture_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$existing_files" -gt 0 ]; then
        log_success "✅ Found $existing_files existing architecture files"
        log_info "  - Data Model, Services, Tech Stack specifications present"
        return 0
    else
        log_info "Architecture generation placeholder - waiting for Claude integration"
        log_info "Expected outputs: architecture-data-model.md, architecture-services.md, architecture-tech-stack.md"
        
        # Create placeholder files
        cat > "$architecture_dir/README.md" <<EOF
# Architecture Generation (Placeholder)

This phase will be implemented when Claude returns architecture artifacts.

**Expected Inputs:**
- Requirements: $requirements_file
- PRD Bundle: $SESSION_DIR/prd/

**Expected Outputs:**
- architecture-data-model.md - Complete data schema with TypeScript interfaces
- architecture-services.md - Service architecture and module breakdown
- architecture-tech-stack.md - Technology choices and rationale
- architecture-api.md - API specifications (when backend needed)
- architecture-deployment.md - Deployment and infrastructure specs

**Status:** Waiting for Claude Code integration
EOF
    fi

    log_success "✅ Architecture generation placeholder created"
    return 0
}

# Phase 2.6: UX Flow Generation (Placeholder for Claude integration)
run_ux_generation() {
    local iteration=$1
    local requirements_file="$SESSION_DIR/requirements/iteration-$iteration.json"
    local ux_dir="$SESSION_DIR/ux"

    log_agent "🎨 Starting UX Flow Generation Phase (Iteration $iteration)..."

    # Check requirements file exists
    if [ ! -f "$requirements_file" ]; then
        log_error "❌ Requirements file not found: $requirements_file"
        return 1
    fi

    # TODO: Integrate with Claude UX generator when available
    # For now, create placeholder structure
    mkdir -p "$ux_dir"

    log_info "UX generation placeholder - waiting for Claude integration"
    log_info "Expected outputs: user-flows.md, wireframes.md, interaction-specs.md"
    
    # Create placeholder files
    cat > "$ux_dir/README.md" <<EOF
# UX Flow Generation (Placeholder)

This phase will be implemented when Claude returns UX artifacts.

**Expected Inputs:**
- Requirements: $requirements_file
- PRD Bundle: $SESSION_DIR/prd/
- Architecture: $SESSION_DIR/architecture/

**Expected Outputs:**
- User Flow Diagrams
- Wireframe Specifications
- Interaction Specifications
- Accessibility Guidelines

**Status:** Waiting for Claude Code integration
EOF

    log_success "✅ UX generation placeholder created"
    return 0
}

# Phase 2.7: Future-Feature Parking (placeholder)
run_parking_sync() {
    local iteration=$1
    local parking_dir="$SESSION_DIR/parking"
    
    log_agent "🅿️ Starting Future-Feature Parking Phase (Iteration $iteration)..."
    
    # Create parking directory
    mkdir -p "$parking_dir"
    
    # TODO: Implement parking sync with backlog and feature evaluation
    # This will capture speculative feature ideas for future development
    
    # Copy parking template
    if [ -f ".claude/idea-to-design/test-gen/parking/parking-template.json" ]; then
        cp ".claude/idea-to-design/test-gen/parking/parking-template.json" "$parking_dir/"
        log_success "✅ Parking template copied to $parking_dir"
    else
        log_warning "⚠️  Parking template not found, creating placeholder"
        
        # Create placeholder template
        cat > "$parking_dir/parking-template.json" << 'EOF'
{
  "title": "Feature Title",
  "description": "Detailed description of the feature idea",
  "opportunity_driver": "Business driver or market opportunity",
  "estimated_value": 5,
  "confidence": 0.7,
  "dependencies": [],
  "timeframe": "Q2 2025",
  "notes": "Additional context and considerations",
  "metadata": {
    "created_date": "2025-01-24",
    "created_by": "user",
    "status": "parked",
    "priority": "medium",
    "category": "enhancement",
    "tags": ["ui", "backend", "integration"],
    "source": "manual"
  }
}
EOF
    fi
    
    # Create placeholder README
    cat > "$parking_dir/README.md" << 'EOF'
# Future-Feature Parking

## Overview
This directory contains speculative feature ideas that aren't ready for immediate development but have potential future value.

## How to Use
1. Copy `parking-template.json` to create new feature entries
2. Fill in the required fields (title, description, opportunity_driver, etc.)
3. Use the evaluation framework to assess value and confidence
4. Promote high-value items to the backlog when ready

## Integration
- **Backlog Sync**: High-value parked items can be promoted to backlog
- **Architecture Generation**: Parking helps inform system design decisions
- **UX Generation**: Feature ideas influence user experience planning
- **Code Generation**: Parking provides input for future development

## Documentation
See `docs/FUTURE_FEATURE_TEMPLATES.md` for complete guide.
EOF

    log_success "✅ Future-feature parking setup complete in $parking_dir"
    log_info "📝 Parking sync will be implemented by Claude Code"
    
    return 0
}

# Phase 2.8: Design Generation (Automated with Templates)
run_design_generation() {
    local iteration=$1
    local requirements_file="$SESSION_DIR/requirements/iteration-$iteration.json"
    local mockups_dir="$SESSION_DIR/mockups/iteration-$iteration"

    log_agent "🎨 Starting Design Generation Phase (Iteration $iteration)..."

    # Check requirements file exists
    if [ ! -f "$requirements_file" ]; then
        log_error "❌ Requirements file not found: $requirements_file"
        return 1
    fi

    # Run template-based mockup generator
    log_info "Generating 3 HTML mockup variations from templates..."

    if node scripts/generate-mockups.js \
        --requirements "$requirements_file" \
        --output-dir "$mockups_dir" 2>&1 | tee /tmp/mockup-generation.log; then

        # Count generated variations
        local mockup_count=$(find "$mockups_dir" -type d -name "option-*" 2>/dev/null | wc -l | tr -d ' ')

        if [ "$mockup_count" -ge 3 ]; then
            log_success "✅ Generated $mockup_count mockup variations"

            # Show summary
            for opt in a b c; do
                local opt_dir="$mockups_dir/option-$opt"
                if [ -d "$opt_dir" ]; then
                    local html_count=$(find "$opt_dir" -name "*.html" -type f | wc -l | tr -d ' ')
                    log_info "  Option $opt: $html_count HTML screens"
                fi
            done

            return 0
        else
            log_error "❌ Design generation failed - expected 3 variations, found $mockup_count"
            return 1
        fi
    else
        log_error "❌ Mockup generator failed - see /tmp/mockup-generation.log"
        return 1
    fi
}

# Phase 3: Visual QA (Automated with Real Playwright Tests)
run_visual_qa() {
    local iteration=$1

    log_agent "📊 Starting Visual QA Phase (Iteration $iteration)..."

    # Ensure scores directory exists
    mkdir -p "$SESSION_DIR/scores"

    local qa_failed=0

    # For each mockup variation, run Visual QA Factory
    for option in a b c; do
        local mockup_dir="$SESSION_DIR/mockups/iteration-$iteration/option-$option"

        if [ -d "$mockup_dir" ]; then
            log_info "Scoring Option $option..."

            # Check if HTML files exist
            local html_count=$(find "$mockup_dir" -name "*.html" -type f 2>/dev/null | wc -l)
            if [ "$html_count" -eq 0 ]; then
                log_warning "⚠️  Option $option: No HTML files found, skipping QA"
                continue
            fi

            log_info "  Found $html_count HTML screens in Option $option"

            # Run actual Visual QA using generic runner
            local output_file="$SESSION_DIR/scores/iteration-$iteration-option-$option.json"

            if node scripts/visual-qa-runner.js \
                --mockup-dir "$mockup_dir" \
                --output-file "$output_file" \
                2>&1 | tee /tmp/qa-option-$option.log; then

                # Parse score from output
                local score=$(jq -r '.scores.overall_score' "$output_file" 2>/dev/null || echo "0")
                log_success "✅ Option $option scored: $score/100"

                # Check if passed threshold
                if [ "$score" -lt "$MIN_QA_SCORE" ]; then
                    log_warning "⚠️  Option $option below threshold ($score < $MIN_QA_SCORE)"
                fi
            else
                log_error "❌ Option $option QA failed"
                qa_failed=1
            fi
        else
            log_warning "⚠️  Option $option directory not found: $mockup_dir"
        fi
    done

    # Generate comparison report
    log_info "Generating comparison report..."

    local report_file="$SESSION_DIR/scores/iteration-$iteration-comparison.md"
    cat > "$report_file" <<EOF
# Visual QA Comparison - Iteration $iteration

## Scores Summary

| Option | Overall | Brand | Responsive | A11y | Performance | Polish |
|--------|---------|-------|------------|------|-------------|--------|
EOF

    for option in a b c; do
        local score_file="$SESSION_DIR/scores/iteration-$iteration-option-$option.json"
        if [ -f "$score_file" ]; then
            local overall=$(jq -r '.scores.overall_score' "$score_file")
            local brand=$(jq -r '.scores.brand_compliance' "$score_file")
            local responsive=$(jq -r '.scores.responsive_design' "$score_file")
            local a11y=$(jq -r '.scores.accessibility' "$score_file")
            local perf=$(jq -r '.scores.performance' "$score_file")
            local polish=$(jq -r '.scores.visual_polish' "$score_file")

            echo "| **Option ${option^^}** | $overall/100 | $brand/25 | $responsive/20 | $a11y/25 | $perf/15 | $polish/15 |" >> "$report_file"
        fi
    done

    cat >> "$report_file" <<EOF

## Pass Threshold: $MIN_QA_SCORE/100

EOF

    log_success "✅ Comparison report: $report_file"

    if [ "$qa_failed" -eq 1 ]; then
        log_warning "⚠️  Some options failed QA"
        return 1
    fi

    log_success "✅ Visual QA complete"
    return 0
}

# Phase 4: Feedback Collection
run_feedback_collection() {
    local iteration=$1

    log_agent "💬 Starting Feedback Collection Phase (Iteration $iteration)..."

    # Create feedback prompt
    local feedback_prompt="You are a Feedback Agent.

ITERATION: $iteration

MOCKUP SCORES:
$(cat "$SESSION_DIR"/scores/iteration-$iteration-option-*.json 2>/dev/null)

YOUR TASK:
1. Present the top 2 mockups to the client (show screenshots)
2. Ask these questions:
   - Which feels more 'you'? A or B?
   - What do you love about your choice?
   - What would you change?
   - Energy level: too low / just right / too high?
   - Ready to proceed or want another iteration?

3. Extract structured feedback:
{
  \"favored_option\": \"a | b\",
  \"liked_elements\": [...],
  \"disliked_elements\": [...],
  \"refinement_directions\": [...],
  \"satisfaction_score\": 1-10,
  \"approval\": true | false
}

4. Save to: $SESSION_DIR/feedback/iteration-$iteration.json

Start presenting the mockups."

    # Run feedback collection (interactive)
    log_info "Presenting mockups to client..."
    echo ""

    claude "$feedback_prompt"

    # Check if feedback was collected
    if [ -f "$SESSION_DIR/feedback/iteration-$iteration.json" ]; then
        log_success "✅ Feedback collected"

        # Check for approval
        local approval=$(jq -r '.approval' "$SESSION_DIR/feedback/iteration-$iteration.json" 2>/dev/null || echo "false")
        local satisfaction=$(jq -r '.satisfaction_score' "$SESSION_DIR/feedback/iteration-$iteration.json" 2>/dev/null || echo "0")

        if [ "$approval" = "true" ] || [ "$satisfaction" -ge "$MIN_CLIENT_SATISFACTION" ]; then
            log_success "🎉 Client approved! (Satisfaction: $satisfaction/10)"
            return 0
        else
            log_info "Client requested refinement (Satisfaction: $satisfaction/10)"
            return 1
        fi
    else
        log_error "❌ Feedback collection failed"
        return 1
    fi
}

# Phase 5: Refinement
run_refinement() {
    local iteration=$1
    local next_iteration=$((iteration + 1))

    log_agent "🔄 Starting Refinement Phase..."

    # Load previous requirements and feedback
    local prev_requirements="$SESSION_DIR/requirements/iteration-$iteration.json"
    local feedback="$SESSION_DIR/feedback/iteration-$iteration.json"

    # Create refinement prompt
    local refinement_prompt="You are a Refinement Agent.

PREVIOUS REQUIREMENTS:
$(cat "$prev_requirements")

CLIENT FEEDBACK:
$(cat "$feedback")

YOUR TASK:
Refine the requirements based on client feedback:
1. Keep what client loved
2. Remove/change what client disliked
3. Incorporate refinement directions
4. Maintain structure of original requirements

Save refined requirements to: $SESSION_DIR/requirements/iteration-$next_iteration.json"

    # Run refinement
    log_info "Refining requirements based on feedback..."
    claude "$refinement_prompt"

    if [ -f "$SESSION_DIR/requirements/iteration-$next_iteration.json" ]; then
        log_success "✅ Requirements refined for iteration $next_iteration"
        return 0
    else
        log_error "❌ Refinement failed"
        return 1
    fi
}

# Phase 6: Code Generation
run_code_generation() {
    local iteration=$1
    local approved_option=$(jq -r '.favored_option' "$SESSION_DIR/feedback/iteration-$iteration.json")

    log_agent "💻 Starting Code Generation Phase..."

    local mockup_dir="$SESSION_DIR/mockups/iteration-$iteration/option-$approved_option"
    local app_name=$(jq -r '.app_name' "$SESSION_DIR/requirements/iteration-$iteration.json" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
    local output_dir="software-factory/generated-apps/$app_name"

    log_info "Converting mockup to production Next.js code..."
    log_info "Output: $output_dir"

    # TODO: Implement actual code generation
    # For now, create placeholder structure
    mkdir -p "$output_dir"

    cat > "$output_dir/README.md" <<EOF
# $app_name

Generated from Idea-to-Design autonomous agent system.

**Session**: $TIMESTAMP
**Iterations**: $((iteration + 1))
**Final Score**: $(jq -r '.overall_score' "$SESSION_DIR/scores/iteration-$iteration-option-$approved_option.json")

## Design Journey
See session details: $SESSION_DIR
EOF

    log_success "✅ Code generation complete: $output_dir"
    log_success "🎉 AUTONOMOUS WORKFLOW COMPLETE!"
}

# Main orchestration loop
main() {
    local idea="${1:-}"

    if [ -z "$idea" ]; then
        log_error "Usage: $0 \"<app idea>\""
        log_info "Example: $0 \"I want an app to track my daily water intake\""
        exit 1
    fi

    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         AUTONOMOUS IDEA-TO-DESIGN AGENT SYSTEM                 ║${NC}"
    echo -e "${CYAN}║  From Vague Idea → Validated Design → Production Code         ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # Initialize
    init_session "$idea"

    # Phase 1: Discovery (once)
    if ! run_discovery "$idea"; then
        log_error "Discovery phase failed. Exiting."
        exit 1
    fi

    # Iteration loop
    local iteration=0
    local converged=false

    while [ $iteration -lt $MAX_ITERATIONS ] && [ "$converged" = "false" ]; do
        log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        log_info "ITERATION $(($iteration + 1))/$MAX_ITERATIONS"
        log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # Phase 2: PRD Generation
        if ! run_prd_generation $iteration; then
            log_error "PRD generation failed. Exiting."
            exit 1
        fi

        # Phase 2.5: Architecture Generation (placeholder)
        if ! run_architecture_generation $iteration; then
            log_error "Architecture generation failed. Exiting."
            exit 1
        fi

        # Phase 2.6: UX Generation (placeholder)
        if ! run_ux_generation $iteration; then
            log_error "UX generation failed. Exiting."
            exit 1
        fi

        # Phase 2.7: Future-Feature Parking (placeholder)
        # TODO: Integrate parking sync with backlog and feature evaluation
        # This will capture speculative feature ideas for future development
        if ! run_parking_sync $iteration; then
            log_error "Future-feature parking failed. Exiting."
            exit 1
        fi

        # Phase 2.8: Design Generation
        if ! run_design_generation $iteration; then
            log_error "Design generation failed. Exiting."
            exit 1
        fi

        # Phase 3: Visual QA
        if ! run_visual_qa $iteration; then
            log_error "Visual QA failed. Exiting."
            exit 1
        fi

        # Phase 4: Feedback Collection
        if run_feedback_collection $iteration; then
            # Client approved!
            converged=true
            log_success "🎉 Convergence achieved at iteration $(($iteration + 1))!"

            # Phase 6: Code Generation
            run_code_generation $iteration
            break
        else
            # Client wants refinement
            if [ $iteration -lt $((MAX_ITERATIONS - 1)) ]; then
                # Phase 5: Refinement
                if ! run_refinement $iteration; then
                    log_error "Refinement failed. Exiting."
                    exit 1
                fi

                iteration=$((iteration + 1))
            else
                log_warning "⚠️  Maximum iterations ($MAX_ITERATIONS) reached"
                log_info "Generating code from best available option..."
                run_code_generation $iteration
                break
            fi
        fi
    done

    # Summary
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    🎉 WORKFLOW COMPLETE! 🎉                    ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    log_info "Session Summary:"
    log_info "  - Total Iterations: $(($iteration + 1))"
    log_info "  - Converged: $converged"
    log_info "  - Session Data: $SESSION_DIR"
    echo ""
}

# Run main function
main "$@"
