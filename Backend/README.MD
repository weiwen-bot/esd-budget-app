## Info
- api_gateway folder is for KONG stuff
- Each Microservice/Complexservice should include:
- -service.py (contains the api calls for the microservice)
- -requirement.txt (contains the packages version that the application would use)
- -Dockerfile (Instructions)
- Ideally we want to create a microservice that can do another api method e.g. Graphql, grpc
- And also use another language for the microservice like e.g. Node.js, Java Springboot
- for now we will initalise the db in the service.py

## run the backend
- cd to Backend
- Setup run -> docker compose up --build