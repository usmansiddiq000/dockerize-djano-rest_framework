Created by Muhammad Usman Siddiq
# dockerize-djano-rest_framework

```
git clone https://github.com/usmansiddiq000/dockerize-djano-rest_framework.git
```

inside project folder run command to Build docker image
```
sudo docker build -t django_api_image  .
```

after that spin up Docker container
```
sudo docker run -d -p 8000:8000 --name api_container django_api_image
```
Now django rest_framwork api will be up and running at localhost:8000


Testing admin Urls's
```
1) http://localhost:8000/admin/ (username: admin, password: admin)
```

Testing Urls's
```
1) http://localhost:8000/rest-auth/login/ (username: user, password: user)
2) http://localhost:8000/items/list/
3) http://localhost:8000/items/get-order/
```

```
docker ps -a
```
it will list all container running.

