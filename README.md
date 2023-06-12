## General Info

NotionChat is a token gated LLM powered chatbot that allows you to query any Notion database you have access to.

## Setup

You’ll first need to create your notion integration token, connect it to a database that you want to query, and then save your token and database ID to use with the app. Full instructions from Notion can be found here:

[Create an integration (notion.com)](https://developers.notion.com/docs/create-a-notion-integration#step-2-share-a-database-with-your-integration)

To run this project, install it locally using yarn for the frontend and pip for the API:

Clone the repository

```
$ git clone <https://github.com/username/NotionChat.git>
```

Navigate to the repository

```
$ cd Notion-Chat-main
```

Install the frontend dependencies

```
$ cd frontend
$ yarn
```

Install the API dependencies

```
$ cd ../api
$ pip install -r requirements.txt
```

To run the frontend and the API, you'll need two terminals. In the first terminal, navigate to the frontend directory and start the server:

```
$ cd frontend
$ yarn dev
```

In the second terminal, navigate to the API directory and start the server:

```
$ cd api
$ cd engrok
$ uvicorn nchat_ngrok_api:app --reload
```

The frontend server will be available on http://localhost:3000 and the API server will be running on http://127.0.0.1:8000
