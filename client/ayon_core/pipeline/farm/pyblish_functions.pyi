import pyblish.api
from ayon_core.pipeline import Anatomy
from typing import Tuple, Union, List


class TimeData:
    start: int
    end: int
    fps: float | int
    step: int
    handle_start: int
    handle_end: int

    def __init__(self, start: int, end: int, fps: float | int, step: int, handle_start: int, handle_end: int):
        ...
    ...

def remap_source(source: str, anatomy: Anatomy): ...
def extend_frames(folder_path: str, product_name: str, start: int, end: int) -> Tuple[int, int]: ...
def get_time_data_from_instance_or_context(instance: pyblish.api.Instance) -> TimeData: ...
def get_transferable_representations(instance: pyblish.api.Instance) -> list: ...
def create_skeleton_instance(instance: pyblish.api.Instance, families_transfer: list = ..., instance_transfer: dict = ...) -> dict: ...
def create_instances_for_aov(instance: pyblish.api.Instance, skeleton: dict, aov_filter: dict) -> List[pyblish.api.Instance]: ...
def attach_instances_to_product(attach_to: list, instances: list) -> list: ...
