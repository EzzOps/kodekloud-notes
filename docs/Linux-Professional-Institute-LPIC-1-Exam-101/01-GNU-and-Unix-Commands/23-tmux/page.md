# tmux

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/tmux/page

Practical guide to tmux covering sessions, windows, panes, copy paste, key bindings, and basic configuration for terminal multiplexing.

This lesson covers tmux fundamentals: what tmux is, how to start it, and how to work with sessions, windows, panes, copy/paste, and basic configuration.

tmux (first released in 2007) is a modern terminal multiplexer similar to GNU Screen but with several enhancements:

* Client–server model: a single server manages multiple sessions; each session contains windows, and windows can be shared between clients.
* Interactive menus for selecting sessions, windows, and clients.
* The same window can be linked to multiple sessions.
* Supports both Vim and GNU Emacs key layouts.
* Full UTF-8 and 256-color terminal support.

<Frame>
  <img
    alt="A dark-themed slide titled &#x22;tmux&#x22; listing features like &#x22;Released in 2007,&#x22;
client-server model with shared windows, interactive session/window selection,
linking the same window to multiple sessions, vim and Emacs key layouts, and
UTF-8/256-color terminal support. The KodeKloud logo appears in the
top-right."
  />
</Frame>

Getting started

* Start tmux from your shell:

```bash theme={null}
$ tmux
```

This opens a shell inside tmux and shows a status bar along the bottom of the terminal. The default command prefix (leader key) is Ctrl+b (referred to below as "prefix").

Status bar contents

* Session name
* Window index (tmux counts windows from 0)
* Window name (by default tmux shows the running program name and updates it automatically)
* An asterisk (\*) indicates the currently visible window
* Host name, time, date, etc.

Example: start tmux and create a named session and window

```bash theme={null}
