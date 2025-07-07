## Steps to run the project:
1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Set up the virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate
    ```

2. Set environment variables:
    ```
    `AUTH`: {"users":{"bharatx":"selected-candidate-1"}}
    ```
3. Run the application:
    ```
    make start
    ```

# working curl request
```
curl --location 'https://bharat-x-sepia.vercel.app/search/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YmhhcmF0eDpzZWxlY3RlZC1jYW5kaWRhdGUtMQ==' \
--data '{
    "country": "US",
    "query": "IPhone 16 Pro"
}'
```