# Django Backend Jenkins Lab

这是一个用于学习 Jenkins 的 Django 后端示例项目。

Jenkins 会从这个仓库拉取最新 `main` 分支代码，然后执行：

```text
Checkout Info -> Install -> Django Check -> Test -> Smoke Runserver -> Build Image -> Deploy -> Verify Deployment
```

本地运行：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Docker 部署：

```bash
docker compose -f deploy/docker-compose.yml -p jenkins-django-deploy up -d --build
curl http://localhost:8000/health/
```
