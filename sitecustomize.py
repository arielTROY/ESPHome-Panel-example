import dataclasses
from ruamel.yaml.representer import SafeRepresenter

# Generic representer to allow ruamel.yaml to dump dataclass instances
# by converting them to plain dictionaries first. This avoids errors like
# "RepresenterError: cannot represent an object" when a library (e.g. Atopile)
# passes a dataclass object directly to yaml.dump.

def _dataclass_representer(dumper, data):
    """Represent dataclass instances as mappings for YAML."""
    if dataclasses.is_dataclass(data):
        # Convert the dataclass to a simple dict before dumping.
        return dumper.represent_dict(dataclasses.asdict(data))
    # Fallback: represent the object as its string form.
    return dumper.represent_str(str(data))

# Register the representer for *any* unrecognised object. The callback will
# check if the object is a dataclass and handle it accordingly.
SafeRepresenter.add_multi_representer(object, _dataclass_representer)

# Note: Python automatically imports `sitecustomize` (if found on the
# PYTHONPATH) during startup. Adding this file to the repository and ensuring
# that the repository path is present in PYTHONPATH makes the patch effective
# for every Python process started by the CI workflow *before* Atopile is
# imported, eliminating the need for runtime file patching.