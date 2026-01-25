# Week 1 — Docker & Terraform  
*Data Engineering Zoomcamp — Module 01*  
Focus: Containerization with Docker, running services, and IaC with Terraform.:contentReference[oaicite:1]{index=1}

---

## 1. Goals of Week 1

**Primary objectives:**

- Understand containerization with Docker.
- Build, run, and manage Docker images and containers.
- Use `docker-compose` for multi‑container setups.
- Run PostgreSQL and pgAdmin in containers.
- Get familiar with Terraform for Infrastructure as Code (IaC).
- Prepare the environment for later modules.:contentReference[oaicite:2]{index=2}

---

## 2. Docker Fundamentals

### 2.1 What is Docker?

Docker is a platform for packaging applications and their dependencies into isolated units called _containers_.  
Containers run consistently across environments (local dev, staging, CI/CD, production).

**Benefits:**
- Repeatable environments
- Dependency isolation
- Rapid service setup

---

### 2.2 Dockerfile Structure

Example of typical Dockerfile sections:

```
# Base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Define default command
CMD ["python", "main.py"]
```

**Key Dockerfile instructions:**
- `FROM`: base image
- `WORKDIR`: working directory
- `COPY`: copy files into image
- `RUN`: commands during image build
- `CMD`: default command when container starts

---

## 3. Running Containers

### 3.1 Basic Commands

Build and run a simple image:

```
docker build -t myapp .
docker run --name myapp-instance -d myapp
```

List containers and images:

```
docker ps
docker images
```

Stop/remove containers:

```
docker stop myapp-instance
docker rm myapp-instance
```

---

## 4. Docker Compose (Multi‑Container)

/docker‑compose.yaml/ allows defining multiple services (e.g., Postgres + application).

**Example service network diagram:**

```
[ local machine ]
        |
  -------------
  |     |     |
[app][postgres][pgadmin]
     \    |    /
      \   |   /
       \  |  /
     [bridge network]
```

**docker‑compose.yml skeleton:**

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@domain.com
      PGADMIN_DEFAULT_PASSWORD: secret
    ports:
      - "8080:80"
```

**Commands:**
```
docker compose up -d
docker compose down
```

---

## 5. PostgreSQL + pgAdmin Setup (in Docker)

- A PostgreSQL container serves as the database backend.
- A pgAdmin container provides a GUI for database management.
- These services communicate via a shared Docker network created automatically by Compose.

After starting them, you can:
- Connect to Postgres from pgAdmin.
- Create tables and run SQL queries.
- Explore data for Zoomcamp homework tasks.

---

## 6. Terraform Basics (Infrastructure as Code)

Terraform lets you define cloud infrastructure declaratively.

**Core concepts:**
```
Terraform config files (.tf)
      │
      ▼
terraform init        # setup providers
terraform plan        # preview changes
terraform apply       # create/update infra
terraform destroy     # teardown
```

- `provider`: cloud API interface
- `resource`: cloud object (bucket, VM, dataset)
- Terraform maintains a *state* file tracking resources.

**Typical workflow:**
```
terraform init
terraform plan
terraform apply -auto-approve
```

---

## 7. Typical Homework Flow (Week 1)

1. **Docker tasks:**
   - Build custom images.
   - Start multi‑service applications.
   - Use SQL via pgAdmin or CLI.
2. **SQL refresher:**
   - Query data inside Postgres (grouping, filtering).
3. **Terraform homework (GCP):**
   - Initialize workspace.
   - Create cloud resources (e.g., storage bucket, dataset).
   - Apply and destroy infra.:contentReference[oaicite:3]{index=3}

---

## 8. Summary of Artefacts Created

```
# Local environment
Dockerfile
docker-compose.yaml

# Containers
app container
postgres container
pgAdmin container

# Terraform
main.tf
variables.tf
terraform.tfstate
```

---

## 9. Suggested Next Steps

- Review Docker CLI commands.
- Practice writing and customizing Dockerfiles.
- Explore Terraform provider docs (Google, AWS, Azure).
- Confirm cloud account access (credits, IAM roles).

---

## References

Course and module structure details from DataTalksClub Zoomcamp syllabus.:contentReference[oaicite:4]{index=4}

