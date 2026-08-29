# pip 9.0.3 from /usr/lib/python3.6/site-packages (python 3.6)
```

> **lightbulb** If the command is simply `pip` without a version specifier, running `pip -V` will help determine which Python version it is associated with. Using the wrong version might result in installing libraries in an unintended environment.

## Installing Packages

To install a package with PIP, use the following syntax. For example, installing the popular Flask web framework can be done as:

```bash theme={null}
pip install flask
```

When Python is installed, a version-specific directory is created under the user library path. Each Python installation maintains its own `site-packages` folder where packages are stored. For instance, if Flask is installed using pip for Python 2, the installation path might look like this:

* For 32-bit packages
* For 64-bit packages
  * Python 2.7: `/usr/lib64/python2.7/site-packages`
  * Python 3.6: `/usr/lib/python3.6/site-packages`

This separation is important for troubleshooting issues where an application cannot locate installed packages. To check where a specific package is installed, use the `pip show` command:

```bash theme={null}
pip show flask
```

An example output may be:

```bash theme={null}
Name: Flask
Version: 1.1.1
Summary: A simple framework for building complex web applications.
Home-page: https://palletsprojects.com/p/flask/
Author: Armin Ronacher
Author-email: armin.ronacher@active-4.com
License: BSD-3-Clause
Location: /usr/lib64/python2.7/site-packages
Requires: Werkzeug, click, Jinja2, itsdangerous
```

## Importing Packages and sys.path

When you import a package using the `import` statement, Python searches through directories listed in `sys.path`. To inspect these directories, run:

```bash theme={null}
python2 -c "import sys; print(sys.path)"
```

This command produces an output similar to:

```Python theme={null}
['/usr/lib/python27.zip',
 '/usr/lib64/python2.7/plat-linux2',
 '/usr/lib/python2.7/lib-tk',
 '/usr/lib/python2.7/lib-old',
 '/usr/lib/python2.7/dylib',
 '/usr/lib/python2.7/site-packages']
```

If an import fails, reviewing the paths in `sys.path` can help identify whether the package was installed in a different location or for another Python version.

## Managing Dependencies with requirements.txt

For larger applications that require multiple packages, it is common to list all dependencies in a file named `requirements.txt`. You can then install all dependencies simultaneously by running:

```bash theme={null}
pip install -r requirements.txt
```

A typical `requirements.txt` file includes package names along with specific versions to avoid compatibility issues. For example:

```plaintext theme={null}
Flask==0.10.1
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.9.6
requests==2.3.0
gunicorn==18.0
```

Storing dependencies with explicit versions ensures consistency for all developers setting up the project using a single command.

## Upgrading and Uninstalling Packages

When a new version of a package becomes available, you can upgrade it using:

```bash theme={null}
pip install flask --upgrade
```

The upgrade process may produce output similar to:

```bash theme={null}
Installing collected packages: click, flask
Attempting uninstall: flask
Found existing installation: Flask 0.10.1
Uninstalling Flask-0.10.1:
Successfully uninstalled Flask-0.10.1
Successfully installed click-7.1.1 flask-1.1.1
```

To uninstall a package, run:

```bash theme={null}
pip uninstall package_name
```

## Additional Package Management Tools

Apart from PIP, Python supports other package management tools such as easy\_install. Originally, easy\_install was used in combination with setuptools to package Python code into a zipped format known as "eggs" (similar to JAR files in Java). Alternatively, you can install or place the egg file in a directory accessible to Python.

Another packaging format is the wheel (with the `.whl` extension). Unlike eggs, wheels require installation (unpacking) before use. They can be installed with a command like:

```bash theme={null}
pip install app.whl
```

## Summary

Python package management with PIP enables you to install, upgrade, and uninstall packages while managing dependencies through a `requirements.txt` file. These tools are essential for maintaining a consistent development environment, particularly when working with multiple Python versions or architectures (32-bit vs 64-bit).

> **lightbulb** Next, apply what you've learned by practicing package management with Python. In the exercise, you will:

  * Identify the list of packages to install.
  * Locate where packages are installed.
  * Work with different versions of PIP.
  * Upgrade and uninstall packages.
  * Utilize `requirements.txt` for dependency management.

Happy coding, and see you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/669946a1-3725-4ba8-af56-14d449f778c3/lesson/0381d9c7-c268-4a11-807d-0b44b5027c47)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/669946a1-3725-4ba8-af56-14d449f778c3/lesson/708d118b-adc4-49d2-b6d8-ebec6dbed209)


# Conclusion

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Conclusion/Conclusion/page

This article concludes a DevOps Prerequisites course and suggests further specialized courses to enhance skills in DevOps and Cloud technologies.

Congratulations on completing the DevOps Prerequisites course! With the insights and skills you have acquired, you are now ready to advance into more specialized DevOps and Cloud courses.

Throughout this course, you mastered the basics of Linux systems, essential applications, networking, YAML, and configuration files. To build upon this strong foundation, consider exploring additional courses:

* Begin with the [Linux Basics Course](https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs) to deepen your understanding of Linux, a critical component in both DevOps and cloud environments. This course presents engaging storylines and hands-on labs that complement the skills you have already developed.
* Enhance your containerization skills by enrolling in the [Docker for Absolute Beginners Course](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner). Docker is indispensable in cloud-native computing and is an excellent primer before moving on to orchestration tools.
* After Docker, consider the [Kubernetes for Beginners Course](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial) to get acquainted with container orchestration and the incredible world of Kubernetes.

![The image shows a beginner's DevOps learning path with courses on Docker, Ansible, Kubernetes, Puppet, and Chef, featuring flowchart-style navigation.](https://kodekloud.com/kk-media/image/upload/v1752873420/notes-assets/images/DevOps-Pre-Requisite-Course-Conclusion/frame_70.jpg)

Kubernetes stands out as one of the most sought-after technologies in IT today. After completing the introductory courses, you can prepare for certifications such as [CKA](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator) and [CKAD](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad). Our certification courses feature extensive hands-on labs and multiple mock exams to ensure your success. Additionally, mastering Kubernetes is a prerequisite for exploring Red Hat OpenShift. Follow the CKAD course with the [Red Hat OpenShift Course](https://learn.kodekloud.com/user/courses/openshift-3-for-the-absolute-beginners) to enhance your deployment skills further.

> **lightbulb** For those interested in automation, start with the [Ansible for Absolute Beginners Course](https://learn.kodekloud.com/user/courses/labs-ansible-for-the-absolute-beginners). This course is tailored for individuals with no prior automation or scripting experience, making it an ideal entry point into the world of IT automation.

The knowledge you gained in this prerequisites course provides a robust foundation for advancing in your DevOps career. Our courses continue to evolve, with new content and hands-on labs that keep you at the forefront of industry practices. Additionally, participating in simulated job environments can further sharpen your real-world skills and prepare you for challenging tasks.

![The image is a webpage from KodeKloud, highlighting statistics and advantages of their engineering program, including real projects and scenarios, with over 2000 engineers and 6000 tasks completed.](https://kodekloud.com/kk-media/image/upload/v1752873421/notes-assets/images/DevOps-Pre-Requisite-Course-Conclusion/frame_170.jpg)

Thank you for joining this course. We look forward to supporting your learning journey across our next courses—happy learning and best of luck in your DevOps endeavors!

- [Watch Video](https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/0a08663a-a9ff-4439-be58-54ef6a481c4a/lesson/08c5dd69-7327-4393-b6dd-8e3f02556200)
