# django-docker-deployment


## File explanation

`.env`
This provides values to template variables in docker compose marked ${variable}.
An `.env.sample` is provided, which can be converted to an `.env` file but this should be
kept out of source control as it may contain sensitive data.



## Launching development environment

`docker compose up`



## Troubleshooting

**Run django container shell**

If container is running:

```docker compose exec -ti django sh```

If container is not running:

``` docker compose run --rm -ti django sh ```


**Delete volumes**

```docker compose down -v```


**Checking db connection from django container**

``` pg_isready -d django -h db -p 5432 -U django```