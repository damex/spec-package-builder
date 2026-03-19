# spec package builder

## Description

This repository contains spec files for building RPM packages.

It includes a `Makefile` that builds packages natively on `Red Hat Enterprise Linux` or its derivatives.

The `Makefile` accepts `SPEC_FILE` as a mandatory input, allowing you to specify the path to the spec file included in the `SPECS` directory.

Currently, packages and their corresponding spec files are built and tested only for `Red Hat Enterprise Linux 9`, `Red Hat Enterprise Linux 10` and its derivatives like `Alma Linux 9`, `Alma Linux 10`, `Rocky Linux 9` and `Rocky Linux 10`, as well as `Fedora 43`.

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

### Building Packages Inside Podman

To build packages inside a Podman container, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec build_in_podman
```

### Linting Spec Files Inside Podman

To lint spec files inside a Podman container, run the following command:

```sh
make SPEC_FILE=SPECS/my.spec lint_in_podman
```

## Using prebuilt packages

### Add damex-kubernetes repository with prebuilt packages

To add `damex-kubernetes` repository to `Red Hat Enterprise Linux 9` install the following package:

```sh
# x86_64
https://yum-repositories.damex.org/kubernetes/el/9/x86_64/damex-kubernetes-release-0.2.0-1.el9.x86_64.rpm
# aarch64
https://yum-repositories.damex.org/kubernetes/el/9/aarch64/damex-kubernetes-release-0.2.0-1.el9.aarch64.rpm
```

To add `damex-kubernetes` repository to `Red Hat Enterprise Linux 10` install the following package:

```sh
# x86_64
https://yum-repositories.damex.org/kubernetes/el/10/x86_64/damex-kubernetes-release-0.2.0-1.el10.x86_64.rpm
# aarch64
https://yum-repositories.damex.org/kubernetes/el/10/aarch64/damex-kubernetes-release-0.2.0-1.el10.aarch64.rpm
```

Alternatively, it can be done manually by adding the following configuration to `/etc/yum.repos.d/damex-kubernetes.repo`:

```sh
[damex-kubernetes]
name = damex-kubernetes
baseurl = https://yum-repositories.damex.org/kubernetes/el/$releasever/$basearch
gpgcheck = 1
gpgkey = https://yum-repositories.damex.org/kubernetes/yum-repositories-2035-11-30.asc
```

### Add damex-prometheus repository with prebuilt packages

To add `damex-prometheus` repository to `Red Hat Enterprise Linux 9` install the following package:

```sh
# x86_64
https://yum-repositories.damex.org/prometheus/el/9/x86_64/damex-prometheus-release-0.2.0-1.el9.x86_64.rpm
# aarch64
https://yum-repositories.damex.org/prometheus/el/9/aarch64/damex-prometheus-release-0.2.0-1.el9.aarch64.rpm
```

To add `damex-prometheus` repository to `Red Hat Enterprise Linux 10` install the following package:

```sh
# x86_64
https://yum-repositories.damex.org/prometheus/el/10/x86_64/damex-prometheus-release-0.2.0-1.el10.x86_64.rpm
# aarch64
https://yum-repositories.damex.org/prometheus/el/10/aarch64/damex-prometheus-release-0.2.0-1.el10.aarch64.rpm
```

Alternatively, it can be done manually by adding the following configuration to `/etc/yum.repos.d/damex-prometheus.repo`:

```sh
[damex-prometheus]
name = damex-prometheus
baseurl = https://yum-repositories.damex.org/prometheus/el/$releasever/$basearch
gpgcheck = 1
gpgkey = https://yum-repositories.damex.org/prometheus/yum-repositories-2035-11-30.asc
```

### Add damex-incus repository with prebuilt packages

To add `damex-incus` repository to `Fedora 43` install the following package:

```sh
# x86_64
https://yum-repositories.damex.org/incus/fc/43/x86_64/damex-incus-release-0.1.1-1.fc43.x86_64.rpm
# aarch64
https://yum-repositories.damex.org/incus/fc/43/aarch64/damex-incus-release-0.1.1-1.fc43.aarch64.rpm
```

Alternatively, it can be done manually by adding the following configuration to `/etc/yum.repos.d/damex-incus.repo`:

```sh
[damex-incus]
name = damex-incus
baseurl = https://yum-repositories.damex.org/incus/fc/43/$basearch
gpgcheck = 1
gpgkey = https://yum-repositories.damex.org/incus/yum-repositories-2035-11-30.asc
```

### List of prebuilt packages

| Package              | Repository | Architecture | Distributives              |
|----------------------|------------|--------------|----------------------------|
| cni-plugins          | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| cni-plugins-ipam     | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| cni-plugins-main     | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| cni-plugins-meta     | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd                 | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-benchmark       | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-dump-db         | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-dump-logs       | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-dump-metrics    | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-etcdctl         | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| etcd-etcdutil        | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| helm                 | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kube-apiserver       | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kube-controller-manager | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kube-proxy           | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kube-router          | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kube-scheduler       | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kubectl              | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kubectl-convert      | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kubelet              | damex-kubernetes | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| alertmanager           | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| alertmanager-amtool    | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| blackbox-exporter      | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| kafka-exporter         | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| node-exporter          | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| postgresql-exporter    | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| prometheus             | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| prometheus-promtool    | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| rsyslog-exporter       | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| smartctl-exporter      | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| systemd-exporter       | damex-prometheus | x86_64, aarch64 | Red Hat Enterprise Linux 9, Red Hat Enterprise Linux 10|
| incus                  | damex-incus | x86_64, aarch64 | Fedora 43 |
| incus-agent            | damex-incus | x86_64, aarch64 | Fedora 43 |
| incus-client           | damex-incus | x86_64, aarch64 | Fedora 43 |
| incus-tools            | damex-incus | x86_64, aarch64 | Fedora 43 |
