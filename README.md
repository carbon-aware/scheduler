# scheduler
Carbon Aware job scheduler

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
