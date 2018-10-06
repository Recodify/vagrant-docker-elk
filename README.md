# Provision Ubuntu 14.04LTS on Azure.

- specify username with no full stop 
- set password
- Open ports/endpoints: 

		TCP 15672 : Rabbit Management
		TCP 8080 : Rabbit Web
		TCP 5672 : AMPQ
		TCP 443 : HTTPS
		TCP 80 : HTTP
		TCP 9200 : ElasticSearch
		TCP 8000 : Kibana
		TCP 5601  : PassThru Kibana

- ssh hostname.cloudapp.net -l username

# Upgrade Docker 
		-- Update Kernal
		$ sudo service docker stop
		$ sudo apt-get update
		$ sudo apt-get install linux-image-generic-lts-trusty
		$ sudo reboot

		-- Install latest docker
		$ sudo apt-get update
		$ sudo apt-get install wget
		$ wget -qO- https://get.docker.com/ | sh

		-- Pull docker images
		$ sudo docker pull logstash
		$ sudo docker pull elasticsearch
		$ sudo docker pull kibana
		$ sudo docker pull rabbitmq
		-- Start RabbitMQ container
		$ sudo docker run -d --hostname inty-rabbit --name log-rabbit -p 8080:15672 -p 5672:5672 -e RABBITMQ_DEFAULT_USER=publisher -e RABBITMQ_DEFAULT_PASS=snowwhite  rabbitmq:3-management


# ELK playbook

A playbook to setup a simple ELK stack using Docker and point it at an existing Rabbit instance. The playbook treats the nginx/Kibana and Logstash/ElasticSearch part separately so that they can be installed on separate suitable machines (a Linux machine running Docker).

![ELK Layout](./artifacts/loyaltyElk.png)

Items in yellow are provisioned by this playbook.

## Requirements

You will need to have a machine running [Ansible] to provision the stack. Ansible only runs on Linux, this can be the same machine you are provisioning or a remote linux machine.

$ sudo apt-get update
$ sudo install ansible


## Configuring a new Instance

Each instance needs to have a small configuration set to describe the machine and some machine or environment specific information. This information can then be checked into source and managed as your infrastructure grows.

### Format

The host file follows the INI format:

```INI
[monitor]
<fqdn of the host here>

[store]
<fqdn of the host here>

[store:vars]
rabbitQueue=<your Rabbit queue name here>
rabbitHost=<Rabbit host fqdn>
rabbitExchange=<your Rabbit exchange name here>
```

The **monitor** group represents the location for nginx/Kibana, and **store** represents the location of Logstash/ElasticSearch. These can be the same machine. If they are separate, the host name of the **store** machine will be used by Kibana as the ElasticSeach address.

Create a new file and add the details that describe the environment you want to support. There are examples in **playbooks/hosts**.

### Using the File

The created file lives inside of the **playbook/hosts** folder and should be called something descriptive to identify the host. The name of this file can be passed to **provision.py** as described below.

## Running

You will need to create a host file for the environment you want to provision and place it in **playbooks/hosts**. You can then refer to the file when running the script:

```bash
$ python provision.py --hosts intylive
```

Ansible will do the rest.

If you need to supply a user to connect to the remote machine with, supply the **--u** argument along with the name of the remote user:

```bash
$ python provision.py --hosts inty-live --u remoteUser
```

You will asked for the users password if required. It's best to use a user where a trust relationship exists rather than supplying credentials.

## Testing Changes

Use the included Vagrantfile to create a test environment which includes Ansible and Docker. The project is mounted at **/playbook**. You can run the playbook via:

```bash
$ cd /playbook
$ python provision.py --hosts local
```