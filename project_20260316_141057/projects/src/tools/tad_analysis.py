"""
Tool for TAD (Topologically Associating Domain) analysis of 3D genome data
"""
import cooler
import numpy as np
from scipy import signal
from langchain.tools import tool, ToolRuntime
from typing import Dict, Any, List, Tuple
import os
import json


def calculate_insulation_score(matrix: np.ndarray, window_size: int = 10) -> np.ndarray:
    """
    Calculate insulation score for a contact matrix.

    The insulation score measures the depletion of contacts at a given distance,
    with minima indicating potential TAD boundaries.

    Args:
        matrix: Contact matrix (symmetric)
        window_size: Size of the sliding window (in bins)

    Returns:
        Array of insulation scores
    """
    n = matrix.shape[0]
    insulation = np.zeros(n)

    for i in range(n):
        # Calculate the average contact count in a window around position i
        start = max(0, i - window_size)
        end = min(n, i + window_size)

        # Extract submatrix
        submatrix = matrix[start:end, start:end]

        # Calculate average contact count
        if submatrix.size > 0:
            insulation[i] = np.mean(submatrix)
        else:
            insulation[i] = 0

    return insulation


def find_tad_boundaries(insulation_scores: np.ndarray, threshold: float = 0.5) -> List[int]:
    """
    Find TAD boundaries based on insulation score minima.

    Args:
        insulation_scores: Array of insulation scores
        threshold: Threshold for boundary detection (relative to median)

    Returns:
        List of boundary positions (bin indices)
    """
    # Smooth the insulation scores
    smoothed = signal.savgol_filter(insulation_scores, window_length=11, polyorder=3)

    # Find local minima
    minima_indices = signal.argrelextrema(smoothed, np.less)[0]

    # Filter minima below threshold
    median_score = np.median(smoothed)
    normalized_minima = [idx for idx in minima_indices if smoothed[idx] < median_score * threshold]

    return normalized_minima


def define_tads(boundaries: List[int], matrix_size: int) -> List[Dict[str, Any]]:
    """
    Define TAD regions from boundary positions.

    Args:
        boundaries: List of boundary positions
        matrix_size: Size of the matrix

    Returns:
        List of TAD regions with start and end positions
    """
    tads = []

    # Sort boundaries
    sorted_boundaries = sorted(boundaries)

    # Add start and end if not present
    if not sorted_boundaries or sorted_boundaries[0] != 0:
        sorted_boundaries.insert(0, 0)
    if sorted_boundaries[-1] != matrix_size:
        sorted_boundaries.append(matrix_size)

    # Create TAD regions
    for i in range(len(sorted_boundaries) - 1):
        tads.append({
            "tad_id": i + 1,
            "start_bin": sorted_boundaries[i],
            "end_bin": sorted_boundaries[i + 1],
            "size_bins": sorted_boundaries[i + 1] - sorted_boundaries[i]
        })

    return tads


def calculate_tad_statistics(matrix: np.ndarray, tad: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate statistics for a specific TAD region.

    Args:
        matrix: Contact matrix
        tad: TAD region information

    Returns:
        Dictionary of TAD statistics
    """
    start = tad["start_bin"]
    end = tad["end_bin"]

    # Extract TAD submatrix
    tad_matrix = matrix[start:end, start:end]

    # Calculate statistics
    stats = {
        "tad_id": tad["tad_id"],
        "start_bin": start,
        "end_bin": end,
        "size_bins": end - start,
        "total_contacts": float(np.sum(tad_matrix)),
        "mean_contacts": float(np.mean(tad_matrix)),
        "max_contact": float(np.max(tad_matrix)),
        "internal_contact_ratio": float(np.sum(tad_matrix) / np.sum(matrix)) if np.sum(matrix) > 0 else 0.0,
        "diagonal_enrichment": float(np.mean(np.diag(tad_matrix))) / (float(np.mean(tad_matrix)) + 1e-10)
    }

    return stats


@tool
def analyze_tads(file_path: str, chromosome: str = None, window_size: int = 10, boundary_threshold: float = 0.5, resolution: int = None, runtime: ToolRuntime = None) -> str:
    """
    Perform TAD (Topologically Associating Domain) analysis on a mcool file.

    This tool identifies TAD boundaries and defines TAD regions using insulation score method.

    Args:
        file_path: Path to the mcool file
        chromosome: Chromosome to analyze (e.g., "chr1"). If None, analyzes all chromosomes.
        window_size: Window size for insulation score calculation (in bins)
        boundary_threshold: Threshold for boundary detection (relative to median insulation score)
        resolution: Resolution in base pairs (for multires files)

    Returns:
        A string containing TAD analysis results in JSON format
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

        # Determine which chromosomes to analyze
        chromosomes_to_analyze = [chromosome] if chromosome else clr.chromnames[:5]  # Limit to first 5 chromosomes if not specified

        results = {
            "file_path": file_path,
            "parameters": {
                "window_size": int(window_size),
                "boundary_threshold": float(boundary_threshold),
                "resolution": int(clr.binsize) if resolutions and clr.binsize else None
            },
            "chromosomes": {}
        }

        for chrom in chromosomes_to_analyze:
            # Skip if chromosome doesn't exist
            if chrom not in clr.chromnames:
                results["chromosomes"][chrom] = {
                    "error": f"Chromosome not found"
                }
                continue

            # Get contact matrix for the chromosome (disable balancing to avoid inf/NaN)
            matrix = clr.matrix(sparse=False, balance=False).fetch(chrom)

            # Check for inf/NaN values and replace them
            matrix = np.nan_to_num(matrix, nan=0.0, posinf=0.0, neginf=0.0)

            # Calculate insulation scores
            insulation_scores = calculate_insulation_score(matrix, window_size)

            # Find TAD boundaries
            boundaries = find_tad_boundaries(insulation_scores, boundary_threshold)

            # Define TAD regions
            tads = define_tads(boundaries, matrix.shape[0])

            # Calculate statistics for each TAD
            tad_stats = [calculate_tad_statistics(matrix, tad) for tad in tads]

            # Store results for this chromosome
            results["chromosomes"][chrom] = {
                "chromosome": chrom,
                "matrix_shape": [int(matrix.shape[0]), int(matrix.shape[1])],
                "num_tads": len(tads),
                "boundaries": [int(x) for x in boundaries],
                "tads": [
                    {
                        "tad_id": int(tad.get("tad_id", 0)),
                        "start_bin": int(tad["start_bin"]),
                        "end_bin": int(tad["end_bin"]),
                        "size_bins": int(tad["size_bins"]),
                        "total_contacts": float(tad["total_contacts"]),
                        "mean_contacts": float(tad["mean_contacts"]),
                        "max_contact": float(tad["max_contact"]),
                        "internal_contact_ratio": float(tad["internal_contact_ratio"]),
                        "diagonal_enrichment": float(tad["diagonal_enrichment"])
                    }
                    for tad in tad_stats
                ],
                "insulation_score_stats": {
                    "mean": float(np.mean(insulation_scores)),
                    "std": float(np.std(insulation_scores)),
                    "min": float(np.min(insulation_scores)),
                    "max": float(np.max(insulation_scores))
                }
            }

        return json.dumps(results, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": f"TAD analysis failed: {str(e)}"}, indent=2)
