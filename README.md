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

### List of prebuilt packages

| Package              | Repository | Architecture | Distributive              |
|----------------------|------------|--------------|---------------------------|
| cni-plugins          | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-ipam     | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-main     | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins-meta     | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| cni-plugins          | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd                 | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-benchmark       | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-db         | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-logs       | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-dump-metrics    | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-etcdctl         | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| etcd-etcdutil        | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| helm                 | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-apiserver       | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-controller-manager | kubernetes | x86_64   | Red Hat Enterprise Linux 9|
| kube-proxy           | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-router          | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kube-scheduler       | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubectl              | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubectl-convert      | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| kubelet              | kubernetes | x86_64       | Red Hat Enterprise Linux 9|
| alertmanager           | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| alertmanager-amtool    | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| blackbox-exporter      | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| node-exporter          | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| postgresql-exporter    | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| prometheus             | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| prometheus-promtool    | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| smartctl-exporter      | prometheus | x86_64       | Red Hat Enterprise Linux 9|
| systemd-exporter       | prometheus | x86_64       | Red Hat Enterprise Linux 9|
