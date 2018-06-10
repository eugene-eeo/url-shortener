# url-shortener

URL shortener written with Flask and MySQL.

## Installation

- You need to have a local instance of MySQL running.
- `$ ./install.sh` (if you have authentication set up for your
  MySQL database you probably need to modify the script). By
  default ('in production') the app uses a database called `urlshortener`.

## HTTP endpoints

| Endpoint        | Method | JSON data | Description |
|-----------------|:------:|:---------:|-------------|
| `/url/<id>`     | GET    |           | Fetches the URL object associated with the given ID. |
| `/url/<id>`     | DELETE |           | Deletes the URL object associated with the ID. |
| `/url/<id>`     | POST   | URL object without `hits` and `id`. | Associates an ID with a given URL. If the ID is already used this returns a non 200 status code. |
| `/url`          | POST   | URL object without `hits` and `id`. | Shortens the given URL and returns a JSON object with a random ID. |
| `/tagged/<tag>` | GET    |           | Returns all URL objects that have the given tag. |
| `/fwd/<id>`     | GET    |           | Redirects to the URL associated with the given ID (if there is one, else 404 is raised). |

### URL object format

```json
{
    "id":          "id",
    "destination": "valid http(s) url",
    "tags":        ["tag1", "tag2", "..."],
    "hits":        1
}
```

## Running tests

You need to have a running (local) MySQL instance. The way I do it:

```sh
$ mysqld --skip-grant-tables
$ URLSHORTENER_DB='urlshortener_testing' python app.py  # another terminal session
$ ./test.sh                                             # another terminal session
```
