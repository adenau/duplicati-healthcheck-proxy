# Healthchecks Proxy

Healthchecks (found at https://healthchecks.io), is a cron monitor : it allows the monitoring of jobs that are run at regular intervals. However, it has a particular functionality not found in most cron monitor : the ability to signal failures. This allows Healthchecks to be used a centralized monitoring solution.

In itself, Healthchecks is a pretty flexible tool. It can receive callbacks from any third-party sources, including Zapier and other automation tools. However, some tools might require a "web call" to be transformed or modified before it is forwarded to Healthcheck. This project, ''Healchecks Proxy'', acts as an intermediary for some of these tools, allowing them to use Healthchecks with little changes to their configuration.

:warning: The project is in pre-release and documentation is still being written. 

# Currently Supported 3rd Parties

The following 3rd parties are currently supported :

## Duplicati

Duplicati is a backup software that can be installed on most modern desktop OS (Windows, Mac, Linux, etc.) and some NAS devices. It is Open Source, supports multiple backends and is managed from a web interface. However, it lacks centralized management and monitoring.

One useful feature of Duplicati is that when backups are completed, it can send a report to a specific URL. However, sending reports to Healthchecks.io directly is a bad a solution, as Healthchecks.io will not detected a failed backup. This project, ''Healchecks Proxy'', can detected a failed backup and send the appropriate output to Healthchecks.io. As the --send-http-report paramter, just point it to a Healthchecks Proxy with the appropriate check id.

For example

https://hcp.adinfo.qc.ca/duplicati/jdiesfofjehoefh

## Habitica

Habitica is a habit forming RPG ...


# Installation

The preferred solution to run Healthcheck Proxy is Docker.

    docker run -p 8000:8000 adenau/healthchecks-proxy

To deploy in Kubernetes, assuming your kubectl is properly configured, changed to the deploy directory and 

    kubectl --kubeconfig ~/.kube/kaon-kubeconfig.yaml create -f deployment.yml 
    kubectl --kubeconfig ~/.kube/kaon-kubeconfig.yaml create -f service-lb.yml 

Deployment was tested on Digital Ocean.

# Development

Clone the repository. Run the following to setup dependencies.

    pip install pipenv
    pipenv install

To run the program, change to the src directory and run the following

    pipenv run gunicorn --workers=2 --threads=4 --worker-class=gthread main:app
