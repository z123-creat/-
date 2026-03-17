"""
Setup script: Upload PDF documents to knowledge base
"""
from coze_coding_dev_sdk.fetch import FetchClient
from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType
from coze_coding_utils.runtime_ctx.context import Context

# Initialize clients (Context is optional)
fetch_client = FetchClient()
knowledge_config = Config()
knowledge_client = KnowledgeClient(config=knowledge_config)

# PDF URLs
pdf_urls = [
    {
        "title": "Science - HiC",
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F0910+Science+-+HiC.pdf&nonce=51e23611-15d3-4aaa-86fe-9c7ad043f02c&project_id=7615111316956725248&sign=78b229fc328438b6b5498b213c490d80cbe724929df314efae3ddd64fee3cbda"
    },
    {
        "title": "Nature - TAD",
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F1204+Nature+-+TAD.pdf&nonce=dbdf7a8c-f00c-4a98-a91c-1c2723df9b4a&project_id=7615111316956725248&sign=06ea1c5d3e1f6f81c9b1aae415d7e04ef14a570e00125990afdac94bd1a2741a"
    },
    {
        "title": "Cell - insitu HiC Loop",
        "url": "https://code.coze.cn/api/sandbox/coze_coding/file/proxy?expire_time=-1&file_path=assets%2F1412+Cell+-+insitu+HiC+Loop.pdf&nonce=1ba1d776-8b37-4707-9e5a-9ad79ced0590&project_id=7615111316956725248&sign=81dac17035f9ff93360101beba37721a1709c8875700a2797c5bcaa144da9217"
    }
]

def upload_pdf_to_knowledge(pdf_info):
    """Fetch PDF content and upload to knowledge base"""
    print(f"Processing: {pdf_info['title']}")

    # Fetch PDF content
    try:
        response = fetch_client.fetch(url=pdf_info['url'])

        if response.status_code != 0:
            print(f"  ❌ Failed to fetch: {response.status_message}")
            return False

        # Extract text content
        text_content = "\n".join(
            item.text for item in response.content if item.type == "text"
        )

        if not text_content:
            print(f"  ⚠️  No text content found")
            return False

        print(f"  ✓ Fetched {len(text_content)} characters")

        # Upload to knowledge base
        doc = KnowledgeDocument(
            source=DataSourceType.TEXT,
            raw_data=text_content,
            metadata={
                "title": pdf_info['title'],
                "source": pdf_info['url'],
                "type": "scientific_paper"
            }
        )

        kb_response = knowledge_client.add_documents(
            documents=[doc],
            table_name="3d_genomics_literature"
        )

        if kb_response.code == 0:
            print(f"  ✓ Uploaded to knowledge base: {kb_response.doc_ids}")
            return True
        else:
            print(f"  ❌ Failed to upload: {kb_response.msg}")
            return False

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("Setting up 3D Genomics Literature Knowledge Base")
    print("=" * 60)
    print()

    success_count = 0
    for pdf_info in pdf_urls:
        if upload_pdf_to_knowledge(pdf_info):
            success_count += 1
        print()

    print("=" * 60)
    print(f"Summary: {success_count}/{len(pdf_urls)} documents uploaded")
    print("=" * 60)

if __name__ == "__main__":
    main()
