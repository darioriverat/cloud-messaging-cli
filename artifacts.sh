#!/bin/bash

# Exit on error
set -o errexit

# Load environment variables from .env file if it exists
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs)
fi

# Set GCP project if GCP_PROJECT_ID is specified
if [[ -n "$GCP_PROJECT_ID" ]]; then
    gcloud config set core/project "$GCP_PROJECT_ID"
    project_id="$GCP_PROJECT_ID"
else
    echo "Error: GCP_PROJECT_ID not set. Please set it in the .env file."
    exit 1
fi



# Function to display usage
show_usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create-docker-repository <NAME> [--location <LOCATION>]  Create a new Docker repository"
    echo "  tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY> [--location <LOCATION>]  Tag local image for registry submission"
    echo "  push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>  Push Docker image to registry"
    echo ""
    echo "Options:"
    echo "  --location <LOCATION>  Specify the repository location (required for create-docker-repository and push-docker-image, optional for tag-docker-image)"
    echo "  --local-image <LOCAL_IMAGE>  Local Docker image name (required for tag-docker-image)"
    echo "  --remote-image <REMOTE_IMAGE>  Remote image name for registry (required for tag-docker-image)"
    echo "  --repository <REPOSITORY>  Repository name (required for tag-docker-image and push-docker-image)"
    echo ""
    echo "Examples:"
    echo "  $0 create-docker-repository my-repo --location us-central1"
    echo "  $0 tag-docker-image --local-image myapp:latest --remote-image myapp:v1.0.0 --repository my-repo --location us-central1"
    echo "  $0 push-docker-image myapp:v1.0.0 --repository my-repo --location us-central1"
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

# Function to tag Docker image for registry
tag_docker_image() {
    local local_image=""
    local remote_image=""
    local repository=""
    local location="us-central1"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --local-image)
                local_image="$2"
                shift 2
                ;;
            --remote-image)
                remote_image="$2"
                shift 2
                ;;
            --repository)
                repository="$2"
                shift 2
                ;;
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
                echo "Error: Unexpected argument $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$local_image" ]]; then
        echo "Error: --local-image is required"
        echo "Usage: $0 tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY>"
        exit 1
    fi

    if [[ -z "$remote_image" ]]; then
        echo "Error: --remote-image is required"
        echo "Usage: $0 tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY>"
        exit 1
    fi

    if [[ -z "$repository" ]]; then
        echo "Error: --repository is required"
        echo "Usage: $0 tag-docker-image --local-image <LOCAL_IMAGE> --remote-image <REMOTE_IMAGE> --repository <REPOSITORY>"
        exit 1
    fi

    # Build registry URL from location
    local registry_url="${location}-docker.pkg.dev"

    # Construct the full remote image name
    local full_remote_image="$registry_url/$project_id/$repository/$remote_image"

    echo "Tagging Docker image for registry submission..."

    # Tag the local image with the remote image name
    echo "Executing: docker tag \"$local_image\" \"$full_remote_image\""
    docker tag "$local_image" "$full_remote_image"

    echo "Successfully tagged $local_image as $full_remote_image"
}

    # Function to push Docker image to registry
push_docker_image() {
    local image_name=""
    local repository=""
    local location=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --repository)
                repository="$2"
                shift 2
                ;;
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
                if [[ -z "$image_name" ]]; then
                    image_name="$1"
                else
                    echo "Error: Too many arguments"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$image_name" ]]; then
        echo "Error: Image name is required"
        echo "Usage: $0 push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>"
        exit 1
    fi

    if [[ -z "$repository" ]]; then
        echo "Error: --repository is required"
        echo "Usage: $0 push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>"
        exit 1
    fi

    if [[ -z "$location" ]]; then
        echo "Error: --location is required"
        echo "Usage: $0 push-docker-image <IMAGE_NAME> --repository <REPOSITORY> --location <LOCATION>"
        exit 1
    fi

    # Build registry URL from location
    local registry_url="${location}-docker.pkg.dev"

    # Construct the full remote image name
    local full_remote_image="$registry_url/$project_id/$repository/$image_name"

    echo "Pushing Docker image to registry..."

    # Push the image to the registry
    echo "Executing: docker push \"$full_remote_image\""
    docker push "$full_remote_image"

    echo "Successfully pushed $image_name to $full_remote_image"
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
        "tag-docker-image")
            tag_docker_image "$@"
            ;;
        "push-docker-image")
            push_docker_image "$@"
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

