# Knowledge sharing session pixi
This is the script of the knowledge sharing session about pixi. The session was held on 2024-10-10.

## Installation
Follow the [link](https://pixi.sh/latest/#installation). I install pixi from `pacman` (package manager in my distro). Also there are autocompletions for fish, zsh, ...

## Initialising a new project
```batch
pixi init tardigrade --format pyproject
cd tardigrade
```

```bash
pixi add python
```

```bash
pixi install 
```
## Investigate pyproject.toml
Note
- The project itself is an editable depdency.

We have pypi-dependencies and dependencies.

## Intermezzo: Abstractions in pixi

### Platforms
We can ensure that dependencies can be resolved on different platforms:
```yaml
platforms = ["win-64", "linux-64", "osx-64", "osx-arm64"]
```

There are also options to have target specifiers for specific platforms.
### Channels
e.g.
```yaml
channels = ["nvidia/label/cuda-12.1.0", "nvidia", "conda-forge", "pytorch"]
```
For each package we install, the channel can be defined. The list of channels is prioritised from first to last.
### Environment
Different environments can be used for different settings: different platforms, different python version / package versions, develop dependencies and without, environment for cuda.

### Features
Features describe parts of environments 
`default` sets the global dependencies , features set optional dependencies. A feature can be linked to an environment.

### Tasks
Tasks can replace things we do in Makefiles (compiling, testing, linting, ...)
Tasks also support dependencies, ...

### System requirements
e.g. require glibc, ...


## Coming from poetry
[Cheatsheet](https://pixi.sh/latest/switching_from/poetry/#quick-look-at-the-differences)
## Adding packages to a feature
A feature can contain collection of dependencies, tasks, channels ...

```bash
pixi add pytest ruff --feature dev
```

## Add an environment with the feature
Add an environment that contains the feature, solve-group decides which versions to pick from the shared ones.
```bash
pixi project environment add dev --feature dev --solve-group default
```

```bash
pixi install -e dev
```

Check what is installed and from where.
```shell
pixi list
```

```shell
pixi list -e dev
```

**Note**: We can have environments with different python versions.

## Add a task
```bash
pixi task add --feature dev run_tests "pytest -vv"
```

## Interoperability pypi and conda
pypi packages can depend on conda packages.

## Troubleshooting
If your environments do not work
```bash
rm -rf .pixi
```

Sometimes interoperability between conda and pypi does not entirely work. -> Install required packages from conda.

## Github Actions
Example
```yaml
- uses: prefix-dev/setup-pixi@v0.8.0
  with:
    pixi-version: v0.32.1
    cache: true
    auth-host: prefix.dev
    auth-token: ${{ secrets.PREFIX_DEV_TOKEN }}
- run: pixi run test
```

Compare [docs](https://pixi.sh/latest/advanced/github_actions/)

## Containerise with pixi
Example
```python
FROM ghcr.io/prefix-dev/pixi:0.32.1 AS build

# copy source code, pixi.toml and pixi.lock to the container
WORKDIR /app
COPY . .

# install dependencies to `/app/.pixi/envs/prod`
# use `--locked` to ensure the lockfile is up to date with pixi.toml
RUN pixi install --locked -e prod

# create the shell-hook bash script to activate the environment
RUN pixi shell-hook -e prod -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint.sh
RUN cat /shell-hook >> /app/entrypoint.sh

# extend the shell-hook script to run the command passed to the container
RUN echo 'exec "$@"' >> /app/entrypoint.sh

FROM ubuntu:24.04 AS production
WORKDIR /app

# only copy the production environment into prod container
# please note that the "prefix" (path) needs to stay the same as in the build container
COPY --from=build /app/.pixi/envs/prod /app/.pixi/envs/prod
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh

# copy your project code into the container as well
COPY ./my_project /app/my_project

EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]

# run your app inside the pixi environment

CMD [ "uvicorn", "my_project:app", "--host", "0.0.0.0" ]
```


## Migrating from poetry
Put the dependencies into pypi dependencies and adjust the format or reinstall all dependencies from scratch (recommended).