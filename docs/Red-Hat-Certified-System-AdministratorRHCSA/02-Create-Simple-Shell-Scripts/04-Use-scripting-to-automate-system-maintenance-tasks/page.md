# Use scripting to automate system maintenance tasks

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Create-Simple-Shell-Scripts/Use-scripting-to-automate-system-maintenance-tasks/page

This guide explores using Bash scripting to automate routine system maintenance tasks on CentOS.

In this guide, we explore how Bash scripting can automate routine system maintenance tasks on a CentOS operating system. When you log into CentOS, you are presented with a shell prompt where the Bash command interpreter runs. Although you can enter individual commands interactively, Bash scripts allow you to execute a series of commands stored in a file sequentially.

## Understanding Bash and Script Basics

After a successful login, Bash starts and awaits your commands. Every command you type is interpreted and executed. Instead of entering commands one by one, you can place them in a script file. A script is simply a file with multiple commands executed in order from top to bottom.

For example, running the following command interactively prints the current date and time:

```bash theme={null}
$ date
Mon Dec  6 16:28:09 CST 2021
```

To better understand the script workflow, let’s create a simple script.

### Creating Your First Script

1. Create a new file called "script.sh". (The `.sh` extension is optional but helpful for identification.)

2. Open "script.sh" in your favorite text editor, and add the following content. The first line must include the shebang:

   ```bash theme={null}
   #!/bin/bash
   ```

   This tells the system to use `/bin/bash` as the interpreter. Comments in the script, indicated by a hash sign (#), describe the functionality but are not executed.

3. Append a command to log the current date and time to a file:

   ```bash theme={null}
   #!/bin/bash
   # Log the date and time the script was last executed
   date >> /tmp/script.log
   ```

You can run commands in scripts as you would on the shell prompt, including redirection and piping. Now, add another command to append the contents of `/proc/version` (which shows the Linux kernel details) to the same log file. The complete content of the script now looks like this:

```bash theme={null}
#!/bin/bash
