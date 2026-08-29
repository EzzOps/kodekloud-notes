# Creating your first shell script

Source: https://notes.kodekloud.com/docs/Shell-Scripts-for-Beginners/Shell-Script-Introduction/Creating-your-first-shell-script/page

Learn to automate tasks by creating your first shell script to execute multiple commands in sequence, reducing manual effort and errors.

In this guide, you'll learn how to automate repetitive tasks by creating your first shell script. Shell scripts allow you to execute multiple commands in sequence, significantly reducing manual effort. Before you start, it’s essential to clearly understand your script’s purpose. List the steps and commands required to complete your task.

## Mission Requirements

For our example mission, the requirements are as follows:

1. Create a directory named "lunar-mission".
2. Create a rocket for that mission.
3. Add the rocket using the "rocket-add" command.
4. Execute the launch sequence with a series of commands.
5. Verify the rocket's status using the "rocket-status" command.

Previously, these steps were executed manually with the following commands:

```bash theme={null}
$ mkdir lunar-mission
$ rocket-add lunar-mission
$ rocket-start-power lunar-mission
$ rocket-internal-power lunar-mission
$ rocket-start-sequence
```

Automating these tasks with a shell script means you only need to run one command to perform all the steps.

## Creating the Shell Script

Create a file called "create-and-launch-rocket.sh" and move all of the above commands into it in the same order. Choosing a descriptive name for your shell script is crucial. In this example, the script not only creates but also launches a rocket—hence, the name "create-and-launch-rocket.sh" clearly reflects its purpose.

Once your shell script is ready, execute it using the bash command. When the script runs, each command is executed sequentially; the script will wait for a command to finish if it takes any time to execute.

Here’s an extended version of the commands that might be included in your script:

```bash theme={null}
$ mkdir lunar-mission
$ rocket-add lunar-mission
$ rocket-start-power lunar-mission
$ rocket-internal-power lunar-mission
$ rocket-start-sequence lunar-mission
$ rocket-start-engine lunar-mission
$ rocket-lift-off lunar-mission
$ rocket-status lunar-mission
```

To execute the script using bash, run:

```bash theme={null}
$ bash create-and-launch-rocket.sh
```

## Running the Script as an Executable Command

You can configure your shell script to run like any other command on your system by making it executable. It is a common best practice to omit the `.sh` extension for commands intended for frequent use.

If you try to run your script immediately after creation, you might encounter an error such as:

```bash theme={null}
$ create-and-launch-rocket
create-and-launch-rocket: command not found
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

The operating system searches for executable commands in directories listed in the PATH environment variable. If your script is not located in one of these directories, it will not be found.

To add your script's directory to your PATH, append that directory to the PATH variable as follows:

```bash theme={null}
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

$ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

$ export PATH=$PATH:/home/michael

$ create-and-launch-rocket
```

By updating your PATH, you can run your script without providing its full path.

## Setting Execution Permissions

For your shell script to run properly, you must set the correct file permissions. If you try to run the script without the appropriate permissions, you might see an error like:

```bash theme={null}
$ /home/michael/create-and-launch-rocket
-bash: ./create-and-launch-rocket: Permission denied
```

Use the `ls -l` command to inspect file permissions. If the execute bit is not set, update the permissions with:

```bash theme={null}
$ chmod +x create-and-launch-rocket
```

Once you’ve added the execute permission, your script will run as expected.

> **lightbulb** * Choose descriptive script names. Avoid generic names like "script1.sh," "my\_script.sh," or "test.sh" to make the script’s purpose clear.
  * If you plan to use the script as an executable command, consider omitting the `.sh` extension for a more natural command-line experience.

## Summary

By following the steps outlined in this guide, you can create and execute a shell script that automates repetitive tasks. This method not only simplifies your workflow but also minimizes errors during manual execution of commands.

Let's practice creating and executing your first shell script. Happy scripting, and see you in the next lesson!

## Additional Resources

* [Bash Scripting Tutorial](https://www.gnu.org/software/bash/manual/bash.html)
* [Shell Script Best Practices](https://www.shellscript.sh/)
* [Linux Command Line Basics](https://linuxjourney.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/bed31683-dcad-4a23-8bb9-c2402635b125)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/shell-scripts-for-beginners/module/2709b373-3a6f-4b31-9aff-fe8a553898fa/lesson/558a44a8-6237-4f38-af65-d2059da05eb7)
