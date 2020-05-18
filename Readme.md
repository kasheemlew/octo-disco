## 用法

### 一次性运行

1. 安装 docker-compose
2. 配置 template.json 中的规则
3. 配置 settings.py 中的 MongoDB 参数，缺省状态下会使用 docker-compose 在 localhost:27017 创建的 MongoDB 容器
4. docker-compose up

### 开启持续后端服务

```bash
$ make server
```

## 运行测试

```bash
$ make test
```