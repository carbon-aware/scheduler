def create_secret(path, name, namespace):
    local("kubectl create secret generic {name} --from-env-file={path} -n {namespace} --save-config --dry-run=client -o yaml | kubectl apply -f -".format(name=name, path=path, namespace=namespace))
