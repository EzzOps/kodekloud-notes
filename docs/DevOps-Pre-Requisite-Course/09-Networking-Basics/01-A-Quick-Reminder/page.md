# Output:
# Hi
```

```bash theme={null}
ls
# Output (example):
# file.txt  my_dir1  file2.conf
```

```bash theme={null}
cd my_dir1
```

```bash theme={null}
pwd
# Output (example):
# /home/my_dir1
```

```bash theme={null}
mkdir new_directory
```

```bash theme={null}
cd new_directory; mkdir www; pwd
# Output (example):
# /home/my_dir1/new_directory
```

<Callout icon="lightbulb">
  The above example demonstrates executing multiple commands in sequence by separating them with semicolons. This method enables streamlined operations within the CLI.
</Callout>

To create an entire directory tree in a single command, use the following:

```bash theme={null}
mkdir -p /tmp/asia/india/bangalore
```

The `-p` option ensures that the entire directory tree is created if it doesn’t already exist. Conversely, to remove a directory and its contents recursively, you can use:

```bash theme={null}
rm -r /path/to/directory
```

## Working with Files

File manipulation is a common Linux task. Here are some basic file operations:

1. Create an empty file:

   ```bash theme={null}
   touch new_file.txt
   ```

2. Add content to a file using redirection:

   ```bash theme={null}
   cat > new_file.txt
   This is some sample content.
   # (Press CTRL+D to save)
   ```

3. Display the file contents:

   ```bash theme={null}
   cat new_file.txt
   # Output:
   # This is some sample content.
   ```

For editing files, text editors like vi or vim are essential tools and will be covered in more detail later in the course. Additionally, you can easily copy, move, and delete files:

```bash theme={null}
cp new_file.txt copy_file.txt
mv new_file.txt sample_file.txt  # This renames the file
rm sample_file.txt
```

These commands allow you to duplicate, rename/move, and remove files as required.

<Callout icon="lightbulb">
  We encourage you to practice using these commands within a lab environment to build confidence and improve your command line proficiency.
</Callout>

As you progress through the labs, focus on mastering these CLI fundamentals. The next section will guide you through deploying a Linux system on your laptop using tools like VirtualBox, providing a solid foundation for deeper exploration in future lessons.

Happy learning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/c990b480-a646-4321-89b4-a6fbc217f4e2/lesson/b9610050-dedf-4758-ab56-88b15a24b32a" />
</CardGroup>


# A Quick Reminder

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Networking-Basics/A-Quick-Reminder/page

This article emphasizes the importance of completing course materials before setting up a local environment, focusing on Docker image management and running containers.

In this lesson, it's essential to focus on the provided labs and instructional videos. While the idea of setting up your own local environment might be tempting, we strongly recommend that you complete the course materials first. These labs and videos offer a structured, distraction-free learning experience designed to equip you with the necessary skills step by step.

<Callout icon="lightbulb">
  Completing the structured course materials ensures a streamlined learning path and minimizes potential interruptions. This approach helps you optimize your learning and makes your time with KodeKloud more productive.
</Callout>

## Listing Docker Images

During the labs, you'll encounter tasks such as listing Docker images on your system. Below is an example command that displays available Docker images:

```bash theme={null}
$ docker images
REPOSITORY                    TAG       SIZE
redis                         latest    105MB
ubuntu                        latest    72.7MB
mysql                         latest    556MB
nginx                         latest    22.6MB
alpine                        latest    5.61MB
postgres                      latest    133MB
kodekloud/simple-webapp-mysql latest    314MB
kodekloud/simple-webapp      latest    96.6MB
```

## Running a Redis Container

Once you're comfortable with the basics, you'll have the opportunity to run containers and build out your local environment. For now, in the lab environment, try running a Redis container with the following command:

```bash theme={null}
$ docker run redis
```

Thank you for choosing our course. We at KodeKloud are committed to guiding you through every step of your learning journey and helping you achieve your technical career goals.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-pre-requisite-course/module/1790dd89-e589-4173-a51e-7be5efbd210a/lesson/9ae601b6-e4f5-4b06-a96b-b56ebcd3035b" />
</CardGroup>
