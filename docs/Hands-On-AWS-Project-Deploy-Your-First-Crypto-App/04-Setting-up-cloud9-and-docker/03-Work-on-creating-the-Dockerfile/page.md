# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password123"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if provided credentials match the default ones
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
    return render_template('product.html')

@app.route('/place_order')
def place_order():
    product_id = request.args.get('product')
    return render_template('place_order.html', product_id=product_id)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Code to handle order submission will be added later
    pass
```

If you prefer to work locally instead of in Cloud9, cloning CodeCommit on your machine requires proper authentication (CodeCommit credential helper or SSH keys). For more details, see AWS CodeCommit documentation:

* [AWS Cloud9 User Guide](https://docs.aws.amazon.com/cloud9/latest/user-guide/welcome.html)
* [AWS CodeCommit HTTPS connections and Git credentials](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html)

Next steps

* Create a `Dockerfile` in the repository root to containerize the Flask app.
* Build and run the container locally inside Cloud9 to validate the app before deploying to AWS services.

That’s it for this lesson. In the next lesson we will add a Dockerfile and prepare the application for container-based deployment. See you there.

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/f2cfee46-980a-49cb-b81a-dd46bfce3824/lesson/c6012ff4-299e-4702-9693-67e9b3503b02)


# Work on creating the Dockerfile

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/Setting-up-cloud9-and-docker/Work-on-creating-the-Dockerfile/page

Creating a Dockerfile to containerize a Flask app, install dependencies, expose port, and run or prepare for production deployment with recommendations.

Welcome back. In this lesson we'll create a Dockerfile to containerize a Flask application so it can be built, tested locally, and deployed in a scalable way. The steps below walk you through creating a minimal, production-friendly Dockerfile based on a slim Python image, placing the app in a working directory, installing dependencies, and exposing the Flask port.

Prerequisites:

* A Flask app with an entry point named `app.py`.
* A `requirements.txt` file listing Python dependencies.
* Docker installed locally (see [Docker documentation](https://docs.docker.com/get-docker/)).

Open your Cloud9 editor, right-click the project folder, choose New File, and name it `Dockerfile`. Double-click to open the empty file and add the following content step by step.

1. Choose a lightweight Python base image

```dockerfile theme={null}
