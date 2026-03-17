#!/usr/bin/env python3
"""
将三维基因组学领域的 PDF 文献导入知识库
"""

import os
import sys
from pathlib import Path

# 添加项目路径到 PythonPATH
sys.path.insert(0, os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects"), "src"))

from coze_coding_dev_sdk import KnowledgeClient, Config, KnowledgeDocument, DataSourceType
from coze_coding_dev_sdk.s3 import S3SyncStorage
from coze_coding_utils.runtime_ctx.context import Context

# 要导入的 PDF 文件列表（用户指定的 10 篇文献）
PDF_FILES = [
    "1511 PNAS - loop extrusion.pdf",
    "1906 COCEBI - compartment  and loop mechanism Review.pdf",
    "1912 Nat.Rev.Gen - 3D chromosome Review.pdf",
    "2001 - 基于生物信息学的Hi_C研究现状与发展趋势.pdf",
    "2004 - 探索染色质三维构象的工具箱研究进展_林达.pdf",
    "2302 NC - POSSUMM compartment.pdf",
    "2308 BIB - HiC pattern tools.pdf",
    "2411 Adv.Sci - AutoBA.pdf",
    "2412 GB - HTAD.pdf",
    "2509 NC - scHiC embedding tools.pdf",
]

# 数据集名称
DATASET_NAME = "3d_genomics_papers"

# 工作目录
WORKSPACE_PATH = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
ASSETS_DIR = os.path.join(WORKSPACE_PATH, "assets")


def main():
    """主函数：导入 PDF 文献到知识库"""
    print("=" * 80)
    print("开始导入三维基因组学文献到知识库")
    print("=" * 80)

    # 1. 初始化对象存储客户端
    print("\n[1/3] 初始化对象存储客户端...")
    storage = S3SyncStorage(
        endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
        access_key="",
        secret_key="",
        bucket_name=os.getenv("COZE_BUCKET_NAME"),
        region="cn-beijing",
    )
    print("✓ 对象存储客户端初始化成功")

    # 2. 初始化知识库客户端
    print("\n[2/3] 初始化知识库客户端...")
    config = Config()
    knowledge_client = KnowledgeClient(config=config)
    print("✓ 知识库客户端初始化成功")

    # 3. 上传并导入每个 PDF 文件
    print(f"\n[3/3] 开始处理 {len(PDF_FILES)} 个 PDF 文件...")
    print("-" * 80)

    uploaded_keys = []
    import_errors = []

    for i, pdf_filename in enumerate(PDF_FILES, 1):
        pdf_path = os.path.join(ASSETS_DIR, pdf_filename)

        print(f"\n[{i}/{len(PDF_FILES)}] 处理文件: {pdf_filename}")

        # 检查文件是否存在
        if not os.path.exists(pdf_path):
            print(f"  ✗ 文件不存在，跳过: {pdf_path}")
            import_errors.append((pdf_filename, "文件不存在"))
            continue

        try:
            # 步骤 1: 上传 PDF 到对象存储
            print(f"  → 上传到对象存储...")
            with open(pdf_path, "rb") as f:
                storage_key = storage.stream_upload_file(
                    fileobj=f,
                    file_name=f"3d_genomics_papers/{pdf_filename}",
                    content_type="application/pdf",
                )
            print(f"  ✓ 上传成功，Key: {storage_key}")
            uploaded_keys.append((pdf_filename, storage_key))

            # 步骤 2: 导入到知识库（使用 URI 类型）
            print(f"  → 导入到知识库...")
            doc = KnowledgeDocument(
                source=DataSourceType.URI,
                raw_data=storage_key,  # 使用对象存储的 key
                metadata={"filename": pdf_filename, "type": "3d_genomics_paper"}
            )

            response = knowledge_client.add_documents(
                documents=[doc],
                table_name=DATASET_NAME,
            )

            if response.code == 0:
                print(f"  ✓ 导入成功，文档 ID: {response.doc_ids[0]}")
            else:
                print(f"  ✗ 导入失败: {response.msg}")
                import_errors.append((pdf_filename, response.msg))

        except Exception as e:
            print(f"  ✗ 处理失败: {str(e)}")
            import_errors.append((pdf_filename, str(e)))

    # 4. 输出结果摘要
    print("\n" + "=" * 80)
    print("导入完成！结果摘要：")
    print("=" * 80)
    print(f"\n总计文件数: {len(PDF_FILES)}")
    print(f"成功导入: {len(PDF_FILES) - len(import_errors)}")
    print(f"失败数量: {len(import_errors)}")

    if import_errors:
        print("\n❌ 失败文件列表：")
        for filename, error in import_errors:
            print(f"  - {filename}: {error}")

    print("\n✓ 上传的对象存储 Key 列表：")
    for filename, key in uploaded_keys:
        print(f"  - {filename}: {key}")

    print("\n" + "=" * 80)
    print(f"✓ 文献已导入到知识库数据集: {DATASET_NAME}")
    print("=" * 80)


if __name__ == "__main__":
    main()
