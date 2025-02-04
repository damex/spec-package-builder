# spec package builder

## Description

This repository contains spec files for building RPM packages.

It includes a `Makefile` that builds packages natively on `Red Hat Linux` or its derivatives.

The `Makefile` accepts `SPEC_FILE` as a mandatory input, allowing you to specify the path to the spec file included in the `SPECS` directory.

[Follow here if you want to build packages yourself](#Usage).

[Follow here if you want to use prebuilt packages](#Using-prebuilt-packages).

## Usage

### Building Packages

To build packages natively on your system, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec build
```

### Linting Spec Files

To lint spec files natively on your system, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec lint
```

### Building Packages Inside Docker

To build packages inside a Docker container, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec build_in_docker
```

### Linting Spec Files Inside Docker

To lint spec files inside a Docker container, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec lint_in_docker
```

## Using prebuilt packages

### Add damex-kubernetes repository with prebuilt packages

To add `damex-kubernetes` repository install the following package:

```sh
https://yum-repositories.damex.org/kubernetes/el/9/x86_64/damex-kubernetes-release-0.1.0-1.el9.x86_64.rpm
```

Alternatively, it can be done manually by adding the following configuration to `/etc/yum.repos.d/damex-kubernetes.repo`:

```sh
[damex-kubernetes]
name = damex-kubernetes
baseurl = https://yum-repositories.damex.org/kubernetes/el/9/x86_64
gpgcheck = 0
```

### Add damex-prometheus repository with prebuilt packages

To add `damex-prometheus` repository install the following package:

```sh
https://yum-repositories.damex.org/prometheus/el/9/x86_64/damex-prometheus-release-0.1.0-1.el9.x86_64.rpm
```

Alternatively, it can be done manually by adding the following configuration to `/etc/yum.repos.d/damex-prometheus.repo`:

```sh
[damex-prometheus]
name = damex-prometheus
baseurl = https://yum-repositories.damex.org/prometheus/el/9/x86_64
gpgcheck = 0
```

### List of prebuilt packages

| Package              | Repository | Architecture | Distributive              |
|----------------------|------------|--------------|---------------------------|
| cni-plugins          | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-ipam     | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-main     | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-meta     | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins          | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd                 | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-benchmark       | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-db         | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-logs       | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-metrics    | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-etcdctl         | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-etcdutil        | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| helm                 | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-apiserver       | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-controller-manager | damex-kubernetes | x86_64   | Red Hat Enterprise Linux 9|
| kube-proxy           | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-router          | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-scheduler       | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubectl              | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubectl-convert      | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubelet              | damex-kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| alertmanager           | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| alertmanager-amtool    | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| blackbox-exporter      | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| node-exporter          | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| postgresql-exporter    | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| prometheus             | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| prometheus-promtool    | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| smartctl-exporter      | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
| systemd-exporter       | damex-prometheus | x86_64       | Red Hat Enterprise Linux 9|
