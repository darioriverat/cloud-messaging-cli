#!/bin/bash

# Exit on error
set -o errexit

# Load environment variables from .env file if it exists
if [[ -f ".env" ]]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Set GCP project if GCP_PROJECT_ID is specified
if [[ -n "$GCP_PROJECT_ID" ]]; then
    echo "Setting GCP project to: $GCP_PROJECT_ID"
    gcloud config set core/project "$GCP_PROJECT_ID"
else
    echo "Warning: GCP_PROJECT_ID not set. Using default project."
fi



# Function to display usage
show_usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create-docker-repository <NAME> [--location <LOCATION>]  Create a new Docker repository"
    echo ""
    echo "Options:"
    echo "  --location <LOCATION>  Specify the repository location (required)"
    echo ""
    echo "Examples:"
    echo "  $0 create-docker-repository my-repo --location us-central1"
    echo ""
    echo "Environment Variables:"
    echo "  GCP_PROJECT_ID: Set in .env file or environment to specify the GCP project"
    echo ""
    echo "For more information about gcloud artifacts repositories, run:"
    echo "  gcloud artifacts repositories --help"
}

# Function to create Docker repository
create_docker_repository() {
    local repo_name=""
    local location=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --location)
                location="$2"
                shift 2
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            -*)
                echo "Error: Unknown option $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$repo_name" ]]; then
                    repo_name="$1"
                else
                    echo "Error: Too many arguments"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$repo_name" ]]; then
        echo "Error: Repository name is required"
        echo "Usage: $0 create-docker-repository <NAME> --location <LOCATION>"
        exit 1
    fi

    if [[ -z "$location" ]]; then
        echo "Error: --location is required"
        echo "Usage: $0 create-docker-repository <NAME> --location <LOCATION>"
        echo "Example: $0 create-docker-repository my-repo --location us-central1"
        exit 1
    fi

    echo "Creating Docker repository: $repo_name in location: $location"

    # Build the gcloud command with location
    local gcloud_cmd="gcloud artifacts repositories create \"$repo_name\" --repository-format=docker --location=\"$location\""

    echo "Executing: $gcloud_cmd"
    eval "$gcloud_cmd"
}

# Main script logic
main() {
    # Check if at least one argument is provided
    if [[ $# -eq 0 ]]; then
        show_usage
        exit 1
    fi

    local command="$1"
    shift

    case "$command" in
        "create-docker-repository")
            create_docker_repository "$@"
            ;;
        "help"|"--help"|"-h")
            show_usage
            ;;
        *)
            echo "Error: Unknown command '$command'"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"

