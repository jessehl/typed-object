# typed-object
A Python class that behaves like a TypeScript Object.

## Set-up
Make sure to add the plugin to MyPy:
```ini
[mypy]
plugins = ./typedobjectplugin.py
```


## Development
```shell
python3 -m mypy typedobject.py --show-traceback
```


