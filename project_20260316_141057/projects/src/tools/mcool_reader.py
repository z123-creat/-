"""
Tool for reading and parsing mcool files (3D genome Hi-C data format)
"""
import cooler
import numpy as np
import json
from langchain.tools import tool, ToolRuntime
from typing import Dict, Any
import os


def _extract_mcool_info(file_path: str) -> Dict[str, Any]:
    """
    Extract basic information from mcool file
    """
    if not os.path.exists(file_path):
        return {
            "error": f"File not found: {file_path}"
        }

    try:
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
            # This is a multires mcool file
            # Use the highest resolution (smallest bin size)
            default_resolution = resolutions[0]
            full_path = f"{file_path}::/resolutions/{default_resolution}"
            clr = cooler.Cooler(full_path)
            is_multires = True
        else:
            # Single resolution file
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
            "nbins": int(clr.info.get("nbins", 0)),
            "nnz": int(clr.info.get("nnz", 0))
        }

        return info

    except Exception as e:
        return {
            "error": f"Failed to read mcool file: {str(e)}"
        }


@tool
def read_mcool_file(file_path: str, runtime: ToolRuntime = None) -> str:
    """
    Read and parse a mcool file, returning basic information and structure.

    Args:
        file_path: Path to the mcool file

    Returns:
        A string containing the mcool file information in JSON format
    """
    info = _extract_mcool_info(file_path)

    import json
    return json.dumps(info, indent=2, ensure_ascii=False)


@tool
def get_chromosome_matrix(file_path: str, chromosome: str, resolution: int = None, runtime: ToolRuntime = None) -> str:
    """
    Get the contact matrix for a specific chromosome from the mcool file.

    Args:
        file_path: Path to the mcool file
        chromosome: Chromosome name (e.g., "chr1", "chr2")
        resolution: Resolution in base pairs (optional, uses default if not specified)

    Returns:
        A string containing the matrix information and statistics
    """
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File not found: {file_path}"}, indent=2)

    try:
        # Check if it's a multires mcool file
        import h5py
        with h5py.File(file_path, 'r') as f:
            resolutions = []
            if 'resolutions' in f.keys():
                res_group = f['resolutions']
                for key in res_group.keys():
                    try:
                        res = int(key)
                        resolutions.append(res)
                    except ValueError:
                        continue
            resolutions.sort()

        if resolutions:
            # This is a multires mcool file
            target_resolution = resolution if resolution else resolutions[0]

            if target_resolution not in resolutions:
                return json.dumps({
                    "error": f"Resolution {target_resolution} not found. Available resolutions: {resolutions}"
                }, indent=2)

            full_path = f"{file_path}::/resolutions/{target_resolution}"
            clr = cooler.Cooler(full_path)
        else:
            # Single resolution file
            if resolution:
                return json.dumps({
                    "error": f"This is not a multires file, resolution parameter not supported"
                }, indent=2)
            clr = cooler.Cooler(file_path)

        # Validate chromosome exists
        if chromosome not in clr.chromnames:
            return json.dumps({
                "error": f"Chromosome '{chromosome}' not found. Available chromosomes: {clr.chromnames}"
            }, indent=2)

        # Get matrix for the chromosome (disable balancing)
        matrix = clr.matrix(sparse=False, balance=False).fetch(chromosome)

        # Calculate statistics
        stats = {
            "chromosome": chromosome,
            "matrix_shape": [int(dim) for dim in matrix.shape],
            "resolution": int(clr.binsize) if clr.binsize else None,
            "total_contacts": float(np.sum(matrix)),
            "mean_contacts": float(np.mean(matrix)),
            "max_contact": float(np.max(matrix)),
            "min_contact": float(np.min(matrix)),
            "std_contacts": float(np.std(matrix)),
            "nonzero_pixels": int(np.count_nonzero(matrix)),
            "sparsity": float(1.0 - (np.count_nonzero(matrix) / matrix.size))
        }

        import json
        return json.dumps(stats, indent=2, ensure_ascii=False)

    except Exception as e:
        import json
        return json.dumps({"error": f"Failed to get chromosome matrix: {str(e)}"}, indent=2)


@tool
def list_available_resolutions(file_path: str, runtime: ToolRuntime = None) -> str:
    """
    List all available resolutions in a multi-resolution mcool file.

    Args:
        file_path: Path to the mcool file

    Returns:
        A string containing the list of available resolutions
    """
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File not found: {file_path}"}, indent=2)

    try:
        # For mcool files, list all cooler paths and extract resolutions
        import h5py
        resolutions = []

        with h5py.File(file_path, 'r') as f:
            # Check if 'resolutions' group exists (multires mcool format)
            if 'resolutions' in f.keys():
                res_group = f['resolutions']
                for key in res_group.keys():
                    try:
                        # Try to parse as a number (resolution)
                        resolution = int(key)
                        resolutions.append(resolution)
                    except ValueError:
                        # Not a resolution number, skip
                        continue

        resolutions.sort()

        return json.dumps({
            "file_path": file_path,
            "resolutions": resolutions,
            "count": len(resolutions),
            "is_multiresolution": len(resolutions) > 0
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"Failed to list resolutions: {str(e)}"}, indent=2)
