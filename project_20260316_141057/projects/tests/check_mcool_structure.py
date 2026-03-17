"""
Check the structure of test.mcool file
"""
import h5py
import json

file_path = "assets/test.mcool"

print(f"Checking structure of {file_path}")
print("=" * 60)

with h5py.File(file_path, 'r') as f:
    print("\nTop-level keys:")
    for key in f.keys():
        print(f"  - {key}: {type(key)} = {repr(key)}")

    print("\nTrying to parse as numbers:")
    for key in f.keys():
        try:
            num = int(key)
            print(f"  - {key} -> {num} ✓")
        except ValueError:
            print(f"  - {key} -> not a number ✗")

    print("\nLooking for 'resolutions' group:")
    if 'resolutions' in f.keys():
        print("  Found 'resolutions' group!")
        res_group = f['resolutions']
        print(f"  Keys in resolutions: {list(res_group.keys())}")

    print("\nAll groups in file:")
    def visit_func(name, obj):
        if isinstance(obj, h5py.Group):
            print(f"  Group: {name}")
    f.visititems(visit_func)

print("\n" + "=" * 60)
print("Done!")
