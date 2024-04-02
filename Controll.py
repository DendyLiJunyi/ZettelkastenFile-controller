import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# 连接到数据库
conn = sqlite3.connect('data_management.db')
cursor = conn.cursor()

# 确保数据表存在
cursor.execute('''CREATE TABLE IF NOT EXISTS data
               (id TEXT PRIMARY KEY, content TEXT, related_ids TEXT)''')

def insert_data(id, content, related_ids):
    """插入数据到数据库"""
    try:
        cursor.execute("INSERT INTO data (id, content, related_ids) VALUES (?, ?, ?)",
                       (id, content, ','.join(related_ids)))
        conn.commit()
        print("数据插入成功")
    except sqlite3.IntegrityError:
        print("错误：ID已存在。")

def search_keyword(keyword):
    """搜索关键词，并显示包含关键词的所有数据的ID和内容"""
    cursor.execute("SELECT id, content FROM data WHERE content LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    if results:
        print("找到包含指定关键词的数据：")
        for id, content in results:
            print(f"ID: {id}, Content: {content}")
    else:
        print("没有找到含有该关键词的数据。")

def delete_data(id):
    """根据ID删除数据"""
    cursor.execute("DELETE FROM data WHERE id = ?", (id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("没有找到ID为 {} 的数据。".format(id))
    else:
        print("ID为 {} 的数据已被删除。".format(id))

def show_all_data():
    """显示所有数据，按字典序排序"""
    cursor.execute("SELECT id, content FROM data ORDER BY id")
    results = cursor.fetchall()
    if results:
        print("所有数据：")
        for id, content in results:
            print(f"ID: {id}, Content: {content}")
    else:
        print("数据库为空。")

def visualize_data_structure():
    """可视化数据结构"""
    cursor.execute("SELECT id, related_ids FROM data")
    rows = cursor.fetchall()
    
    G = nx.DiGraph()  # 创建一个有向图
    for row in rows:
        id = row[0]
        related_ids = row[1].split(',') if row[1] else []
        G.add_node(id)  # 为每个ID添加一个节点
        for related_id in related_ids:
            G.add_edge(id, related_id)  # 添加从id到related_id的边
    
    # 绘制图
    pos = nx.spring_layout(G)  # 为图的节点设置布局
    nx.draw(G, pos, with_labels=True)
    plt.show()  # 显示图


def main():
    while True:
        print("\n请选择操作：")
        print("1. 插入数据")
        print("2. 搜索关键词")
        print("3. 删除数据")
        print("4. 显示所有数据")
        print("5. 显示所有数据联系")
        print("6. 退出")
        choice = input("> ")

        if choice == '1':
            id = input("输入ID: ")
            content = input("输入内容: ")
            related_ids = input("输入相关ID，用逗号分隔: ").split(',')
            insert_data(id, content, related_ids)
        elif choice == '2':
            keyword = input("输入要搜索的关键词: ")
            search_keyword(keyword)
        elif choice == '3':
            id_to_delete = input("输入要删除的数据ID: ")
            delete_data(id_to_delete)
        elif choice == '4':
            show_all_data()
        elif choice == '5':
            visualize_data_structure()
        elif choice == '6':
            print("退出程序。")
            break
        else:
            print("无效的输入，请重新输入。")


if __name__ == "__main__":
    main()

# 不要忘记在程序结束前关闭数据库连接
conn.close()
