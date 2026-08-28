# Example of a model using SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
```

Similarly, your Flask-WTF forms can be set up as follows:

```python theme={null}
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

<Callout icon="lightbulb">
  Keep in mind that some parts of this code might not function correctly on the first try. The intentional errors are meant to represent real-world troubleshooting scenarios when using AI-generated tools.
</Callout>

***

## Next Steps

In the upcoming lesson, we will integrate the Flask API and perform testing to ensure the application operates as expected. We will also troubleshoot and refine the workflow to enhance our development process.

Happy coding, and see you in the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-development/module/0f8882f1-0976-491e-8243-9b522243717f/lesson/c43e2b75-72fe-4d97-9430-661e8177d637" />
</CardGroup>


# Testing with Postman

Source: https://notes.kodekloud.com/docs/AI-Assisted-Development/Development-Phase-Backend/Testing-with-Postman/page

This guide covers testing the image upload endpoint of a Flask API using Postman, focusing on validation, error handling, and logging.

In this guide, we walk you through testing the image upload endpoint of our Flask API. The endpoint now features enhanced image-loading, validation, robust error handling, and detailed logging. We use [Postman Essentials](https://learn.kodekloud.com/user/courses/postman-essentials) to simulate various scenarios—including successful uploads and error conditions—to ensure the system behaves as expected.

Below is an excerpt of the image upload endpoint. This snippet demonstrates how we manage file selection, validate file extensions, check file content using both imghdr and Pillow, and verify the quality parameter. Notice that after reading the file content, we reset the file pointer to ensure proper subsequent processing.

```python theme={null}
def upload():
    image = request.files['image']

    if image.filename == '':
        logger.error('No image selected for uploading')
        return jsonify({'error': 'No image selected for uploading'}), 400

    # Secure the filename
    filename = secure_filename(image.filename)

    # Check the file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        logger.error('Invalid file extension: %s', filename)
        return jsonify({'error': 'Invalid file extension'}), 400

    # Check the file content
    image_content = image.read()
    image.seek(0)  # Reset the file pointer to the beginning
    if imghdr.what(None, h=image_content) not in allowed_extensions:
        logger.error('Invalid image file content for: %s', filename)
        return jsonify({'error': 'Invalid image file'}), 400

    # Additional validation using Pillow
    try:
        img = Image.open(io.BytesIO(image_content))
```

## Running the Flask Server and Testing with Postman

Once the Flask server is running using `flask run`, open [Postman Essentials](https://learn.kodekloud.com/user/courses/postman-essentials) and follow these steps:

1. **Select an Image:** For this test, we use an image of the Northern Lights.
2. **Set the Parameters:** In Postman, create a new request with the following details.

Below is an example request for a full-quality image upload:

```text theme={null}
POST http://127.0.0.1:5000/upload

Key          Value
image        DSC90804.JPG
quality      100
```

This test confirms that the system only accepts specific file types—PNG, JPEG, JPG, and GIF—even when JPEG is a less common file extension.

## Additional Upload Function Verification

The following snippet shows an alternative version of the upload function. This version first checks if the 'image' key exists, then validates the file extension and content:

```python theme={null}
def upload():
    try:
        if 'image' not in request.files:
            logger.error('No image part in the request')
            return jsonify({'error': 'No image part in the request'}), 400

        image = request.files['image']

        if image.filename == '':
            logger.error('No image selected for uploading')
            return jsonify({'error': 'No image selected for uploading'}), 400

        # Secure the filename
        filename = secure_filename(image.filename)

        # Check the file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            logger.error('Invalid file extension: %s', filename)
            return jsonify({'error': 'Invalid file extension'}), 400

        # Check the file content
        image_content = image.read()
        image.seek(0)  # Reset the file pointer to the beginning
        if imghdr.what(None, h=image_content) not in allowed_extensions:
            logger.error('Invalid image file content for: %s', filename)
            return jsonify({'error': 'Invalid image file'}), 400
```

### Testing with a JPEG File

For a JPEG file upload, the request might look like this:

```text theme={null}
POST http://127.0.0.1:5000/upload
Key           Value
image         DSC08804.JPG
quality       100
```

### Testing with a PNG File

After selecting a PNG image (e.g., `book.png`), setting the quality parameter to 100 should display an acceptable image. However, reducing quality to 5 will result in poor output:

```text theme={null}
POST http://127.0.0.1:5000/upload
Params:
  image: File --> book.png
  quality: Text --> 5
```

### Testing with Another JPEG File

Similarly, testing with another JPEG file (`coolgirl.jpeg`) confirms that the quality adjustments work as expected:

```text theme={null}
POST http://127.0.0.1:5000/upload

Key              Value
image            File: coolgirl.jpeg
quality          Text: 100

Response:
200 OK
```

### Testing with a GIF File

When attempting to upload a GIF file, you may see a "failed to decode image" error. This outcome is expected because OpenCV's imdecode function does not support GIF images:

```python theme={null}
def upload():
    logger.error('Invalid image file content')
    return jsonify({'error': 'Invalid image file'})
