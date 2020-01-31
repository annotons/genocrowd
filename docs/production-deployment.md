In production, Genocrowd is deployed with docker and docker-compose. We provide `docker-compose.yml` templates to deploy your instance.

# Prerequisites

Install `git`

```bash
# Debian/Ubuntu
apt install -y git
# Fedora
dnf install -y git
```

Install `docker`:

- [Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
- [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Fedora](https://docs.docker.com/install/linux/docker-ce/fedora/)

Install `docker-compose`:

```bash
# Debian/Ubuntu
apt install -y docker-compose
# Fedora
dnf install -y docker-compose
```

# Deploy

## Download templates

First, clone the [genocrowd-docker-compose](https://github.com/annotons/genocrowd-docker-compose) repository. It contain template files to deploy your Genocrowd instance.


```bash
git clone https://github.com/annotons/genocrowd-docker-compose.git
```

This repo contains several directories, depending on your needs

```bash
cd genocrowd-docker-compose
ls -1
```

Two directories are used for production deployment

- `standalone`: deploy Genocrowd with all its dependencies for a standalone usage
- `federated`: deploy Genocrowd with all its dependencies for a federated usage (Ask external endpoint such as [NeXtProt](https://sparql.nextprot.org))

Choose one of this directory depending of your needs

```bash
cd federated
```
## Configure

First, edit the `docker-compose.yml` file. You can change the following entries:

- `services` > `genocrowd` > `image`: Use the [latest](https://github.com/annotons/genocrowd/releases/latest) image tag. Example: `annotons/genocrowd:3.2.5`
- `services` > `nginx` > `ports`: You can change the default port if `80` is already used on your machine. Example: `"8080:80"`

### Nginx (web proxy)

Nginx is used to manage web redirection. Nginx configuration is in two files: `nginx.conf` and `nginx.env`. If you want to access the virtuoso endpoint, uncomment the `virtuoso` section in `nginx.conf`


### Genocrowd

For more information about Genocrowd configuration, see [configuration](configure.md) section.
