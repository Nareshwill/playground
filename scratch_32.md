# Installing Node Using the Node Version Manager (NVM)

> An alternative for installing Node.js is to use a tool called `nvm`, 
> the Node Version Manager (NVM). Rather than working at the operating 
> system level, `nvm` works at the level of an independent directory within your home directory. 
> This means that you can install multiple self-contained versions of Node.js without affecting the entire system.

> Controlling your environment with `nvm` allows you to access the newest versions of Node.js 
> and retain and manage previous releases. It is a different utility from `apt`, however, and 
> the versions of Node.js that you manage with it are distinct from the versions you manage with `apt`.

---

#### This installs the nvm script to your user account.

```shell
    kpit@L-9088:~$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

#### In order to use it, first source the .bashrc file:

```shell
    kpit@L-9088:~$ source ~/.bashrc
```

#### Checking the installation version of `nvm` & `Output`
```shell
    kpit@L-9088:~$ nvm -v
    0.39.1
```

### For our application use, Our target version is `v14`

### Install Node v14 using `nvm`
```shell
    kpit@L-9088:~$ nvm install 14
    Downloading and installing node v14.19.0...
    Downloading https://nodejs.org/dist/v14.19.0/node-v14.19.0-linux-x64.tar.xz...
    ####################################################################################################################################### 100.0%
    Computing checksum with sha256sum
    Checksums matched!
    Now using node v14.19.0 (npm v6.14.16)
```

### Use the installed Node v14 using `nvm`
```shell
    kpit@L-9088:~$ nvm use 14
    Now using node v14.19.0 (npm v6.14.16)
```

### Check your `node` and `nvm` version
```shell
    kpit@L-9088:~$ node -v
    v14.19.0
    kpit@L-9088:~$ npm -v
    6.14.16
```