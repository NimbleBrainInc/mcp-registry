# mcp-registry deployment
# No build-time secrets needed (read-only API)

.PHONY: build push deploy status logs

# Configuration
ENV ?= staging
TAG ?= $(shell git rev-parse --short HEAD)
APP := mcp-registry

# AWS/ECR
AWS_ACCOUNT_ID := 533267450054
AWS_REGION := us-east-1
ECR := $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(APP)

# Helm chart (OCI registry)
CHART_REGISTRY := oci://$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/charts
CHART_VERSION ?= 0.3.0

# --- Targets ---

# Build Docker image for linux/amd64
build:
	@echo "Building $(APP):$(TAG) for $(ENV)..."
	@docker build --platform linux/amd64 -t $(ECR):$(TAG) .

# Login to ECR and push
push:
	@echo "Pushing $(APP):$(TAG) to ECR..."
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR)
	@docker push $(ECR):$(TAG)

# Login to ECR for Helm OCI
chart-login:
	@aws ecr get-login-password --region $(AWS_REGION) | helm registry login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

# Deploy with Helm (pulls chart from OCI registry)
helm: chart-login
	@echo "Deploying $(APP) to $(ENV) with tag $(TAG) using chart $(CHART_VERSION)..."
	@helm upgrade --install $(APP) $(CHART_REGISTRY)/web-app --version $(CHART_VERSION) \
		--namespace apps \
		--values k8s/$(ENV)/values.yaml \
		--set image.tag=$(TAG)

# Full deploy: build, push, helm
deploy: build push helm
	@echo "Deployed $(APP):$(TAG) to $(ENV)"

# Check deployment status
status:
	@kubectl get pods -n apps -l app.kubernetes.io/name=$(APP)
	@echo "---"
	@kubectl get ingress -n apps $(APP) 2>/dev/null || true

# Tail logs
logs:
	@kubectl logs -n apps -l app.kubernetes.io/name=$(APP) --tail=100 -f

# Show what would be built (dry run)
dry-run:
	@echo "Environment: $(ENV)"
	@echo "Tag: $(TAG)"
	@echo "ECR: $(ECR)"
	@echo "Chart: $(CHART_REGISTRY)/web-app:$(CHART_VERSION)"
