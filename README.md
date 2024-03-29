Globality black
===============

[DISCLAIMER](./DISCLAIMER.md)

[Tech talk](https://docs.google.com/presentation/d/1Lp0jLSI5YJYOXEntxSvaHeOALAlndlgu/edit?usp=sharing&ouid=102083878154902570127&rtpof=true&sd=true)

A wrapper for [black](https://github.com/psf/black), adding pre- and post-processing
to better align with Globality conventions.

`globality-black` performs the following steps:

 - pre-processing: to protect from black actions
 - black
 - postprocessing: to revert / correct black actions

Note: if you are not familiar with black (or need a refresh), please
read our [Black refresh](#black-refresh).


# Table of contents
- [Globality black](#globality-black)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [Pycharm](#pycharm)
  - [JupyterLab](#jupyterlab)
  - [VScode](#vscode)
    - [Working with remotes](#working-with-remotes)
    - [Shortcuts](#shortcuts)
    - [Working with notebooks](#working-with-notebooks)
- [Features](#features)
  - [Blank lines](#blank-lines)
  - [Dotted chains](#dotted-chains)
  - [Length one tuples](#length-one-tuples)
  - [Comprehensions](#comprehensions)
    - [Before globality-black](#before-globality-black)
    - [After globality-black](#after-globality-black)
  - [Partially disable globality-black](#partially-disable-globality-black)
- [Pending / Future work](#pending--future-work)
- [Black refresh](#black-refresh)
  - [Magic comma](#magic-comma)
- [FAQ](#faq)
- [Tests](#tests)
- [Contributing](#contributing)
  - [Submit and issue](#submit-and-issue)
  - [Submit a pull request](#submit-a-pull-request)
  - [Code of Conduct](#code-of-conduct)


# Installation
-----

`pip install globality-black`

# Usage
-----

There are two ways to use `globality-black`, via CLI, or importing the helpers in the library.
Next, we show some typical use cases:

## CLI

Please see command line arguments running `globality-black --help`.

## Pycharm

To use `globality-black` in PyCharm, go to PyCharm -> Preferences... -> Tools -> External Tools -> Click + symbol
to add new external tool.

![img](docs/pycharm-external-tools.png)
Recommended configuration to format the current file:
* Program: path to `globality-black`, e.g. `/Users/marty-mcfly/miniconda3/envs/gb/bin/globality-black`
* Arguments: `$FilePath$`
* Working directory: `$ProjectFileDir$`

Recommended configuration to check the whole repo (but not formatting it it):
* Program: path to `globality-black`, e.g. `/Users/marty-mcfly/miniconda3/envs/gb/bin/globality-black`
* Arguments: `. --check`
* Working directory: `$ProjectFileDir$`

Next, configure a keymap, as in [here](https://www.jetbrains.com/help/pycharm/configuring-keyboard-and-mouse-shortcuts.html).

![img](docs/pycharm-shortcuts.png)

## JupyterLab

We can leverage [this](https://jupyterlab-code-formatter.readthedocs.io/en/latest/how-to-use.html#custom-formatter) extension,
with a custom formatter. Here we explain how to get the following options:

![img](docs/jupyter-lab-new-buttons.png)


There are two ways to apply `globality-black`, see left-hand-side, or by clicking on the button next to "Code". We will configure
the extension to make it apply the `isort + globality-black` pipeline when clicking such button.

To do so, install the extension, generate the config for jupyter lab and edit it:

```shell script
pip install jupyterlab_code_formatter
jupyter lab --generate-config
vim ~/.jupyter/jupyter_lab_config.py
```

You might already have some config in `jupyter_lab_config`. If so, you might want to omit
 the second command above, and edit it (vim) instead.

In any case, we will add the following code:

```python
from jupyterlab_code_formatter.formatters import SERVER_FORMATTERS
from globality_black.jupyter_formatter import GlobalityBlackFormatter
SERVER_FORMATTERS['globality-black'] = GlobalityBlackFormatter(line_length=100)
```

Then, go to the extension preferences, and add:

```json
{
    "preferences": {
        "default_formatter": {
            "python": [
                "isort",
                "globality-black",
            ],
        }
    },
    "isort": {
           "combine_as_imports": true,
           "force_grid_wrap": 4,
           "force_to_top": "true",
           "include_trailing_comma": true,
           "known_third_party": ["wandb", "tqdm"],
           "line_length": 100,
           "lines_after_imports": 2,
           "multi_line_output": 3,
    }
}
```

Notes:
 - The last step above translates into user settings saved in
`~/.jupyter/lab/user-settings/@ryantam626/`.
 - The extension is applied to all cells in the notebook. It can be configured to be applied just to
 the current cell, if interested.
 - The extension is applied to each cell in isolation. Hence, if multiple imports appear in different
 cells, they won't be merged together on top of the notebook.


## VScode

To use `globality-black` in VScode, install the extension
[External formatters](https://marketplace.visualstudio.com/items?itemName=SteefH.external-formatters).

Then, go to Preferences: Settings (JSON). A file `settings.json` will open. Add this to the file:
```json
"[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
        "editor.defaultFormatter": "SteefH.external-formatters",
    },
    "isort.args":["--profile", "black"],
```
This will configure isort to run when saving, and glo-black as the default
formatter. Add also this
```json
[
    "externalFormatters.languages": {
        "python": {
            "command": "$PATH_TO_ENV/bin/globality-black",
            "arguments": [
                "-",
            ]
        }
    },
    "isort.interpreter": [
        "$PATH_TO_ENV/bin/python"
    ],
]
```
setting or replacing `$PATH_TO_ENV` with whatever you need to get to the
`globality-black` Python env.

### Working with remotes
Important: these two paths have to be absolute paths, and need to be the
same everywhere you use VScode. This means that if you use VScode on remotes (e.g. an EC2 instance),
the same paths needs to exist. Obviosuly, that's not possible, since e.g.
in EC2 you'll have `/home/ubuntu/...` and in your machine `/Users/john/...`. A workaround for this is to create a symbolic link in your instance, e.g:
```bash
sudo ln -s /home/ubuntu /Users/john
```

### Shortcuts

 To configure shortcuts, go to `Preferences: Keyboard Shortcuts (JSON)` from the Palette (command+shift+p). The file `keybindings.json` will open.
 Add to this file:
```json
[
    {
        "key": "cmd+shift+j",
        "command": "editor.action.formatDocument",
        "when": "editorHasDocumentFormattingProvider && editorTextFocus && !editorReadonly && !inCompositeEditor"
    }
]
```
This will allow you to run `globality-black` on the currently open file,
passing the content of the file via stdin.

### Working with notebooks

To format notebooks, there is a shortcut
```json
{
    "key": "shift+alt+f",
    "command": "notebook.formatCell",
    "when": "editorHasDocumentFormattingProvider && editorTextFocus && inCompositeEditor && notebookEditable && !editorReadonly && activeEditor == 'workbench.editor.notebook'",
}
```
that you can modify if you don't like this combination. This will format the
current cell with the default formatter. I did not find a way to run isort
though. There is a "format notebook on save" option, but it's not exactly what
 we configured for python files. That would run isort + glo-black.


# Features
--------

## Blank lines

Black would remove those blank lines after `wandb` and `scikit-learn` below:

```
graph.use(
    "wandb",

    "scikit-learn",

    # we love pandas
    "pandas",
)
```

`globality-black` protects those assuming the developer added them for readability.


## Dotted chains

In a similar fashion to the "blank lines" feature, "dotted chains" allows to keep the block:

```python
return (
    df_field[COLUMNS_PER_FIELD[name]]
    .dropna(subset=["column"])
    .reset_index(drop=True)
    .assign(mapped_type=MAP_DICT[name])
)

LABELS = set(
    df[df.labels.apply(len) > 0]
    .flag.apply(curate)
    .apply(normalize)
    .unique()
)
```

the same. In this feature, **we don't explode anything** but rather protect code assuming it was
written by this in purpose for readability.

## Length one tuples

This is a very simple and specific feature. Black (at least up to 21.9b0) has a bug so that tuples
with one element are compressed as in

```python
x = (
    3,
)
```
becomes
```python
x = (3,)
```
See https://github.com/psf/black/issues/1139#issuecomment-951014094. With globality-black,
will protect these.


## Comprehensions

Explode comprehensions
* all dict comprehensions
* any comprehension with an if
* any comprehension with multiple for loops (see examples below)
* list / set comprehensions where the element:
   - has a ternary operator (see examples below)
   - has another comprehension

For everything else, we rely on `black`. Examples:

### Before globality-black

```
[3 for _ in range(10)]

[3 for i in range(10) if i < 4]

{"a": 3 for _ in range(4)}

{"a": 3 for _ in range(4) if i < 4}

["odd" if i %% 2 == 0 else "even" for _ in range(10)]

double_comp1 = [3*i*j for i in range(10) for j in range(4)]

double_comp2 = [[i for i in range(7) if i < 5] for j in range(10)]

double_comp3 = {i: [i for i in range(7) if i < 5] for j in range(10) if i < 2}
```

### After globality-black

```
[3 for _ in range(10)]

[
    3
    for i in range(10)
    if i < 4
]

{
    "a": 3
    for _ in range(4)
}

{
    "a": 3
    for _ in range(4)
    if i < 4
}

[
    "odd" if i %% 2 == 0 else "even"
    for _ in range(10)
]

double_comp1 = [
    3 * i * j
    for i in range(10)
    for j in range(4)
]

double_comp2 = [
    [i for i in range(7) if i < 5]
    for j in range(10)
]

double_comp3 = {
    i: [i for i in range(7) if i < 5]
    for j in range(10)
    if i < 2
}
```

Note that in the last two comprehensions, the nested comprehensions are not exploded even though
having an if. This is a limitation of `globality-black`, but we believe not very frequent
in everyday cases. If you really want to explode those and make `globality-black` respect it,
please use the feature explained next.

## Partially disable globality-black

If you see some block where you don't want to apply `globality-black`, wrap it
with `# fmt.off` and `# fmt:on` and it will be ignored. Note that this is the same syntax as
for `black`. For example, for readability you might want to do something as:

```
# fmt: off
files_to_read = [
    (f"{key1}_{key2}", key1, key2, key1 + key2)
    for key1 in range(10)
]
# fmt: on
```

Note that as a default (same as `black`), `globality-black` will write the expression above as a
one-liner.

# Pending / Future work
------------

- Explode ternary operators under some criteria
- Nested comprehensions
- Magic comma for single element subscripts, due to [this](https://github.com/psf/black/pull/2942/files#diff-31972cba2ef33b6d8853302bec17d8c60e796566d67ce57e5d233f17a0c6f5a4R17-R18)

Please give us feedback if you find any issues, and check `known_failed`


# Black refresh
--------

`black` is an opinionated Python formatter that tries to save as much vertical space as possible. In
this regard, it compresses lines to the maximum character length that has been configured. `black`'s
default is 88, whereas in `globality-black` we use a default of 100 characters, as agreed for
Globality repos globally. If you want to have a custom max character length, add a `pyproject.toml`
file to the root of your repo. This works the same way as in `black`, and `globality-black` will
take your config from there.

See how `black` works in their [README](https://github.com/psf/black). It is especially useful to
review [this section](https://github.com/psf/black/blob/master/docs/the_black_code_style.md), where
important recent features are explained.

## Magic comma

`black` added a feature at the end of 2020 that we used to call the "magic comma". It's one of the
first examples where `black` is giving a bit of freedom to the developer on how the final code will
look like (apart from `fmt:off` and `fmt:on` to ignore `black` entirely). Read more about it
[here](https://github.com/psf/black/blob/main/docs/the_black_code_style/current_style.md#the-magic-trailing-comma).

# FAQ
---

Here we list a number of questions and solutions raised when presenting this project to other teams:

**I like this project, but this would destroy all our git history and git blames**

Our recommendation is:
 1. Create a big PR for all your repo, and do the effort of reviewing the changes just once.
 1. Add a `.git-blame-ignore-revs` file to your repo, ignoring the bulk commit where
 `globality-black` is applied. See
 [here](https://www.moxio.com/blog/43/ignoring-bulk-change-commits-with-git-blame)
 for more details.

**I like most of the changes, but in some places I really prefer the way I write the code**

No problem, for those specific cases where you like more your style, just wrap the block with
`fmt:off` and `fmt:on`, see the
[Partially disable Globality Black](#partially-disable-globality-black) section.

**100 characters per line is too short / too long for me**

Just add a `pyproject.toml` to the root of your repo (as the one in this very own
project) and specify your preferred length, see the [Black refresh](#black-refresh) section.

**I want to know what will be changed before applying the changes**

Please use the `--diff` option from the CLI, see the [CLI](#cli) section.

**I want to explode list of arguments, but `globality-black` is compressing them into one line**

Please use the magic comma feature, see [Magic comma](#magic-comma).

# Tests

Run the tests as in

```
bash entrypoint.sh test
```
or simply
```
pytest .
```

Some options:
* `-s` to show prints and be able to debug
* `--pdb` to trigger debugger when having an exception
* `pytest route_to_test` to test a specific test file
* `pytest route_to_test::test_function` to test a specific test function
* `pytest route_to_test::test_function[test_case]`
* ` --cov-report term` to show coverage

You might find other code inspectors in `entrypoint.sh`. Note that these are run
against your code if opening a pull request.

# Contributing

All contributions, bug reports, security issues, bug fixes, documentation improvements, enhancements, and ideas are welcome. This section is adapted and simplified
from [pandas contribution guide](https://pandas.pydata.org/docs/development/contributing.html).

## Submit and issue

Bug reports, security issues, and enhancement requests are an important part of making open-source software more stable and are curated through Github issues. When reporting and issue or request, please fill out the issue form fully to ensure others and the core development team can fully understand the scope of the issue.

The issue will then show up to the community and be open to comments/ideas from others.

## Submit a pull request

`deboiler` is hosted on GitHub, and to contribute, you will need to sign up for a free GitHub account. We use Git for version control to allow many people to work together on the project. If you are new to Git, you can reference some of the resources in the pandas contribution guide cited above.

Also, the project follows a standard forking workflow whereby contributors fork the repository, make changes, create a feature branch, push changes, and then create a pull request. To avoid redundancy, please follow all the instructions in the pandas contribution guide  cited above.

## Code of Conduct

As contributors and maintainers to this project, you are expected to abide by the code of conduct. More information can be found at the [Contributor Code of Conduct]((https://github.com/globality-corp/deboiler/.github/blob/master/CODE_OF_CONDUCT.md)).
