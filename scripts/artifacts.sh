#!/bin/bash

# Exit on error
set -o errexit

# Load environment variables from .env file if it exists
if [[ -f ".env" ]]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check current gcloud project and compare with .env file
if [[ -n "$GCP_PROJECT_ID" ]]; then
    # Get current project from gcloud config
    current_project=$(gcloud config get-value core/project 2>/dev/null || echo "")

    if [[ -n "$current_project" ]]; then
        if [[ "$current_project" == "$GCP_PROJECT_ID" ]]; then
            # Project already set to $GCP_PROJECT_ID, no update needed
            project_id="$GCP_PROJECT_ID"
        else
            # Updating project from $current_project to $GCP_PROJECT_ID
            gcloud config set core/project "$GCP_PROJECT_ID"
            project_id="$GCP_PROJECT_ID"
        fi
    else
        # No project currently set, setting to $GCP_PROJECT_ID
        gcloud config set core/project "$GCP_PROJECT_ID"
        project_id="$GCP_PROJECT_ID"
    fi
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
    echo "  auth-docker-location <LOCATION>  Configure Docker authentication for the specified location"
    echo "  docker config  Display Docker configuration"
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
    echo "  $0 auth-docker-location us-central1"
    echo "  $0 docker config"
    echo ""
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

# Function to configure Docker authentication for a location
auth_docker_location() {
    local location=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
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
                if [[ -z "$location" ]]; then
                    location="$1"
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
    if [[ -z "$location" ]]; then
        echo "Error: Location is required"
        echo "Usage: $0 auth-docker-location <LOCATION>"
        exit 1
    fi

    # Build registry URL from location
    local registry_url="${location}-docker.pkg.dev"

    echo "Configuring Docker authentication for location: $location..."

    # Configure Docker authentication
    echo "Executing: gcloud auth configure-docker \"$registry_url\""
    gcloud auth configure-docker "$registry_url"

    echo "Successfully configured Docker authentication for $registry_url"
}

# Function to display Docker configuration
docker_config() {
    local subcommand=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
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
                if [[ -z "$subcommand" ]]; then
                    subcommand="$1"
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
    if [[ -z "$subcommand" ]]; then
        echo "Error: Subcommand is required"
        echo "Usage: $0 docker <SUBCOMMAND>"
        echo "Available subcommands: config"
        exit 1
    fi

    case "$subcommand" in
        "config")
            echo "Displaying Docker configuration..."
            if [[ -f ~/.docker/config.json ]]; then
                cat ~/.docker/config.json | jq .
            else
                echo "Docker configuration file not found at ~/.docker/config.json"
                exit 1
            fi
            ;;
        *)
            echo "Error: Unknown subcommand '$subcommand'"
            echo "Available subcommands: config"
            exit 1
            ;;
    esac
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
        "auth-docker-location")
            auth_docker_location "$@"
            ;;
        "docker")
            docker_config "$@"
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

