# Remote Tester (Demo)

## Introduction

A simple server to simulate some reference programs that may not run on a different software version.

For example, if you use a different version of python to run a `.pyc` file, you may receive "bad magic number" error.

```
RuntimeError: Bad magic number in .pyc file
```

The remote tester sets up a small service (handles concurrent ) on a server so programmers can run the reference program remotely. You may use `nc` to access the server.

```shell
nc {server_ip} 233 < testcase.txt
```

This demo is written for ShanghaiTech SI100C, which requires python3.5.2 to run the reference program.

## Deployment

### Native

Install the specific version of program (like python3.5.2).

```shell
python3 server.py
```

You can recieve log from both screen and log file.

### Docker

No need to install the specific version of program. Install docker, then:

```shell
docker build -t remote-tester .
docker run -d -p 23:23 -p 233:233 {-p host_port:docker_port...} -v {logfile_location}:/server/logs remote-tester
```

Screen logging does not work right, use log file to check the connection info.

## TODO

- [ ] Use iptables to get the real ip after forwarded by docker.
- [ ] Specific different Exception types.

## More

Bug and security reports are welcomed. GLHF. : )