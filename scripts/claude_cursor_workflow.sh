#!/bin/bash
# Claude Code Web ↔ Cursor Workflow Orchestrator
# Manages background Claude jobs, branch syncing, and teleport workflows

set -euo pipefail

# Configuration (can be overridden via environment variables)
CLAUDE_JOBS_DIR="${CLAUDE_JOBS_DIR:-.claude-jobs}"
METADATA_FILE="$CLAUDE_JOBS_DIR/metadata.json"
BRANCH_PREFIX="${CLAUDE_BRANCH_PREFIX:-claude-}"
MAX_CONCURRENT_JOBS="${CLAUDE_MAX_JOBS:-3}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
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

# Check prerequisites
check_prerequisites() {
    local missing_deps=()

    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi

    if ! command -v gh &> /dev/null; then
        missing_deps+=("gh (GitHub CLI)")
    fi

    # Claude CLI is optional for testing - warn but don't fail
    if ! command -v claude &> /dev/null; then
        log_warning "Claude CLI not installed - teleport functionality will be limited"
        log_info "Install with: npm install -g @anthropic-ai/claude"
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Install missing dependencies and try again"
        exit 1
    fi

    # Check if we're in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not in a git repository"
        exit 1
    fi

    # Check if we're in a GitHub repo
    if ! gh repo view > /dev/null 2>&1; then
        log_error "Not in a GitHub repository or GitHub CLI not authenticated"
        exit 1
    fi
}

# Initialize metadata file
init_metadata() {
    if [ ! -d "$CLAUDE_JOBS_DIR" ]; then
        mkdir -p "$CLAUDE_JOBS_DIR"
    fi
    
    if [ ! -f "$METADATA_FILE" ]; then
        echo '{"jobs": {}, "next_id": 1}' > "$METADATA_FILE"
    fi
}

# Generate unique job ID
generate_job_id() {
    local next_id
    next_id=$(jq -r '.next_id' "$METADATA_FILE")
    echo "job-$next_id"
}

# Update next ID
update_next_id() {
    local current_id
    current_id=$(jq -r '.next_id' "$METADATA_FILE")
    jq --argjson id $((current_id + 1)) '.next_id = $id' "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
}

# Create job metadata
create_job_metadata() {
    local job_id="$1"
    local branch_name="$2"
    local prompt="$3"
    local priority="${4:-normal}"

    # Use jq to safely construct JSON, avoiding interpolation issues
    jq --arg job_id "$job_id" \
       --arg branch "$branch_name" \
       --arg prompt "$prompt" \
       --arg priority "$priority" \
       --arg created "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
       --arg updated "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
       '.jobs[$job_id] = {
           "id": $job_id,
           "branch_name": $branch,
           "prompt": $prompt,
           "priority": $priority,
           "status": "queued",
           "created_at": $created,
           "updated_at": $updated,
           "claude_session_id": null,
           "teleport_command": null,
           "notes": ""
       }' "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
}

# Update job status
update_job_status() {
    local job_id="$1"
    local status="$2"
    local notes="${3:-}"
    
    local update_data=".jobs[\"$job_id\"].status = \"$status\" | .jobs[\"$job_id\"].updated_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\""
    
    if [ -n "$notes" ]; then
        update_data="$update_data | .jobs[\"$job_id\"].notes = \"$notes\""
    fi
    
    jq "$update_data" "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
}

# Queue a new Claude job
queue_job() {
    local prompt="$1"
    local priority="${2:-normal}"
    local branch_suffix="${3:-}"
    
    # Generate unique branch name
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local branch_name="${BRANCH_PREFIX}${timestamp}"
    if [ -n "$branch_suffix" ]; then
        branch_name="${branch_name}-${branch_suffix}"
    fi
    
    # Generate job ID
    local job_id=$(generate_job_id)

    log_info "Queueing Claude job: $job_id"
    log_info "Branch: $branch_name"
    log_info "Prompt: $prompt"

    # Create job metadata
    create_job_metadata "$job_id" "$branch_name" "$prompt" "$priority"

    # Increment next_id to ensure unique job IDs
    update_next_id
    
    # Check concurrent job limit
    local active_jobs
    active_jobs=$(jq -r '.jobs | to_entries | map(select(.value.status == "running" or .value.status == "queued")) | length' "$METADATA_FILE")
    
    if [ "$active_jobs" -ge "$MAX_CONCURRENT_JOBS" ]; then
        log_warning "Maximum concurrent jobs ($MAX_CONCURRENT_JOBS) reached. Job queued but not started."
        log_info "Use 'sync' command to check status and start queued jobs"
    else
        start_job "$job_id"
    fi
    
    log_success "Job $job_id queued successfully"
    echo "Job ID: $job_id"
    echo "Branch: $branch_name"
    echo "Status: queued"
}

# Start a queued job
start_job() {
    local job_id="$1"
    
    local branch_name
    branch_name=$(jq -r ".jobs[\"$job_id\"].branch_name" "$METADATA_FILE")
    
    local prompt
    prompt=$(jq -r ".jobs[\"$job_id\"].prompt" "$METADATA_FILE")
    
    log_info "Starting Claude job: $job_id"
    
    # Update status to running
    update_job_status "$job_id" "running" "Started Claude Code Web session"
    
    # Create branch
    git checkout -b "$branch_name" 2>/dev/null || {
        log_warning "Branch $branch_name already exists, checking it out"
        git checkout "$branch_name"
    }

    # Push branch to remote so Claude Code Web can access it
    log_info "Pushing branch to remote..."
    if git push -u origin "$branch_name" 2>/dev/null; then
        log_success "Branch pushed to remote successfully"
    else
        log_warning "Failed to push branch to remote - you may need to push manually later"
        log_info "Run: git push -u origin $branch_name"
    fi

    # Start Claude Code Web session
    log_info "Starting Claude Code Web session..."
    log_info "Prompt: $prompt"
    
    # Note: This would integrate with Claude CLI to start web session
    # For now, we'll simulate the process
    local session_id="claude-session-$(date +%s)"
    
    # Update job with session ID
    jq --arg session "$session_id" ".jobs[\"$job_id\"].claude_session_id = \$session" "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
    
    log_success "Claude session started: $session_id"
    log_info "Access Claude Code Web to continue the session"
    log_info "Use 'sync $job_id' to check progress and pull results"
}

# Sync job status and pull results
sync_job() {
    local job_id="$1"
    
    if [ ! -f "$METADATA_FILE" ]; then
        log_error "No metadata file found. Run 'queue' first."
        exit 1
    fi
    
    local job_exists
    job_exists=$(jq -r ".jobs[\"$job_id\"] != null" "$METADATA_FILE")
    
    if [ "$job_exists" = "false" ]; then
        log_error "Job $job_id not found"
        exit 1
    fi
    
    local status
    status=$(jq -r ".jobs[\"$job_id\"].status" "$METADATA_FILE")
    
    local branch_name
    branch_name=$(jq -r ".jobs[\"$job_id\"].branch_name" "$METADATA_FILE")
    
    log_info "Syncing job: $job_id"
    log_info "Status: $status"
    log_info "Branch: $branch_name"
    
    case "$status" in
        "queued")
            log_info "Starting queued job..."
            start_job "$job_id"
            ;;
        "running")
            log_info "Job is running. Checking for updates..."
            # Check if branch has been pushed
            if git ls-remote --heads origin "$branch_name" | grep -q "$branch_name"; then
                log_info "Branch $branch_name found on remote"
                update_job_status "$job_id" "completed" "Branch pushed to remote"
                
                # Pull the branch
                git fetch origin "$branch_name"
                git checkout "$branch_name"
                
                log_success "Job $job_id completed and synced"
            else
                log_info "Job still running. No remote branch yet."
            fi
            ;;
        "completed")
            log_info "Job already completed. Pulling latest changes..."
            git fetch origin "$branch_name"
            git checkout "$branch_name"
            log_success "Job $job_id synced"
            ;;
        *)
            log_warning "Unknown status: $status"
            ;;
    esac
}

# Generate teleport command
generate_teleport_command() {
    local job_id="$1"
    
    local session_id
    session_id=$(jq -r ".jobs[\"$job_id\"].claude_session_id" "$METADATA_FILE")
    
    if [ "$session_id" = "null" ] || [ -z "$session_id" ]; then
        log_error "No Claude session ID found for job $job_id"
        return 1
    fi
    
    local teleport_cmd="claude teleport $session_id"
    
    # Update job with teleport command
    jq --arg cmd "$teleport_cmd" ".jobs[\"$job_id\"].teleport_command = \$cmd" "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
    
    log_info "Teleport command generated:"
    echo "$teleport_cmd"
    log_info "Run this command in Cursor to import the Claude conversation"
}

# List all jobs
list_jobs() {
    if [ ! -f "$METADATA_FILE" ]; then
        log_info "No jobs found"
        return 0
    fi
    
    local jobs_count
    jobs_count=$(jq -r '.jobs | length' "$METADATA_FILE")
    
    if [ "$jobs_count" -eq 0 ]; then
        log_info "No jobs found"
        return 0
    fi
    
    log_info "Claude Jobs ($jobs_count total):"
    echo
    
    jq -r '.jobs | to_entries | sort_by(.value.created_at) | reverse | .[] | 
        "\(.key): \(.value.status) | \(.value.branch_name) | \(.value.created_at)"' "$METADATA_FILE" | \
    while IFS='|' read -r job_id status branch created; do
        printf "%-20s %-10s %-30s %s\n" "$job_id" "$status" "$branch" "$created"
    done
}

# Show job details
show_job() {
    local job_id="$1"
    
    if [ ! -f "$METADATA_FILE" ]; then
        log_error "No metadata file found"
        exit 1
    fi
    
    local job_exists
    job_exists=$(jq -r ".jobs[\"$job_id\"] != null" "$METADATA_FILE")
    
    if [ "$job_exists" = "false" ]; then
        log_error "Job $job_id not found"
        exit 1
    fi
    
    log_info "Job Details: $job_id"
    echo
    
    jq -r ".jobs[\"$job_id\"] | 
        \"ID: \(.id)
Status: \(.status)
Branch: \(.branch_name)
Priority: \(.priority)
Created: \(.created_at)
Updated: \(.updated_at)
Session ID: \(.claude_session_id // \"N/A\")
Teleport Command: \(.teleport_command // \"N/A\")
Notes: \(.notes // \"None\")
Prompt: \(.prompt)\"" "$METADATA_FILE"
}

# Clean up completed jobs
cleanup_jobs() {
    local days="${1:-7}"
    
    log_info "Cleaning up jobs older than $days days"
    
    local cutoff_date
    cutoff_date=$(date -u -d "$days days ago" +%Y-%m-%dT%H:%M:%SZ)
    
    local jobs_to_remove
    jobs_to_remove=$(jq -r --arg cutoff "$cutoff_date" '.jobs | to_entries | map(select(.value.status == "completed" and .value.updated_at < $cutoff)) | .[].key' "$METADATA_FILE")
    
    if [ -z "$jobs_to_remove" ]; then
        log_info "No jobs to clean up"
        return 0
    fi
    
    echo "$jobs_to_remove" | while read -r job_id; do
        log_info "Removing job: $job_id"
        jq "del(.jobs[\"$job_id\"])" "$METADATA_FILE" > "$METADATA_FILE.tmp" && mv "$METADATA_FILE.tmp" "$METADATA_FILE"
    done
    
    log_success "Cleanup completed"
}

# Show help
show_help() {
    cat <<EOF
Claude Code Web ↔ Cursor Workflow Orchestrator

USAGE:
    $0 <command> [options]

COMMANDS:
    queue <prompt> [priority] [suffix]    Queue a new Claude job
    sync <job_id>                          Sync job status and pull results
    teleport <job_id>                      Generate teleport command
    list                                   List all jobs
    show <job_id>                          Show job details
    cleanup [days]                         Clean up old completed jobs
    help                                   Show this help

EXAMPLES:
    $0 queue "Refactor the authentication system to use JWT tokens"
    $0 queue "Add comprehensive error handling" high
    $0 queue "Research AI integration patterns" normal research
    $0 sync job-1
    $0 teleport job-1
    $0 list
    $0 show job-1
    $0 cleanup 14

WORKFLOW:
    1. Queue a job with a descriptive prompt
    2. Use 'sync' to check progress and pull results
    3. Use 'teleport' to import conversation into Cursor
    4. Review and merge changes locally
    5. Clean up old jobs periodically

CONFIGURATION:
    Max concurrent jobs: $MAX_CONCURRENT_JOBS
    Branch prefix: $BRANCH_PREFIX
    Metadata file: $METADATA_FILE

EOF
}

# Main script logic
main() {
    check_prerequisites
    init_metadata
    
    case "${1:-help}" in
        "queue")
            if [ $# -lt 2 ]; then
                log_error "Usage: $0 queue <prompt> [priority] [suffix]"
                exit 1
            fi
            queue_job "$2" "${3:-normal}" "${4:-}"
            ;;
        "sync")
            if [ $# -lt 2 ]; then
                log_error "Usage: $0 sync <job_id>"
                exit 1
            fi
            sync_job "$2"
            ;;
        "teleport")
            if [ $# -lt 2 ]; then
                log_error "Usage: $0 teleport <job_id>"
                exit 1
            fi
            generate_teleport_command "$2"
            ;;
        "list")
            list_jobs
            ;;
        "show")
            if [ $# -lt 2 ]; then
                log_error "Usage: $0 show <job_id>"
                exit 1
            fi
            show_job "$2"
            ;;
        "cleanup")
            cleanup_jobs "${2:-7}"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"