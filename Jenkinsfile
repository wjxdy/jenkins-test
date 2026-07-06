pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        APP_IMAGE = 'jenkins-django-backend:local'
        COMPOSE_PROJECT = 'jenkins-django-deploy'
        DEPLOY_HEALTH_URL = 'http://host.docker.internal:8000/health/'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Checkout Info') {
            steps {
                sh '''
                    set -eux
                    pwd
                    git rev-parse --short HEAD
                    git branch --show-current || true
                    ls -la
                '''
            }
        }

        stage('Install') {
            steps {
                sh '''
                    set -eux
                    rm -rf .venv
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Django Check') {
            steps {
                sh '''
                    set -eux
                    . .venv/bin/activate
                    python manage.py check
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -eux
                    . .venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Smoke Runserver') {
            steps {
                sh '''
                    set -eux
                    . .venv/bin/activate
                    python manage.py runserver 127.0.0.1:8000 > /tmp/django-runserver.log 2>&1 &
                    SERVER_PID=$!
                    cleanup() {
                        kill "$SERVER_PID" >/dev/null 2>&1 || true
                        wait "$SERVER_PID" >/dev/null 2>&1 || true
                        cat /tmp/django-runserver.log || true
                    }
                    trap cleanup EXIT

                    for i in $(seq 1 30); do
                        python3 - <<'PY' && exit 0 || true
import json
import urllib.request

with urllib.request.urlopen('http://127.0.0.1:8000/health/', timeout=2) as response:
    body = json.loads(response.read().decode('utf-8'))
    assert body == {'status': 'ok'}, body
PY
                        sleep 1
                    done

                    exit 1
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    set -eux
                    docker compose -f deploy/docker-compose.yml -p "$COMPOSE_PROJECT" build
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eux
                    docker compose -f deploy/docker-compose.yml -p "$COMPOSE_PROJECT" up -d
                    docker compose -f deploy/docker-compose.yml -p "$COMPOSE_PROJECT" ps
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eux
                    for i in $(seq 1 30); do
                        python3 - <<'PY' && exit 0 || true
import json
import os
import urllib.request

url = os.environ['DEPLOY_HEALTH_URL']
with urllib.request.urlopen(url, timeout=2) as response:
    body = json.loads(response.read().decode('utf-8'))
    assert body == {'status': 'ok'}, body
PY
                        sleep 1
                    done

                    docker logs django-backend-lab-app || true
                    exit 1
                '''
            }
        }
    }
}
