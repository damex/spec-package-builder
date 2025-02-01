# spec package builder

## Description

This repository contains spec files for building RPM packages.

It includes a `Makefile` that builds packages natively on `Red Hat Linux` or its derivatives.

The `Makefile` accepts `SPEC_FILE` as a mandatory input, allowing you to specify the path to the spec file included in the `SPECS` directory.

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
