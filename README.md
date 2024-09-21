## Wiseby Design Store

#### A minimalistic store page to display products, in short a lightweight PIM and CMS system for small businesses and resellers.

## Setup

- Create a environment with venv `python -m venv ./env`
- Acivate the environment `source ./env/bin/activate`
- Install dependencies `pip install --requirements`
- Create a new database (currently sqlite)
  - DB Commands:
    - flask --app store init-db
- Create directories to store files/images
  `mkdir ./instance/files/images/products`
- Start the environment `flask --app store run --debug`
