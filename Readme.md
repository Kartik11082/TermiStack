# Stacksearch

## _CLI tool for Stack Exchange_

Stacksearch is a versatile CLI tool that lets you search Stack Exchange websites and debug Python scripts directly from the terminal.

## Features

- Search any Stack Exchange site from the terminal.
- Input mode available if flags are too cumbersome.
- Know whether a question is answered directly in the terminal.
- Enjoy colored terminal text 🤩.
- Run a Python script and automatically search Stack Overflow for any errors encountered, returning relevant results.

## Tech

Stacksearch uses a number of projects to work properly:

- [Requests][requestsSite] - HTTP for Humans.
- [Argparse][argparseSite] - Parser for command-line options and arguments.

And of course, Stacksearch itself is open-source with a [repository][githubPage] on GitHub.

## Installation

Stacksearch requires [Python][pythonSIte] to run.

Clone the repository in the startup directory of your terminal:

```sh
git clone https://github.com/Kartik11082/Stacksearch.git
cd Stacksearch
```

![cloning](https://user-images.githubusercontent.com/49190983/159106823-b894c7bf-5e51-4f31-b81e-b2ddd98fbefc.gif)

Install all requirements:

```sh
pip install -r requirement.txt
```

## Command Formats

- ### Flags

  - `-i`: for input mode.
  - `-q "_Query_"`: for searching queries in the title.
  - `-n _number_`: number of responses to return.
  - `-t "_tags_"`: for filtering by tags.
  - `-s "_sitename_"`: for specifying the website name.
  - `--run "_script.py_"`: execute a Python script and search for errors on Stack Overflow if they occur.

- ### Examples
  - Searching in terminal:
    ![run](https://user-images.githubusercontent.com/49190983/159106838-b8489b47-8a14-4b52-b68f-ff2042e5013c.gif)
  - Input mode:
    ![inputmode](https://user-images.githubusercontent.com/49190983/159106854-e0911baa-bd30-41ab-9606-282d501da10f.gif)
  - Running a script and fetching error details:
    ```sh
    python stacksearch.py --run example_script.py
    ```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # "Reference links"
[githubPage]: https://github.com/Kartik11082/Stacksearch
[requestsSite]: https://docs.python-requests.org/en/latest/
[argparseSite]: https://docs.python.org/3/library/argparse.html
[pythonSite]: https://www.python.org/
