# Punch

CLI work clocking system.

## Usage/Commands

```
Usage: punch <command> [options]

Commands:
  in                Record punch-in time
  break             Start or stop a break
    start             Record break start time
    end               Record break end time
  out               Record punch-out time
  state             Output the current state of the TimeLog
    --index           Default index=1. Index from the head entry
    --hours           Default hours=8. How long the work day is

Coming soon:
  reveal            Open a program to manually edit the contents of .clock

Options:
  -h, --help        Show this usage menu
  --debug           Run with debug messages


```

## Setup

### Mac/Linux (UNIX):

1. Install the latest version of python/pip.

1. Use pip to install pyinstaller:

    ```
    pip3 install pyinstaller
    ```
    or
    ```
    python3 -m pip install pyinstaller
    ```

1. Check the installation of pyinstaller by running

    ```
    which pyinstaller
    ```
    or
    ```
    pyinstaller -v
    ```

1. From GitHub, make sure you're in the branch of the your operating system (the `mac` branch will work for both MacOS and Linux).

1. Click the green `Code` button, then `Download ZIP` from the menu.

1. Unzip the project directory.

    NOTE: You may wish to move it out of the Downloads folder and into another location within your user directory.

1. In the terminal, cd into the unzipped project directory.

    e.g.
    ```
    cd ~/Downloads/punch-mac
    ```

1. Run the `build.sh` shell script:

    ```
    ./build.sh
    ```
    or 
    ```
    sh build.sh
    ```

1. Verify that the distribution directory was created by running

    ```
    ls
    ```
    Output should look similar to this:
    ```
    README.md          clock_interface.py punch.py
    build              dist               timelog.py
    build.sh           log_entry.py       utils.py
    ```
    Just make sure there is a `build/` and a `dist/` directory.

1. Add the resulting distribution executable to your PATH.

    0. Create a file at `~/.zshrc` if you don't already have one.

    1. Open `~/.zshrc` using your favorite text editor.
        
        e.g.
        ```
        code ~/.zshrc
        ```

    1. Modify this line and add it to the bottom of the file:

        ```
        export PATH="$PATH:$HOME/path/to/dist/punch"
        ```
        e.g.
        ```
        ...
        export PATH="$PATH:$HOME/Downloads/punch-mac/dist/punch"
        ```

        (The `punch` executable file should be located in the `dist/punch/` dir)

1. Restart your terminal.

1. Verify that the punch CLI works by running `punch -h`.

    Output:
    ```
    user@host:~/dev/python/punch-mac % punch -h

    Usage: punch <command> [options]

    Commands:
      in                Record punch-in time
      break             Start or stop a break
        start             Record break start time
        end               Record break end time
      out               Record punch-out time
      state             Output the current state of the TimeLog
        --index           Default index=1. Index from the head entry
        --hours           Default hours=8. How long the work day is

    Coming soon:
      reveal          Open a program to manually edit the contents of .clock

    Removed:
      show                      Output the contents of the .clock file
      upload                    Upload current .csv file to Google Sheets worksheet
      email                     Display the service email account
      --desc "[description]"    Add or replace existing work description

    Options:
      -h, --help        Show this usage menu
      --debug           Run with debug messages

    user@host:~/dev/python/punch-mac % 
    ```

<hr>

### Windows:

1. Install the latest version of python/pip.

1. Use pip to install pyinstaller:

    ```
    pip install pyinstaller
    ```
    or
    ```
    python -m pip install pyinstaller
    ```

1. Check the installation of pyinstaller by running

    ```
    pyinstaller -v
    ```

1. From GitHub, make sure you're in the branch of the your operating system (the `win` branch for Windows).

1. Click the green `Code` button, then `Download ZIP` from the menu.

1. Unzip the project directory.

    NOTE: You may wish to move it out of the Downloads folder and into another location within your user directory, such as your `%LOCALAPPDATA%` folder.

1. In the terminal, cd into the unzipped project directory.

    e.g.
    ```
    cd %LOCALAPPDATA%/punch-win
    ```

1. Run the `build.bat` batch script:

    ```
    ./build.bat
    ```

1. Verify that the distribution directory was created by running

    ```
    ls
    ```
    Output should look similar to this:
    ```
    
        Directory: %USER_PROFILE%\Downloads\punch-win
    
    MODE    LastWriteTime    Length Name
    ----    -------------    ------ ----
    d----             ...           build
    d----             ...           dist
    -a---             ...       ... build.bat
    -a---             ...       ... clock_interface.py
    -a---             ...       ... log_entry.py
    -a---             ...       ... punch.py
    -a---             ...       ... README.md
    -a---             ...       ... timelog.py
    -a---             ...       ... utils.py
    ```
    Just make sure there is a `build/` and a `dist/` directory.

1. Add the distribution directory containing the resulting executable to your PATH.

    1. Open System Environment Variables.
    1. Edit PATH variable.
    1. Add the `path/to/dist/punch` as a new PATH entry.

        e.g. `%LOCALAPPDATA%/punch-windows/dist/punch`

        (`punch.exe` should be located in the `dist/punch/` dir within the project folder)

1. Restart your terminal.

1. Verify that the punch CLI works by running `punch -h`.


## Features

- Ability to start and stop (a) break(s) in between punch-in and -out.

    e.g.
    ```
    user@host: ~ > punch in
    user@host: ~ > punch break start
    user@host: ~ > punch break end
    user@host: ~ > punch out
    ```

- `punch state` shows how much time has elapsed since punch-in.
- `punch state` shows when to clock out to achieve 8 hours.