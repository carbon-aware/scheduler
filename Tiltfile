# Tiltfile for carbon-aware/scheduler

load('tilt/utils.Tiltfile', 'create_secret')

create_secret('scheduler/.env', 'carbon-aware-scheduler', 'default')

# -- Build the scheduler image
docker_build(
    'ghcr.io/carbon-aware/scheduler:latest',
    'scheduler',
)

# --- Deploy Helm chart ---
k8s_yaml(helm(
    './helm/scheduler',
    name='scheduler',
    namespace='default',
))


# -- Port forwarding ---
k8s_resource(
    'scheduler',
    port_forwards=[
        port_forward(8080, 8080, name='scheduler'),
    ],
    labels=['carbon-aware']
)

k8s_resource(
    'scheduler-memcached',
    port_forwards=[
        port_forward(11211, 11211, name='scheduler-memcached'),
    ],
    labels=['carbon-aware']
)