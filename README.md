# Project #7 - Python Discord-Chat Exporter Script

Project Type: Python project to export Discord chats history and securely uploading it to an Amazon S3 bucket.

Project Description: Client wanted a python project to export discord chats and he wanted to dockerize and deploy it in ECS Cluster.

Solution:
- I developed a python project that takes a json file as input and extract discord channels with channel id from json file.
- I dockerized my python discord-chat-exporter project and pushed it to Dockerhub repository.
- I configured security group for Python application.
- I configured security group for LoadBalancer.
- I deployed an ECS cluster.
- I deployed a Task definiton according to my Application needs.
- I deployed my task in service.
- I provided the demo to the client which demonstrated the process of chats being exported and being stored in s3 bucket.

  ![1bf7965af8184b76acf2fa70940f686c](https://github.com/awab-hassan/07-pythonProject-DEVOPS/assets/90965012/89f73208-53b7-49c9-b013-6b0298b50340)
