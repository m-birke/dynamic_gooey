import json
from pathlib import Path
from typing import Any, List, Union

import dpath.util
import yaml
from gooey import Gooey, GooeyParser
from jsonpath_ng import jsonpath, parse

ConfigType = Union[dict, list, str, int, float, bool, None]


def render(path: Union[str, Path]) -> Any:
    path = Path(path)

    cfg = _load_cfg(path)

    dygo_params_map = _find_dygo_params(cfg)

    if not dygo_params_map:
        return cfg

    # key: dest, value: node path
    dygo_param_maps_with_dest = {_get_path_target(node_path, cfg)["dest"]: node_path for node_path in dygo_params_map}

    args = _render_gooey(dygo_param_maps_with_dest, cfg)

    for arg_dest in dygo_param_maps_with_dest:
        value = getattr(args, arg_dest)
        _overwrite_map_target(cfg, dygo_param_maps_with_dest[arg_dest], value)

    return cfg


@Gooey
def _render_gooey(dygo_params_map_with_id: dict, cfg: ConfigType):
    parser = GooeyParser(description="TODO allow user to define progr name")

    for param_id in dygo_params_map_with_id:
        arg_params = _get_path_target(dygo_params_map_with_id[param_id], cfg)
        arg_params = _clean_arg_params(arg_params)
        parser.add_argument(**arg_params)

    args = parser.parse_args()
    return args


def _clean_arg_params(arg_params: dict):
    arg_params.pop("dygo")
    return arg_params


def _get_path_target(node_path: str, cfg: ConfigType):
    return dpath.util.get(obj=cfg, glob=node_path, separator=".")


def _overwrite_map_target(cfg: ConfigType, node_path: str, value):
    dpath.util.set(obj=cfg, glob=node_path, value=value, separator=".")


def _find_dygo_params(cfg: ConfigType) -> List[str]:
    """Extracts all paths to dygo params from the config

    :param cfg: loaded config
    :return: list of . separated paths to dygo params
    """
    # this query searches for all 'dygo' keys
    # https://github.com/json-path/JsonPath
    jsonpath_expr: jsonpath.Descendants = parse("$..dygo")
    matches: list[jsonpath.DatumInContext] = jsonpath_expr.find(cfg)

    # .context for parent node
    return [str(match.context.full_path) for match in matches]


def _load_cfg(path: Path) -> ConfigType:

    if path.suffix == ".json":
        with path.open() as file:
            return json.load(file)

    if path.suffix == ".yaml" or path.suffix == ".yml":
        with path.open() as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    raise NotImplementedError(f"File ending {path.suffix} not supported")
