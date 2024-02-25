# Feature Store with MongoDB and SimpleEmbeddingService

## Sample Dataset
Home Depot product data is downloaded from <https://data.world/>

You can check out my project @ [Data.World](https://data.world/mehmetcagri/educationmaterials)
## Compose Files
### MongoDB
For the purpose of this tutorial MongoDB is used to store embeddings along with rest of the data
> sudo docker volume create mondodb_data
> 
> sudo docker-compose up -d
```yaml
version: '3.7'
services:
  mongodb_container:
    image: mongo:latest
    environment:
      MONGO_INITDB_ROOT_USERNAME: username
      MONGO_INITDB_ROOT_PASSWORD: password
    ports:
      - 27017:27017
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```
### PostgreSQL
PostgreSQL DB server with pgvector extension is used. Vector storage and indexing capabilities are not part of this tutorial
> sudo docker volume create postgresql_data
> 
> sudo docker-compose up -d

```yaml
services:
  db:
    hostname: db
    image: ankane/pgvector
    ports:
     - 5432:5432
    restart: always
    environment:
      - POSTGRES_DB=vectordb
      - POSTGRES_USER=testuser
      - POSTGRES_PASSWORD=testpwd
      - POSTGRES_HOST_AUTH_METHOD=trust
    volumes:
     - postgresql_data:/var/lib/postgresql/data
     
volumes:
  postgresql_data:
```
## FileProcessor Notebook
This notebook is used for the initial setup of the Postgre data source and sample use of embedding service for the ETL process to store Product data and embeddings. The embeddings for the product names will be generated.

## Next Steps
<ol>
  <li>Initialize Databases -  ✅</li>
  <li>Create embeddings for product names and create collection - ✅</li>
  <li>Extending SimpleEmbeddingService to handle images - ✅</li>
  <li>Create image embeddings for product images and update collection - ✅</li>
  <li>Automation of feature store updates with Prefect - ✅</li>
</ol>
