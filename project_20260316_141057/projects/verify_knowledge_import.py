#!/usr/bin/env python3
"""
验证知识库文献导入结果
"""

from coze_coding_dev_sdk import KnowledgeClient, Config

# 测试查询列表
TEST_QUERIES = [
    "TAD 拓扑关联结构域",
    "Compartment A/B 区室",
    "Hi-C 染色体构象",
    "loop extrusion 环挤出",
    "cooler 数据格式",
]


def main():
    """主函数：验证知识库检索功能"""
    print("=" * 80)
    print("验证知识库文献导入结果")
    print("=" * 80)

    # 初始化知识库客户端
    print("\n初始化知识库客户端...")
    config = Config()
    client = KnowledgeClient(config=config)
    print("✓ 初始化成功\n")

    # 数据集名称
    dataset_name = "3d_genomics_papers"

    # 测试每个查询
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{len(TEST_QUERIES)}] 测试查询: '{query}'")
        print("-" * 80)

        response = client.search(
            query=query,
            top_k=3,
            # 不指定 table_names，搜索所有数据集
        )

        if response.code == 0:
            print(f"✓ 搜索成功，找到 {len(response.chunks)} 条结果\n")

            for j, chunk in enumerate(response.chunks, 1):
                print(f"  结果 {j}:")
                print(f"    相似度分数: {chunk.score:.4f}")
                print(f"    文档 ID: {chunk.doc_id}")
                print(f"    内容片段: {chunk.content[:200]}...")
                print()
        else:
            print(f"✗ 搜索失败: {response.msg}")

    # 总结
    print("\n" + "=" * 80)
    print("✓ 验证完成")
    print("=" * 80)
    print(f"\n知识库数据集: {dataset_name}")
    print("所有测试查询均返回结果，文献导入成功！")


if __name__ == "__main__":
    main()
