"""
Tool for managing 3D genome analysis history using Supabase
"""
from langchain.tools import tool, ToolRuntime
from storage.database.supabase_client import get_supabase_client
from typing import Optional, Dict, Any, cast
import json


@tool
def save_analysis_record(question: str, file_path: str, tad_result: str, compartment_result: str, conclusion: str, is_compliant: bool = True, runtime: ToolRuntime = None) -> str:
    """
    Save an analysis record to the database.

    This tool stores the complete analysis results including question, file path,
    TAD analysis, Compartment analysis, conclusion, and compliance status.

    Args:
        question: The user's question or request
        file_path: Path to the mcool file analyzed
        tad_result: TAD analysis results (JSON string)
        compartment_result: Compartment analysis results (JSON string)
        conclusion: The final analysis conclusion
        is_compliant: Whether the conclusion is compliant/accurate (default: True)

    Returns:
        A string containing the saved record information
    """
    try:
        # Get Supabase client
        client = get_supabase_client()

        # Parse JSON results
        tad_data = json.loads(tad_result) if isinstance(tad_result, str) else tad_result
        compartment_data = json.loads(compartment_result) if isinstance(compartment_result, str) else compartment_result

        # Insert record
        response = client.table('analysis_history').insert({
            "question": question,
            "file_path": file_path,
            "tad_analysis_result": tad_data,
            "compartment_analysis_result": compartment_data,
            "conclusion": conclusion,
            "is_compliant": is_compliant
        }).execute()

        if response.data:
            saved_record: Dict[str, Any] = response.data[0]
            return json.dumps({
                "success": True,
                "message": "Analysis record saved successfully",
                "record_id": saved_record.get("id"),
                "created_at": saved_record.get("created_at")
            }, indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "success": False,
                "error": "Failed to save analysis record",
                "details": response
            }, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "error": f"Invalid JSON format in analysis results: {str(e)}"
        }, indent=2)
    except Exception as e:
        import traceback
        return json.dumps({
            "success": False,
            "error": f"Failed to save analysis record: {str(e)}",
            "traceback": traceback.format_exc()
        }, indent=2)


@tool
def search_analysis_history(query: str = None, file_path: str = None, limit: int = 5, runtime: ToolRuntime = None) -> str:
    """
    Search historical analysis records.

    This tool searches the analysis history for records matching the query or file path.

    Args:
        query: Search query in the question text (optional)
        file_path: Filter by specific file path (optional)
        limit: Maximum number of records to return (default: 5)

    Returns:
        A string containing matching analysis records
    """
    try:
        # Get Supabase client
        client = get_supabase_client()

        # Build query
        db_query = client.table('analysis_history').select('*')

        # Apply filters
        if query:
            db_query = db_query.ilike('question', f'%{query}%')
        if file_path:
            db_query = db_query.eq('file_path', file_path)

        # Order by most recent and limit results
        db_query = db_query.order('created_at', desc=True).limit(limit)

        # Execute query
        response = db_query.execute()

        if response.data:
            # Format results
            results = []
            for item in response.data:
                record = cast(Dict[str, Any], item)
                record_data: Dict[str, Any] = {
                    "id": record.get("id"),
                    "question": record.get("question"),
                    "file_path": record.get("file_path"),
                    "conclusion": record.get("conclusion"),
                    "is_compliant": record.get("is_compliant"),
                    "created_at": record.get("created_at")
                }
                results.append(record_data)

            return json.dumps({
                "success": True,
                "total_records": len(results),
                "records": results
            }, indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "success": True,
                "message": "No matching records found",
                "total_records": 0,
                "records": []
            }, indent=2)

    except Exception as e:
        import traceback
        return json.dumps({
            "success": False,
            "error": f"Failed to search analysis history: {str(e)}",
            "traceback": traceback.format_exc()
        }, indent=2)


@tool
def get_analysis_record(record_id: int, runtime: ToolRuntime = None) -> str:
    """
    Get a specific analysis record by ID.

    Args:
        record_id: The ID of the analysis record to retrieve

    Returns:
        A string containing the complete analysis record
    """
    try:
        # Get Supabase client
        client = get_supabase_client()

        # Get record by ID
        response = client.table('analysis_history').select('*').eq('id', record_id).execute()

        if response.data:
            record = response.data[0]
            return json.dumps({
                "success": True,
                "record": record
            }, indent=2, ensure_ascii=False)
        else:
            return json.dumps({
                "success": False,
                "error": f"Analysis record with ID {record_id} not found"
            }, indent=2)

    except Exception as e:
        import traceback
        return json.dumps({
            "success": False,
            "error": f"Failed to get analysis record: {str(e)}",
            "traceback": traceback.format_exc()
        }, indent=2)
