# Setup Git

Source: https://notes.kodekloud.com/docs/Python-API-Development-with-FastAPI/Deployment/Setup-Git/page

Learn to configure Git for projects, enabling change tracking and establishing a remote repository for code storage to simplify deployment and enhance collaboration.

In this lesson, you'll learn how to configure Git for your projects—enabling change tracking and establishing a remote repository for code storage. This process not only simplifies deployment but also enhances collaboration within your team.

Below is an example FastAPI application used in our project. Although this code snippet isn’t directly related to Git setup, it provides context for what will be version controlled.

```python theme={null}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
