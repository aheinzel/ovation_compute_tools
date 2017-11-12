from distutils.core import setup

setup(
    name = "OvationActivityRunner",
    version = "0.1poc",
    install_requires = ["ovation"],
    scripts = ["scripts/execute_ovation_activity.sh", "scripts/ovation_activity_runner.py"]
)
