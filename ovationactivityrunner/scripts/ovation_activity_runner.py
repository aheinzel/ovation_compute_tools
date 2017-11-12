#!/usr/bin/env python3

import sys
import os
import subprocess
from tempfile import mkdtemp
import ovation.session as session
import ovation.core as core
import ovation.activities as activities
import ovation.contents as contents
import ovation.download as download
import ovation.session as session


DATA_ROOT="/tmp/data_root"


def _find_activities(s):
    projects = core.get_projects(s)
    for p in projects:
        rel = core.get_entity(s, p._id).relationships
        if "activities" in rel:
            yield from s.get(rel.activities.related)

            
def _filter_open_activities(s, activities):
    return filter(lambda _: len(s.get(_.relationships.outputs.related)) == 0, activities)


def _run_activity(download_dir):
    try:
        output = subprocess.check_output(["execute_ovation_activity.sh", download_dir], stderr = subprocess.STDOUT, universal_newlines = True)
        status = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        status = e.returncode

    return (output,status)


def _process_activity(s, activity):
    download_dir = mkdtemp()
    download.download_activity(s, activity, download_dir)
    output, status = _run_activity(download_dir)
    outputs_folder = os.path.join(download_dir, "outputs")
    _write_file(os.path.join(outputs_folder, "execution.log"), output)
    output_files = _find_files(outputs_folder)
    activities.add_outputs(s, activity, output_files)


def _write_file(fn, content):
    with open(fn, "w") as f:
        f.write(content)

        
def _find_files(root):
    return [ os.path.join(l[0], f) for l in os.walk(root) for f in l[2] ]


def process_open_activities(user_name):
    s = session.connect(user_name)
    open_activities = _filter_open_activities(s, _find_activities(s))
    for activity in open_activities:
        print("Processing {}".format(activity.attributes.name))
        _process_activity(s, activity)
        print("Finished processing {}".format(activity.attributes.name))


        
def main():
    if len(sys.argv) != 2:
        print("USAGE: {} user_name".format(sys.argv[0]), file = sys.stderr)
        sys.exit(1)

    user_name = sys.argv[1]
    process_open_activities(user_name)

if __name__ == "__main__":
    main()
