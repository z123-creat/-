"""
Tool for Compartment analysis of 3D genome data
Compartment analysis identifies A (active) and B (inactive) compartments in the genome
"""
import cooler
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from langchain.tools import tool, ToolRuntime
from typing import Dict, Any, List
import os
import json


def calculate_observed_expected(matrix: np.ndarray) -> np.ndarray:
    """
    Calculate the observed/expected matrix for normalization.

    Args:
        matrix: Contact matrix

    Returns:
        Normalized matrix (observed/expected)
    """
    # Calculate distance dependence
    n = matrix.shape[0]
    distances = np.arange(n)

    # Calculate expected values for each distance
    expected = np.zeros(n)
    for i in range(n):
        expected[i] = np.mean(np.diag(matrix, i))

    # Normalize matrix
    oe_matrix = np.zeros_like(matrix, dtype=float)
    for i in range(n):
        diag_values = np.diag(matrix, i)
        if expected[i] > 0:
            oe_matrix += np.diag(diag_values / expected[i], i)

    return oe_matrix


def calculate_gc_content(bins_data: np.ndarray) -> np.ndarray:
    """
    Calculate GC content from bin data (simplified version).

    In real implementation, this would use actual genomic sequence data.
    Here we use a proxy based on contact patterns.

    Args:
        bins_data: Bin information from cooler

    Returns:
        Array representing GC-like signal
    """
    # This is a simplified proxy - in practice you'd use actual genomic sequences
    # For demo purposes, we use the diagonal signal as a proxy
    return bins_data


def perform_pca(matrix: np.ndarray, n_components: int = 1) -> tuple:
    """
    Perform Principal Component Analysis on the contact matrix.

    Args:
        matrix: Contact matrix
        n_components: Number of principal components to compute

    Returns:
        Tuple of (eigenvectors, eigenvalues)
    """
    # Standardize the data
    scaler = StandardScaler()
    matrix_scaled = scaler.fit_transform(matrix)

    # Perform PCA
    pca = PCA(n_components=n_components)
    eigenvectors = pca.fit_transform(matrix_scaled)
    eigenvalues = pca.explained_variance_

    return eigenvectors, eigenvalues


def assign_compartments(eigenvector: np.ndarray, gc_content: np.ndarray = None) -> np.ndarray:
    """
    Assign compartments (A or B) based on eigenvector values.

    Positive values typically correspond to A (active) compartments,
    negative values to B (inactive) compartments.

    Args:
        eigenvector: First principal component
        gc_content: GC content for correlation (optional)

    Returns:
        Array of compartment assignments (-1 for B, 1 for A)
    """
    # If GC content is available, correlate to determine A vs B
    if gc_content is not None and len(gc_content) == len(eigenvector):
        # Calculate correlation between eigenvector and GC content
        correlation = np.corrcoef(eigenvector.flatten(), gc_content.flatten())[0, 1]

        # If correlation is positive, positive eigenvector = A compartment
        # If correlation is negative, positive eigenvector = B compartment
        if correlation < 0:
            eigenvector = -eigenvector

    # Assign compartments
    compartments = np.where(eigenvector >= 0, 1, -1)

    return compartments


def calculate_compartment_statistics(matrix: np.ndarray, compartments: np.ndarray) -> Dict[str, Any]:
    """
    Calculate statistics for compartments.

    Args:
        matrix: Contact matrix
        compartments: Array of compartment assignments

    Returns:
        Dictionary of compartment statistics
    """
    # Identify A and B compartment bins
    a_bins = np.where(compartments == 1)[0]
    b_bins = np.where(compartments == -1)[0]

    # Calculate intra-compartment contact frequencies
    if len(a_bins) > 0:
        a_submatrix = matrix[np.ix_(a_bins, a_bins)]
        a_contact_mean = np.mean(a_submatrix)
    else:
        a_contact_mean = 0.0

    if len(b_bins) > 0:
        b_submatrix = matrix[np.ix_(b_bins, b_bins)]
        b_contact_mean = np.mean(b_submatrix)
    else:
        b_contact_mean = 0.0

    # Calculate inter-compartment contact frequency
    if len(a_bins) > 0 and len(b_bins) > 0:
        inter_matrix = matrix[np.ix_(a_bins, b_bins)]
        inter_contact_mean = np.mean(inter_matrix)
    else:
        inter_contact_mean = 0.0

    stats = {
        "num_bins": len(compartments),
        "num_a_bins": len(a_bins),
        "num_b_bins": len(b_bins),
        "a_bin_ratio": len(a_bins) / len(compartments) if len(compartments) > 0 else 0.0,
        "b_bin_ratio": len(b_bins) / len(compartments) if len(compartments) > 0 else 0.0,
        "a_compartment_mean_contact": float(a_contact_mean),
        "b_compartment_mean_contact": float(b_contact_mean),
        "inter_compartment_mean_contact": float(inter_contact_mean),
        "compartment_strength": float((a_contact_mean + b_contact_mean) / (2 * inter_contact_mean + 1e-10))
    }

    return stats


@tool
def analyze_compartments(file_path: str, chromosome: str = None, use_gc_correction: bool = True, resolution: int = None, runtime: ToolRuntime = None) -> str:
    """
    Perform compartment analysis on a mcool file to identify A (active) and B (inactive) compartments.

    This tool uses principal component analysis (PCA) to identify compartmentalization patterns
    in the 3D genome organization.

    Args:
        file_path: Path to the mcool file
        chromosome: Chromosome to analyze (e.g., "chr1"). If None, analyzes all chromosomes.
        use_gc_correction: Whether to use GC content correction for compartment assignment
        resolution: Resolution in base pairs (for multires files)

    Returns:
        A string containing compartment analysis results in JSON format
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
                "use_gc_correction": use_gc_correction,
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

            # Normalize matrix (observed/expected)
            oe_matrix = calculate_observed_expected(matrix)

            # Get bin data for GC content proxy
            bins = clr.bins().fetch(chrom)

            # Calculate GC-like content (proxy)
            gc_content = None
            if use_gc_correction:
                # Use diagonal signal as a proxy for GC content
                gc_content = np.diag(oe_matrix)

            # Perform PCA
            eigenvectors, eigenvalues = perform_pca(oe_matrix, n_components=1)

            # Get first principal component
            pc1 = eigenvectors[:, 0]

            # Assign compartments
            compartments = assign_compartments(pc1, gc_content)

            # Calculate statistics
            stats = calculate_compartment_statistics(matrix, compartments)

            # Store results for this chromosome
            results["chromosomes"][chrom] = {
                "chromosome": chrom,
                "matrix_shape": [int(matrix.shape[0]), int(matrix.shape[1])],
                "eigenvalue": float(eigenvalues[0]) if len(eigenvalues) > 0 else 0.0,
                "explained_variance_ratio": float(eigenvalues[0] / np.sum(eigenvalues)) if np.sum(eigenvalues) > 0 else 0.0,
                "compartments": {
                    "assignments": [int(x) if np.isfinite(x) else 0 for x in compartments],
                    "statistics": {
                        "n_A": int(stats.get("n_A", 0)),
                        "n_B": int(stats.get("n_B", 0)),
                        "total_bins": int(stats.get("total_bins", 0)),
                        "ratio_A": float(stats.get("ratio_A", 0.0))
                    }
                },
                "eigenvector": [float(x) if np.isfinite(x) else 0.0 for x in pc1]
            }

        return json.dumps(results, indent=2, ensure_ascii=False)

    except Exception as e:
        import traceback
        error_details = {
            "error": f"Compartment analysis failed: {str(e)}",
            "traceback": traceback.format_exc()
        }
        return json.dumps(error_details, indent=2)
