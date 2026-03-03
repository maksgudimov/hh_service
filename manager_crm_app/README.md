# Генерация ключей

```shell
Создаем дирректорию certs. Все ключи лежат в ней
mkdir ./certs
```

```shell
# Генерация RSA приватного ключа размером 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Извлекаем публичный ключ на основе приватного ключа и сохраняем
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```