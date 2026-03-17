"""
Debug script to find the JSON serialization issue
"""
import os
import sys
import json

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

import cooler

file_path = "assets/test.mcool"

# Check if it's a multires mcool file
import h5py
with h5py.File(file_path, 'r') as f:
    resolutions = []
    if 'resolutions' in f.keys():
        res_group = f['resolutions']
        for key in res_group.keys():
            try:
                resolution = int(key)
                resolutions.append(resolution)
            except ValueError:
                continue
    resolutions.sort()

if resolutions:
    default_resolution = resolutions[0]
    full_path = f"{file_path}::/resolutions/{default_resolution}"
    clr = cooler.Cooler(full_path)
    is_multires = True
else:
    clr = cooler.Cooler(file_path)
    is_multires = False
    default_resolution = None

# Get basic information
info = {
    "file_path": file_path,
    "format": "mcool",
    "is_multiresolution": is_multires,
    "available_resolutions": resolutions if is_multires else [],
    "current_resolution": int(default_resolution) if default_resolution else None,
    "chromosomes": clr.chromnames,
    "bins_per_chromosome": {},
    "matrix_shape": {},
    "total_pixels": int(clr.info.get("nbins", 0))
}

# Get chromosome-level information
for chrom in clr.chromnames:
    chrom_bins = clr.bins().fetch(chrom)
    info["bins_per_chromosome"][chrom] = len(chrom_bins)

    # Get matrix shape for this chromosome (disable balancing)
    chrom_matrix = clr.matrix(sparse=False, balance=False).fetch(chrom)
    info["matrix_shape"][chrom] = [int(dim) for dim in chrom_matrix.shape]

# Get resolution (if available)
info["resolution"] = int(clr.binsize) if clr.binsize else None

# Get additional metadata
info["metadata"] = {
    "genome_assembly": clr.info.get("genome-assembly", "unknown"),
    "creation_date": clr.info.get("created-at", "unknown"),
    "nbins": clr.info.get("nbins", 0),
    "nnz": clr.info.get("nnz", 0)
}

print("Info dict:")
for key, value in info.items():
    print(f"  {key}: {type(value)} = {value}")

print("\nTrying to serialize...")
try:
    json_str = json.dumps(info, indent=2, ensure_ascii=False)
    print("Success!")
    print(json_str[:500])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

    # Find problematic values
    def find_numpy_types(obj, path=""):
        if isinstance(obj, dict):
            for key, value in obj.items():
                find_numpy_types(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_numpy_types(item, f"{path}[{i}]")
        else:
            module_name = type(obj).__module__
            if module_name == "numpy":
                print(f"Found numpy type at {path}: {type(obj)} = {obj}")

    print("\nSearching for numpy types...")
    find_numpy_types(info)
