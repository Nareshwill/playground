# How to Set up RabbitMq in Ubuntu 18.04 LTS

### Prerequisite
* Ubuntu 18.04 LTS

#### RabbitMQ is an open source message broker software that implements the Advanced Message Queuing Protocol (AMQP) and Streaming Text Oriented Messaging Protocol, Message Queuing Telemetry Transport, and other protocols via a Plugins.
#### The work of a Messaging broker is to receive messages from publishers (applications that publish them) and route them to consumers (applications that process them). AMQP is a messaging protocol that enables conforming client applications to communicate with conforming messaging middleware brokers.

### Follow the steps below to install RabbitMQ Server on Ubuntu 18.04 LTS

## Step 1: Install Erlang
#### RabbitMQ requires Erlang to be installed first before it can run. Install Erlang on Ubuntu 18.04 LTS

## Step 1.1: Import Erlang GPG Key
#### Run the following commands to import Erlang repository GPG key:

```commandline
    sudo apt update
    sudo apt install curl software-properties-common apt-transport-https lsb-release
    curl -fsSL https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/erlang.gpg
```

## Step 1.2: Add Erlang Repository to Ubuntu 18.04 LTS

```commandline
    echo "deb https://packages.erlang-solutions.com/ubuntu $(lsb_release -cs) contrib" | sudo tee /etc/apt/sources.list.d/erlang.list
```

## Step 1.3: Install Erlang on Ubuntu 18.04 LTS
#### The last step is the actual installation of Erlang. Update your system package list and install Erlang:

```commandline
    sudo apt update
    sudo apt install erlang
```

#### After successful, installation of Erlang, We can start installing Rabbitmq in Ubuntu 18.04 LTS

## Step 2: Add RabbitMQ Repository to Ubuntu 18.04 LTS
#### Team RabbitMQ maintains an apt repository on PackageCloud, a package hosting service. It provides packages for most recent RabbitMQ releases.

#### Let’s add RabbitMQ Repository to our Ubuntu system.

```commandline
    curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.deb.sh | sudo bash
```

## Step 3: Install RabbitMQ Server Ubuntu 18.04 LTS
```commandline
    sudo apt update
```
#### Then install rabbitmq-server package:

```commandline
    sudo apt install rabbitmq-server
```

## After installation, RabbitMQ service is started and enabled to start on boot. To check the status, run:
```commandline
    ● rabbitmq-server.service - RabbitMQ broker
       Loaded: loaded (/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: enabled)
       Active: active (running) since Wed 2022-05-18 11:00:51 IST; 59min ago
     Main PID: 20699 (beam.smp)
        Tasks: 32 (limit: 4915)
       CGroup: /system.slice/rabbitmq-server.service
               ├─20699 /usr/lib/erlang/erts-12.3.1/bin/beam.smp -W w -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs 512 -MMmcs 30 -P 1048576 
               ├─20712 erl_child_setup 32768
               ├─20747 /usr/lib/erlang/erts-12.3.1/bin/epmd -daemon
               ├─20778 inet_gethost 4
               └─20779 inet_gethost 4
    
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Doc guides:  https://rabbitmq.com/documentation.html
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Support:     https://rabbitmq.com/contact.html
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Tutorials:   https://rabbitmq.com/getstarted.html
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Monitoring:  https://rabbitmq.com/monitoring.html
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Logs: /var/log/rabbitmq/rabbit@D-12149.log
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:         /var/log/rabbitmq/rabbit@D-12149_upgrade.log
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:         <stdout>
    May 18 11:00:46 D-12149 rabbitmq-server[20699]:   Config file(s): (none)
    May 18 11:00:51 D-12149 rabbitmq-server[20699]:   Starting broker... completed with 0 plugins.
    May 18 11:00:51 D-12149 systemd[1]: Started RabbitMQ broker.    
```

## After installation of Rabbitmq, You can view & manage the Rabbitmq management console by accessing `http://localhost:15672/`.
### The default username is: `guest` & password is: `guest`.

### If we are not able to access the above link, Please execute the below command.
```commandline
    sudo rabbitmq-plugins enable rabbitmq_management
```

## Be aware that the `guest` account can only connect via localhost

## To enable RabbitMQ admin management user please follow below steps.

### This adds a new user and password
```commandline
    sudo rabbitmqctl add_user <username> <password>
```
### This makes the user an administrator

```commandline
    sudo rabbitmqctl set_user_tags <username> administrator
```

### This sets permissions for the user

```commandline
    sudo rabbitmqctl set_permissions -p / <username> ".*" ".*" ".*"
```