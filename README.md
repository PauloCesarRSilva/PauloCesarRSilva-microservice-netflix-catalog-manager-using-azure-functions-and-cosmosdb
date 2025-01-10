## Documentation

This project is a microservice for managing a Netflix-like catalog using Azure Functions and CosmosDB. It is designed to be scalable, efficient, and easy to maintain.

### Project Structure
This project is divided into two main parts:
1. **Backend**: Contains the Azure Functions.
2. **Frontend**: A web interface to fetch and retrieve data.

### Folder Structure
The project is organized into two folders:

```
microservice-netflix-catalog-manager-using-azure-functions-and-cosmosdb/
├── backend-functions/
│   ├── function_app/
│   ├── host.json/
│   ├── local.settings.json/
│   ├── requirements.txt/
├── frontend-list-movies/
│   ├── src/
│       ├── components/
│       ├── utils/
|       |── app.py
|       |── README.md
│       ├── requirements.txt/
```

### Getting Started
#### Prerequisites
- Azure subscription or a sandbox with admin privileges
  - CosmosDB account
  - Storage account
- Development Environment
  - Python 3.8+
  - Azure Functions Core Tools

#### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/microservice-netflix-catalog-manager-using-azure-functions-and-cosmosdb.git
   cd microservice-netflix-catalog-manager-using-azure-functions-and-cosmosdb
   ```

2. In your Azure subscription, create your resource group, and add the storage account and CosmosDB resources.

3. Set up your Azure Functions and CosmosDB endpoints in the `backend` folder.

### Running the Service
Open each folder in a different VSCode window.

To run the Azure Functions locally:
Use `func host start` or `F5` in VSCode.

Once the functions are up and running locally, you can start the frontend by running:
```sh
streamlit run app.py
```

### Using the APIs
The backend functions contains three APIs that you can use. Each method is documented with details on how to make requests and what parameters are required. You can find the documentation for each method in the `backend-functions/function_app.py` file.

To make a request to an API, you can use tools like `curl`, Postman, or any HTTP client library in your preferred programming language. Below is an example using `curl`:

```sh
curl -X GET "http://localhost:7071/api/movies" -H "Content-Type: application/json"
```

Refer to the method documentation for more details on available endpoints and their usage.
