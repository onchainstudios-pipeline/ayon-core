# -*- coding: utf-8 -*-
"""Creator plugin for creating textures."""
import os

from openpype.pipeline import CreatedInstance, Creator

from openpype.hosts.substancepainter.api.pipeline import (
    set_project_metadata,
    get_project_metadata
)

from openpype.lib import (
    EnumDef,
    UILabelDef,
    NumberDef
)

import substance_painter.project
import substance_painter.resource


def get_export_presets():
    import substance_painter.resource

    preset_resources = {}

    # TODO: Find more optimal way to find all export templates
    for shelf in substance_painter.resource.Shelves.all():
        shelf_path = os.path.normpath(shelf.path())

        presets_path = os.path.join(shelf_path, "export-presets")
        if not os.path.exists(presets_path):
            continue

        for fname in os.listdir(presets_path):
            if fname.endswith(".spexp"):
                template_name = os.path.splitext(fname)[0]

                resource = substance_painter.resource.ResourceID(
                    context=shelf.name(),
                    name=template_name
                )
                resource_url = resource.url()

                preset_resources[resource_url] = template_name

    # Sort by template name
    export_templates = dict(sorted(preset_resources.items(),
                                   key=lambda x: x[1]))

    return export_templates


class CreateTextures(Creator):
    """Create a texture set."""
    identifier = "io.openpype.creators.substancepainter.textures"
    label = "Textures"
    family = "textures"
    icon = "picture-o"

    default_variant = "Main"

    def create(self, subset_name, instance_data, pre_create_data):

        if not substance_painter.project.is_open():
            return

        instance = self.create_instance_in_context(subset_name, instance_data)
        set_project_metadata("textures", instance.data_to_store())

    def collect_instances(self):
        workfile = get_project_metadata("textures")
        if workfile:
            self.create_instance_in_context_from_existing(workfile)

    def update_instances(self, update_list):
        for instance, _changes in update_list:
            # Update project's metadata
            data = get_project_metadata("textures") or {}
            data.update(instance.data_to_store())
            set_project_metadata("textures", data)

    def remove_instances(self, instances):
        for instance in instances:
            # TODO: Implement removal
            # api.remove_instance(instance)
            self._remove_instance_from_context(instance)

    # Helper methods (this might get moved into Creator class)
    def create_instance_in_context(self, subset_name, data):
        instance = CreatedInstance(
            self.family, subset_name, data, self
        )
        self.create_context.creator_adds_instance(instance)
        return instance

    def create_instance_in_context_from_existing(self, data):
        instance = CreatedInstance.from_existing(data, self)
        self.create_context.creator_adds_instance(instance)
        return instance

    def get_instance_attr_defs(self):

        return [
            EnumDef("exportPresetUrl",
                    items=get_export_presets(),
                    label="Output Template"),
            EnumDef("exportFileFormat",
                    items={
                        None: "Based on output template",
                        # TODO: implement extensions
                    },
                    label="File type"),
            EnumDef("exportSize",
                    items={
                        None: "Based on each Texture Set's size",
                        #  The key is size of the texture file in log2.
                        #  (i.e. 10 means 2^10 = 1024)
                        7: "128",
                        8: "256",
                        9: "512",
                        10: "1024",
                        11: "2048",
                        12: "4096"
                    },
                    label="Size"),

            EnumDef("exportPadding",
                    items={
                        "passthrough": "No padding (passthrough)",
                        "infinite": "Dilation infinite",
                        "transparent": "Dilation + transparent",
                        "color": "Dilation + default background color",
                        "diffusion": "Dilation + diffusion"
                    },
                    label="Padding"),
            NumberDef("exportDilationDistance",
                      minimum=0,
                      maximum=256,
                      decimals=0,
                      default=16,
                      label="Dilation Distance"),
            UILabelDef("Note: Dilation Distance is only used with "
                       "'Dilation + <xxx>' padding options"),
        ]

    def get_pre_create_attr_defs(self):
        # Use same attributes as for instance attributes
        return self.get_instance_attr_defs()
