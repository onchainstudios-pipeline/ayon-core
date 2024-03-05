from ayon_core.client import get_asset_by_name
from ayon_core.pipeline import CreatedInstance
from ayon_core.hosts.tvpaint.api.plugin import TVPaintAutoCreator


class TVPaintWorkfileCreator(TVPaintAutoCreator):
    product_type = "workfile"
    identifier = "workfile"
    label = "Workfile"
    icon = "fa.file-o"

    def apply_settings(self, project_settings):
        plugin_settings = (
            project_settings["tvpaint"]["create"]["create_workfile"]
        )
        self.default_variant = plugin_settings["default_variant"]
        self.default_variants = plugin_settings["default_variants"]

    def create(self):
        existing_instance = None
        for instance in self.create_context.instances:
            if instance.creator_identifier == self.identifier:
                existing_instance = instance
                break

        create_context = self.create_context
        host_name = create_context.host_name
        project_name = create_context.get_current_project_name()
        asset_name = create_context.get_current_asset_name()
        task_name = create_context.get_current_task_name()

        if existing_instance is None:
            existing_asset_name = None
        else:
            existing_asset_name = existing_instance["folderPath"]

        if existing_instance is None:
            asset_doc = get_asset_by_name(project_name, asset_name)
            product_name = self.get_product_name(
                project_name,
                asset_doc,
                task_name,
                self.default_variant,
                host_name
            )
            data = {
                "folderPath": asset_name,
                "task": task_name,
                "variant": self.default_variant
            }

            new_instance = CreatedInstance(
                self.product_type, product_name, data, self
            )
            instances_data = self.host.list_instances()
            instances_data.append(new_instance.data_to_store())
            self.host.write_instances(instances_data)
            self._add_instance_to_context(new_instance)

        elif (
            existing_asset_name != asset_name
            or existing_instance["task"] != task_name
        ):
            asset_doc = get_asset_by_name(project_name, asset_name)
            product_name = self.get_product_name(
                project_name,
                asset_doc,
                task_name,
                existing_instance["variant"],
                host_name,
                existing_instance
            )
            existing_instance["folderPath"] = asset_name
            existing_instance["task"] = task_name
            existing_instance["productName"] = product_name
