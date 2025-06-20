# Tiltfile for carbon-aware/scheduler

load('tilt/utils.Tiltfile', 'create_secret')

create_secret('scheduler/.env', 'carbon-aware-scheduler', 'default')

# -- Build the scheduler image
docker_build(
    'ghcr.io/carbon-aware/scheduler/backend:latest',
    'scheduler',
    live_update=[
        sync(
            "./scheduler/src",
            "/app/src",
        ),
    ],
    target="local"
)

# --- Deploy Helm chart ---
k8s_yaml(helm(
    './helm/scheduler',
    name='scheduler',
    namespace='default',
    set=["scheduler.image.tag=latest", "scheduler.watttime.existingSecret.name=carbon-aware-scheduler"]
))


# -- Port forwarding ---
k8s_resource(
    'scheduler',
    port_forwards=[
        port_forward(8080, 8080, name='scheduler'),
    ],
    labels=['carbon-aware']
)
