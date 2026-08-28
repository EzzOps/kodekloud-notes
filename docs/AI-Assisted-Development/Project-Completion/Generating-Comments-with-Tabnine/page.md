# Generating Comments with Tabnine

Source: https://notes.kodekloud.com/docs/AI-Assisted-Development/Project-Completion/Generating-Comments-with-Tabnine/page

This article explores using Tabnine to generate inline code comments for a Python backend and React frontend, addressing challenges in documenting large functions.

In this lesson, we explore how to use Tabnine to generate inline code comments for our application. Our project features a Python backend built with Flask for image compression using OpenCV and a React frontend for the image optimizer. Although our application functions well, it requires proper documentation. We will review approaches and challenges involved in generating inline documentation for large functions.

***

## Documenting the Python Backend

Our Python backend contains an 80-line upload function that processes image uploads. Below is an excerpt of the code:

```python theme={null}
import logging
from flask import Blueprint, request, jsonify, send_file
import cv2
import numpy as np
import io
import imghdr
from werkzeug.utils import secure_filename
from PIL import Image
