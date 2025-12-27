# Docker Setup Guide

## Start Docker Service for Airflow

### 1. Create Airflow Directories and Environment File

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### 2. Initialize the Database

Run database migrations and create the first user account:

```bash
docker compose up airflow-init
```

**Wait for initialization to complete.** You should see:
```
airflow-init-1 exited with code 0
```

### 3. Clean Up the Environment

To remove all Airflow containers and volumes:

```bash
docker compose down --volumes --remove-orphans
```