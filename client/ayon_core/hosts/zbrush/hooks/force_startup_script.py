# -*- coding: utf-8 -*-
"""Pre-launch to force zbrush startup script."""
import os
import subprocess
from ayon_core.hosts.zbrush import ZBRUSH_HOST_DIR
from ayon_core.lib import get_openpype_execute_args, get_ayon_launcher_args
from ayon_core.lib.applications import PreLaunchHook, LaunchTypes


class ForceStartupScript(PreLaunchHook):
    """Inject AYON environment to Zbrush.

    Note that this works in combination whit Zbrush startup script that
    is creating the environment variable for the AYON Plugin

    Hook `GlobalHostDataHook` must be executed before this hook.
    """
    app_groups = {"zbrush"}
    order = 11
    launch_types = {LaunchTypes.local}

    def execute(self):
        executable_path = self.launch_context.launch_args.pop(0)

        self.launch_context.env["ZBRUSH_EXE"] = executable_path
        self.launch_context.env["AYON_ZBRUSH_CMD"] = subprocess.list2cmdline(
            get_ayon_launcher_args())
        # Pop rest of launch arguments - There should not be other arguments!
        remainders = []
        while self.launch_context.launch_args:
            remainders.append(self.launch_context.launch_args.pop(0))

        new_launch_args = get_openpype_execute_args(
            "run", self.launch_script_path(), executable_path
        )

        # Append as whole list as these areguments should not be separated
        self.launch_context.launch_args.append(new_launch_args)

        startup_args = [
            os.path.join(ZBRUSH_HOST_DIR, "startup", "startup.txt"),
        ]
        self.launch_context.launch_args.append(startup_args)

        if remainders:
            self.log.warning((
                "There are unexpected launch arguments in Zbrush launch. {}"
            ).format(str(remainders)))
            self.launch_context.launch_args.extend(remainders)


    def launch_script_path(self):
        from ayon_core.hosts.zbrush import get_launch_script_path

        return get_launch_script_path()
