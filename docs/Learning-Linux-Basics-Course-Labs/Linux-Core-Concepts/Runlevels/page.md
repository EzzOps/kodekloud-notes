# Runlevels

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Linux-Core-Concepts/Runlevels/page

This article explains Linux runlevels and systemd targets, detailing how to configure system boot modes and change default operational settings.

Bob noticed something unusual with Dave's laptop.

“Dave, why is it that after the boot process your system goes directly to the Command Line Interface? Mine always loads up the graphical interface,” Bob asked.

Dave explained, “That's because I have specifically set up my system to boot into non-graphical mode.” In Linux, the system can operate in several modes, known as runlevels. You might be familiar with the graphical mode; however, runlevels allow for various operational modes beyond just the GUI.

To determine the current runlevel of a Linux system, use the `runlevel` command. For example, on Dave's laptop, the output is:

```bash theme={null}
Ubuntu 18.04.4 LTS caleston-lp03 tty1
caleston-lp03 login:
```

This output indicates that Dave’s system is running at runlevel 3, which is non-graphical mode. In contrast, Bob’s laptop is configured to run at runlevel 5, which provides a graphical user interface.

The boot process utilizes the runlevel setting by having the init process check the current runlevel and start only those services required for that mode. For instance, graphical mode (runlevel 5) needs a display manager service to start the GUI, whereas this service is unnecessary in non-graphical mode.

<Frame>
  ![The image explains systemd runlevels, showing graphical and command line interfaces, with indicators for display-manager service enabled or disabled.](https://kodekloud.com/kk-media/image/upload/v1752881120/notes-assets/images/Learning-Linux-Basics-Course-Labs-Runlevels/frame_80.jpg)
</Frame>

In modern Linux distributions like Ubuntu 18.04, the system uses systemd as the init process. Under systemd, traditional runlevels are represented as targets:

<Frame>
  ![The image explains systemd targets and runlevels, showing how they boot into graphical or command line interfaces on RHEL and Ubuntu systems.](https://kodekloud.com/kk-media/image/upload/v1752881121/notes-assets/images/Learning-Linux-Basics-Course-Labs-Runlevels/frame_110.jpg)
</Frame>

In this context:

* Runlevel 5 corresponds to the graphical target.
* Runlevel 3 corresponds to the multi-user target.

While additional runlevels (or targets) exist, these two are the most commonly used. For a detailed list of available runlevels/targets, refer to the official [systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/).

<Callout icon="lightbulb">
  If your system boots into a command line interface by default, it's likely configured to use the multi-user target.
</Callout>

## Changing the Default Target

To view the current default systemd target, execute the following command, which reads the file located at `/etc/systemd/system/default.target`:

```bash theme={null}
$ systemctl get-default
graphical.target

$ ls -ltr /etc/systemd/system/default.target
```

In this example, the `default.target` file is a symbolic link to the `graphical.target` unit file located in the `/lib/systemd/system/` directory.

If you wish to change the default target, use the `systemctl set-default` command followed by your desired target. For instance, to switch from graphical mode (runlevel 5) to multi-user mode (runlevel 3), run:

```bash theme={null}
$ systemctl get-default
graphical.target

$ ls -ltr /etc/systemd/system/default.target
/etc/systemd/system/default.target -> /lib/systemd/system/graphical.target

$ systemctl set-default multi-user.target
Created symlink /etc/systemd/system/default.target -> /lib/systemd/system/multi-user.target
```

This command updates the default target, effectively switching your system's mode of operation from graphical to non-graphical.

<Callout icon="lightbulb">
  After changing the default target, you may need to reboot your system for the changes to take effect.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learning-linux-basics-course-labs/module/19296611-5fb9-4e5d-a926-d157d3f3c3db/lesson/b2e0b8bc-8823-4a2c-b66d-3f85184a2404" />
</CardGroup>
