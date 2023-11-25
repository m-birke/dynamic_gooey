from gooey import Gooey, GooeyParser
from pathlib import Path
from typing import Any, Union
import json
import yaml

from typing import Union


def _load_cfg(path: Path):
    
    if path.suffix == ".json":
        with path.open() as file:
            return json.load(file)

    if path.suffix == ".yaml" or path.suffix == ".yml":
        with path.open() as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    raise NotImplementedError(f"File ending {path.suffix} not supported")


def render(path: Union[str, Path]) -> Any:
    path = Path(path)

    cfg = _load_cfg(path)

    dygo_param_maps = _find_dygo_params(cfg)

    if not dygo_param_maps:
        return cfg

    dygo_param_maps_with_dest = {}
    for param_map in dygo_param_maps:
        dest = _get_map_target(param_map, cfg)["dest"]
        dygo_param_maps_with_dest[dest] = param_map

    #print(dygo_param_maps_with_dest)

    args = _render_gooey(dygo_param_maps_with_dest, cfg)

    for arg_dest in dygo_param_maps_with_dest:
        value = getattr(args, arg_dest)
        _overwrite_map_target(cfg, dygo_param_maps_with_dest[arg_dest], value)

    return cfg


def _overwrite_map_target(cfg, map, value):
    temp_target = cfg
    for el in map[:-1]:
        temp_target = temp_target[el]
    temp_target[map[-1]] = value


@Gooey
def _render_gooey(dygo_param_maps_with_id, cfg):
    parser = GooeyParser(description="TODO allow user to define progr name")

    for param_id in dygo_param_maps_with_id:
        arg_params = _get_map_target(dygo_param_maps_with_id[param_id], cfg)
        arg_params = _clean_arg_params(arg_params)
        parser.add_argument(**arg_params)

    args = parser.parse_args()

    return args


def _clean_arg_params(arg_params: dict):
    arg_params.pop("dygo")

    return arg_params


def _get_map_target(map, cfg):
    temp_target = cfg
    for el in map:
        temp_target = temp_target[el]
    return temp_target


def _find_dygo_params(cfg: Any) -> Union[list, bool]:
    if not isinstance(cfg, dict):
        return False

    if cfg.get("dygo", None):
        return True

    maps_to_found_params = []
    for el in cfg:
        res = _find_dygo_params(cfg[el])
        if isinstance(res, bool) and res:
            maps_to_found_params.append([el])

        if isinstance(res, list):
            # here List[List[Any]] is expected
            relative_resolved_mappings = [[el]+res_el for res_el in res]
            maps_to_found_params = maps_to_found_params + relative_resolved_mappings

    return maps_to_found_params
