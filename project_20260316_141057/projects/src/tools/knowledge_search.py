"""
Tool for searching the 3D genomics literature knowledge base
"""
from coze_coding_dev_sdk import KnowledgeClient, Config
from langchain.tools import tool, ToolRuntime
from typing import List, Dict, Any
import json


@tool
def search_literature(query: str, top_k: int = 5, min_score: float = 0.0, runtime: ToolRuntime = None) -> str:
    """
    Search the 3D genomics literature knowledge base for relevant information.

    This tool searches through imported scientific papers to find relevant information
    for validating analysis conclusions.

    Args:
        query: Search query describing the information you're looking for
        top_k: Number of top results to return (default: 5)
        min_score: Minimum similarity score threshold (0.0-1.0, default: 0.0)

    Returns:
        A string containing search results with relevant literature excerpts
    """
    try:
        # Initialize knowledge client
        config = Config()
        client = KnowledgeClient(config=config)

        # Perform search
        # Note: We don't specify table_names to search all datasets
        response = client.search(
            query=query,
            top_k=top_k,
            min_score=min_score
        )

        if response.code != 0:
            return json.dumps({
                "error": f"Knowledge search failed: {response.msg}"
            }, indent=2)

        # Format results
        results = []
        for i, chunk in enumerate(response.chunks):
            results.append({
                "rank": i + 1,
                "score": float(chunk.score),
                "content": chunk.content,
                "doc_id": chunk.doc_id
            })

        output = {
            "query": query,
            "total_results": len(results),
            "results": results
        }

        return json.dumps(output, indent=2, ensure_ascii=False)

    except Exception as e:
        import traceback
        return json.dumps({
            "error": f"Knowledge search error: {str(e)}",
            "traceback": traceback.format_exc()
        }, indent=2)


@tool
def get_literature_context(topic: str, context_size: int = 3, runtime: ToolRuntime = None) -> str:
    """
    Get relevant literature context for a specific topic.

    This tool searches for literature related to a specific topic and returns
    a concise summary of the findings.

    Args:
        topic: The topic you want literature context for (e.g., "TAD boundary detection")
        context_size: Number of literature excerpts to retrieve (default: 3)

    Returns:
        A string containing summarized literature context
    """
    try:
        # Initialize knowledge client
        config = Config()
        client = KnowledgeClient(config=config)

        # Perform search
        response = client.search(
            query=topic,
            top_k=context_size,
            min_score=0.6  # Higher threshold for more relevant results
        )

        if response.code != 0:
            return json.dumps({
                "error": f"Knowledge search failed: {response.msg}"
            }, indent=2)

        if len(response.chunks) == 0:
            return json.dumps({
                "topic": topic,
                "message": "No relevant literature found for this topic"
            }, indent=2)

        # Compile context from multiple sources
        context = {
            "topic": topic,
            "summary": f"Found {len(response.chunks)} relevant literature excerpts",
            "excerpts": []
        }

        for i, chunk in enumerate(response.chunks):
            context["excerpts"].append({
                "source_id": chunk.doc_id,
                "relevance_score": float(chunk.score),
                "content": chunk.content[:500] + "..." if len(chunk.content) > 500 else chunk.content
            })

        return json.dumps(context, indent=2, ensure_ascii=False)

    except Exception as e:
        import traceback
        return json.dumps({
            "error": f"Failed to get literature context: {str(e)}",
            "traceback": traceback.format_exc()
        }, indent=2)
