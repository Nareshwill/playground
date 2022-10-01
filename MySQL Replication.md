# How to configure MySQL Master-Slave Replication on Ubuntu 18.04

> MySQL replication is a process that allows data from one database server to be automatically 
> copied to one or more servers.

> MySQL supports a number of replication topologies with Master/Slave topology being one of the 
> most well-known topologies in which one database server acts as the master, while one or more servers act as slaves.
> By default, the replication is asynchronous where the master sends events that describe database modifications to its
> binary log and slaves request the events when they are ready.

> This document covers a basic example of MySQL Master/Slave replication with one master and one slave server on Ubuntu 18.04.

## Prerequisite
> This example assumes you have two servers running Ubuntu 18.04, which can communicate with each other over a private network.

#### This example contains following server IP's
> Master IP: 10.0.201.32
> 
> Slave IP: 10.0.3.184


## Install MySQL

```shell
    master@ubuntu:~$ sudo apt-get update
    master@ubuntu:~$ sudo apt-get install mysql-server
```

### Install MySQL on the Slave server using the same commands:

```shell
    slave@ubuntu:~$ sudo apt-get update
    slave@ubuntu:~$ sudo apt-get install mysql-server
```

## Configure Firewall on `master` & `slave`:
#### In `master`
```shell
    master@ubuntu:~$ sudo ufw allow 3306/tcp
```

#### In `slave` as well
```shell
    slave@ubuntu:~$ sudo ufw allow 3306/tcp
```

#### Create a mysql user `replicauser` on `master`:
```shell
    master@ubuntu:~$ sudo mysql
    mysql> CREATE USER 'replicauser'@'10.0.201.32' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'replicauser'@'10.0.201.32';
    mysql> FLUSH PRIVILEGES; 
```

## Configure the Master Server
#### The first step is to configure the master MySQL server. We’ll make the following changes:
* Create a mysql user
* Set the MySQL server to listen on the private IP.
* Set a unique server ID.
* Enable the binary logging

#### To do so open the MySQL configuration file and uncomment or set the following:

```shell
    master@ubuntu:~$ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

```shell
    master: /etc/mysql/mysql.conf.d/mysqld.cnf
    bind-address           = 10.0.201.32
    server-id              = 1
    log_bin                = /var/log/mysql/mysql-bin.log
```

#### Once done, restart the MySQL service for changes to take effect:

```shell
    master@ubuntu:~$ sudo systemctl restart mysql
```

#### The next step is to create a new replication user. Log in to the MySQL server as the root user by typing:

```shell
    master@ubuntu:~$ sudo mysql
```

#### From inside the MySQL prompt, run the following SQL queries that will create the replica user `replicauser` and grant the `REPLICATION SLAVE` privilege to the user:

> Make sure you change the IP with your slave IP address. You can name the user as you want.

```shell
    mysql> CREATE USER 'replicauser'@'10.0.3.184' IDENTIFIED BY 'replica_password';
```

> Make sure you change the IP with your slave IP address. You can name the user as you want.

```shell
    mysql> GRANT REPLICATION SLAVE ON *.* TO 'replicauser'@'10.0.3.184';
```

#### While still inside the MySQL prompt, execute the following command that will print the binary filename and position.

```shell
    mysql> SHOW MASTER STATUS\G
```

```shell
    Output
    *************************** 1. row ***************************
                 File: mysql-bin.000001
             Position: 629
         Binlog_Do_DB: 
     Binlog_Ignore_DB: 
    Executed_Gtid_Set: 
    1 row in set (0.00 sec)
```

#### Take note of file name, `mysql-bin.000001` and Position `629`. You'll need these values when configuring the slave server. These values will probably be different on your server.

## Configure the Slave Server

#### Like for the `master` server above, we’ll make the following changes to the `slave` server:
* Set the MySQL server to listen on the private IP
* Set a unique server ID
* Enable the binary logging

#### Open the MySQL configuration file and edit the following lines:
```shell
    slave@ubuntu:~$ sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

```shell
    slave:/etc/mysql/mysql.conf.d/mysqld.cnf
    bind-address           = 10.0.3.184
    server-id              = 2
    log_bin                = /var/log/mysql/mysql-bin.log
```

#### Restart the MySQL service:

```shell
    slave@ubuntu:~$ sudo systemctl restart mysql
```

#### The next step is to configure the parameters that the slave server will use to connect to the master server. Login to the MySQL shell:

```shell
    slave@ubuntu:~$ sudo mysql
```

#### First, stop the slave threads:

```shell
    mysql> STOP SLAVE;
```

#### Run the following query that will set up the `slave` to replicate the `master`:
```shell
    mysql> CHANGE MASTER TO
    mysql> MASTER_HOST='10.0.201.32',
    mysql> MASTER_USER='replicauser',
    mysql> MASTER_PASSWORD='password',
    mysql> MASTER_LOG_FILE='mysql-bin.000001',
    mysql> MASTER_LOG_POS=629;
```

#### Make sure you are using the correct IP address, user name, and password. The log file name and position must be the same as the values you obtained from the master server.

#### Once done, start the slave threads.
```shell
    mysql> START SLAVE;
```

## Test the Configuration

#### At this point, you should have a working Master/Slave replication setup.
#### To verify that everything works as expected, we’ll create a new database on the `master` server:

```shell
    master@ubuntu:~$ mysql -u replicauser -p
```

```shell
    mysql> CREATE DATABASE test;
```

#### Login to the `slave` MySQL shell:
```shell
    slave@ubuntu:~$ sudo mysql
```

#### Run the following command to list all databases:
```shell
    mysql> SHOW DATABASES;
```

#### You will notice that the database you created on the master server is replicated on the slave:
```shell
    Output
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | test               |
    | sys                |
    +--------------------+
    5 rows in set (0.00 sec)
```

## References
> https://linuxize.com/post/how-to-configure-mysql-master-slave-replication-on-ubuntu-18-04/
> 
> https://linuxize.com/post/how-to-create-mysql-user-accounts-and-grant-privileges/