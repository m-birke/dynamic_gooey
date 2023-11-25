# `dygo` - Dynamic Gooey

[![PyPI - Version](https://img.shields.io/pypi/v/dygo.svg)](https://pypi.org/project/dygo)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dygo.svg)](https://pypi.org/project/dygo)

-----

**Table of Contents**

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Limitations](#limitations)
- [License](#license)

## About

Dynamic Gooey (`dygo`) ...

1. Parses config files (json or yaml)
1. Extracts values which have to be defined by the user
1. Renders a GUI via [Gooey](https://github.com/chriskiehl/Gooey)
1. Let the user insert the values for the dynamic parameters
1. Inserts the received entries into the config
1. Returns the config

## Installation

```console
pip install dygo
```

## Usage

```python
from dygo import render

my_cfg = render("path/to/jsonORyaml")
```

The dynamic key needs to be inserted as a dict into the config file. The following two examples do the exact same.

- yaml

    ```yaml
    my_dynamic_param:
        dygo: 'dygo'
        dest: 'param1'
    ```

- json

    ```json
    "my_dynamic_param": {"dygo": "dygo", "dest": "param1"},
    ```

The rendered GUI looks like this:

![example](img/example.png)

The dict will be replaced with the value received from the user. Assuming the user entered `abc` for `param1`, the dict afterwards looks like `{"my_dynamic_param": "abc"}`.

Currently the key `dygo` serves as a flag for Dynamic Gooey to detect dynamic parameters (the value is ignored). All other key-value pairs in the `dygo` dict are treated as args for `GooeyParser.add_argument` (see [Gooey](https://github.com/chriskiehl/Gooey) for further documentation). Most important is the `dest` arg whose value will be displayed as a name of the parameter for the user.

## Limitations

Currently `dygo` only descents into dicts, other iterables like lists are yet not supported. This means if a `dygo` parameter has a list in its map path, it is ignored.

## License

`dygo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
