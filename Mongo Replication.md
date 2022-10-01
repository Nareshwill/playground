
# How to Configure a MongoDB Replica Set on Ubuntu 18.04 LTS

### Introduction

> When working with databases, it’s often useful to have multiple copies of your data. 
> This provides redundancy in case one of the database servers fails and can improve a database’s availability and scalability, as well as reduce read latencies. 
> The practice of synchronizing data across multiple separate databases is called replication. 
> In MongoDB, a group of servers that maintain the same data set through replication are referred to as a replica set.

> This document provides a brief overview of how replication works in MongoDB and outlines how to configure and initiate a replica set with three members. 
> In this example configuration, each member of the replica set will be a distinct MongoDB instance running on separate Ubuntu 18.04 servers. 

### Prerequisites

* Three servers,  each running Ubuntu 18.04. All three of these servers should have a non-root administrative user and a firewall configured with UFW.

* MongoDB 4.4.2 installed on each of your Ubuntu servers.

##### I have taken these following three servers into consideration as mongo0, mongo1 & mongo2

---

```shell
    bryant@mongo0:~$
```

---

```shell
    bryant@mongo1:~$
```

---

```shell
    bryant@mongo2:~$
```

---

## Step 1 - Configuring DNS Resolution

> When it comes time to initialize your replica set, you'll need to provide an address where each replica set member
> can be reached by the other two in the set.


> The MongoDB documentation recommends against using IP addresses when configuring a replica set, since IP addresses can
> change unexpectedly. Instead, MongoDB recommends using logical DNS hostnames when configuring replica sets.

```shell
    sudo nano /etc/hosts
```

```shell
    Ip_address host_name
```

#### Below are the hostnames, the above three servers will use throughout this guide.

> mongo0
> 
> mongo1
> 
> mongo2

#### Using these hostnames, your `/etc/hosts` files would look similar to the following lines
#### `/etc/hosts`

```shell
    bryant@mongo0~$: sudo nano /etc/hosts
    127.0.0.1 localhost
    
    10.0.201.32 mongo0
    10.0.3.184 mongo1
    10.0.211.61 mongo2
```

#### Save and close the file on each of your servers.

```shell
    bryant@mongo1~$: sudo nano /etc/hosts
    127.0.0.1 localhost
    
    10.0.201.32 mongo0
    10.0.3.184 mongo1
    10.0.211.61 mongo2
```

```shell
    bryant@mongo2~$: sudo nano /etc/hosts
    127.0.0.1 localhost
    
    10.0.201.32 mongo0
    10.0.3.184 mongo1
    10.0.211.61 mongo2
```

## Step 2 - Updating Each Server's Firewall Configurations with UFW.

> Assuming you have already set up a firewall on each of the servers on
> which you've installed MongoDB and enabled access for the OpenSSH UFW profile.
> However, these firewalls will also block the MongoDB instances on each server from communicating
> with one another, preventing you from initiating the replica set.


> To correct this, you'll need to add new firewall rules to allow each server access to the port
> on the other two servers on which MongoDB is listening for connections.


#### On `mongo0`, run the following `ufw` command to allow `mongo1` access to port `27017` on `mongo0`

```shell
    bryant@mongo0:~$ sudo ufw allow from mongo1_server_ip to any port 27017
```

#### Then add another firewall rule to give `mongo2` access to the same port:

```shell
    bryant@mongo0:~$ sudo ufw allow from mongo2_server_ip to any port 27017
```

#### Next, update the firewall rules for your other two servers. Run the following commands on `mongo1`, 
#### making sure to change the IP addresses to reflect those of `mongo0` and `mongo2`, respectively:

```shell
    bryant@mongo1:~$ sudo ufw allow from mongo0_server_ip to any port 27017
    bryant@mongo1:~$ sudo ufw allow from mongo2_server_ip to any port 27017
```

#### Lastly, run these two commands on mongo2. Again, be sure that you enter the correct IP addresses for each server:

```shell
    bryant@mongo2:~$ sudo ufw allow from mongo0_server_ip to any port 27017
    bryant@mongo2:~$ sudo ufw allow from mongo1_server_ip to any port 27017
```

#### After adding these UFW rules, each of your three MongoDB servers will be allowed to access the port used by MongoDB on the other two servers.

## Step 3 - Enabling Replication in Each Server's MongoDB Configuration File.

#### On `mongo0` m/c

```shell
    bryant@mongo0:~$ sudo nano /etc/mongod.conf
    . . .
    # network interfaces
    net:
      port: 27017
      bindIp: 127.0.0.1,10.0.201.32
    . . .
    replication:
      replSetName: "rs0"
    . . . 
```

#### On `mongo1` m/c

```shell
    bryant@mongo1:~$ sudo nano /etc/mongod.conf
    . . .
    # network interfaces
    net:
      port: 27017
      bindIp: 127.0.0.1,10.0.3.184
    . . .
    replication:
      replSetName: "rs0"
    . . . 
```

#### On `mongo2` m/c

```shell
    bryant@mongo2:~$ sudo nano /etc/mongod.conf
    . . .
    # network interfaces
    net:
      port: 27017
      bindIp: 127.0.0.1,10.0.211.61
    . . .
    replication:
      replSetName: "rs0"
    . . . 
```

#### After making these changes to each server’s mongod.conf file, save and close each file. Then, restart the mongod service on each server by issuing the following command:

```shell
    sudo systemctl restart mongod
```

## Step 4 - Starting the Replica Set & Adding Members

#### Now that you’ve configured each of your three MongoDB installations, you can open up a MongoDB shell to initiate replication and add each as a member.
### On `mongo0`, open up the MongoDB shell:
```shell
    bryant@mongo0:~$ mongo
    > rs.initiate(
    ... {
    ... _id: "rs0",
    ... members: [
    ... { _id: 0, host: "10.0.201.32:27017" },
    ... { _id: 1, host: "10.0.3.184:27017" },
    ... { _id: 2, host: "10.0.211.61:27017" }
    ... ]
    ... })
```

#### Assuming that you entered all the details correctly, once you press `ENTER` after typing the closing parenthesis the method will run and initiate the replica set. If the method returns `"ok" : 1` in the output, it means that the replica set was started correctly:

```shell
    Output
    {
        "ok" : 1,
        "$clusterTime" : {
            "clusterTime" : Timestamp(1612389071, 1),
            "signature" : {
                "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                "keyId" : NumberLong(0)
            }
        },
        "operationTime" : Timestamp(1612389071, 1)
    }
```

## References.

> Setup Replication Deployment(Production)
> 
> https://docs.mongodb.com/v4.4/tutorial/deploy-replica-set/
> 
> https://www.digitalocean.com/community/tutorials/how-to-configure-a-mongodb-replica-set-on-ubuntu-20-04
> 
> https://docs.mongodb.com/manual/tutorial/deploy-replica-set-with-keyfile-access-control/
 

> Testing the connection
> 
> https://docs.mongodb.com/v4.4/tutorial/troubleshoot-replica-sets/#std-label-replica-set-troubleshooting-check-connection

> Add replica member
> 
> https://docs.mongodb.com/manual/reference/method/rs.add/

> Remove member from replica
> 
> https://docs.mongodb.com/manual/reference/method/rs.remove/

> Replica ids do not match
> 
> https://stackoverflow.com/questions/65243421/mongodb-replica-set-ids-do-not-match 

> If replication state is OTHER 
> 
> https://stackoverflow.com/questions/47439781/mongodb-replica-set-member-state-is-other

> Either all host names in a replica set configuration must be localhost references, or none must be; found 1 out of 2
> 
> https://www.mongodb.com/community/forums/t/either-all-host-names-in-a-replica-set-configuration-must-be-localhost-references-or-none-must-be-found-1-out-of-2/101636

> Uninstall mongodb from ubuntu
> 
> https://stackoverflow.com/questions/29554521/uninstall-mongodb-from-ubuntu
