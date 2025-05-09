# scheduler
Carbon Aware job scheduler

## Installation

You can install the carbon-aware scheduler via Helm:

```
helm repo add carbon-aware https://carbon-aware.github.io/charts
helm install ca-scheduler -n carbon-aware carbon-aware/scheduler
```

Ensure you've included WattTime credentials in a secret in your carbon-aware namespace.

## Development

### Prerequisites

- Tilt
- kubectl
- kind
- ctlptl

### Usage

1. Start a kind cluster
```bash
ctlptl create cluster kind --name kind-ca-scheduler
```

2. Start Tilt
```bash
tilt up
```
