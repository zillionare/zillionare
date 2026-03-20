---
title: 致命的 ID -- DuckDB 中的 Returning 子句之谜
slug: IDENTITY-The-Mystery-of-the-Returning-Clause
date: 2025-05-14
category: tools
motto: You only live once, but if you do it right, once is enough
img: https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514210946.png
tags: 
    - tools
    - programming
    - AI
    - Augment
    - duckdb
---

Duckdb是一个年轻但非常有潜力的数据库。但它也有桀骜不驯的一面：在一个普通的update语句执行时，出现了罕见的违反外键约束的问题。最终，依靠Augment这个强大的AI工具，我们找到了根本原因，并且通过坚实的实验验证了结论。

『华生，你是否曾思考过，在数据库的深处，隐藏着多少不为人知的秘密？』福尔摩斯放下手中的烟斗，凝视着窗外伦敦的雾霭。

『福尔摩斯，我承认数据库对我而言如同迷宫。』我诚实地回答，我正在记录福尔摩斯最新的冒险。

『今天早晨，一位焦虑的开发者前来求助，他遇到了一个令人费解的谜题。』福尔摩斯从桌上拿起那张写满 SQL 代码的纸条，『他的程序在执行一条看似无害的 UPDATE 语句时，突然抛出了外键约束错误。』

这是建表语句，这里有两张表，resources 和 resource_whitelist。resource_whitelist 表有一个外键引用 resources 表的 id 字段。

```sql
CREATE SEQUENCE if not exists seq_resource_id START WITH 1 INCREMENT BY 1;
CREATE TABLE if not exists resources (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_resource_id'),
    course VARCHAR NOT NULL,
    resource VARCHAR NOT NULL,
    seq INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    UNIQUE (course, rel_path)
);

CREATE SEQUENCE if not exists seq_resource_whitelist_id START WITH 1 INCREMENT BY 1;
CREATE TABLE if not exists resource_whitelist (
    id INTEGER PRIMARY KEY DEFAULT nextval('seq_resource_whitelist_id'),
    resource_id INTEGER NOT NULL,
    course VARCHAR NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),
    UNIQUE (customer_id, resource_id)
);
```

!!! info
    这是修改语句：
    ```sql
    UPDATE resources
            SET seq = ?, title = ?, description = ?, 
            publish_date = ?, price = ?
            WHERE id = ?
            RETURNING id
    ```

『但这有什么奇怪的呢？』我问道，『外键约束不就是为了防止数据不一致吗？』

『我最初也是这么看』。福尔摩斯轻叹一口气，继续说道，『作为一个阅案无数的高手，我几乎立刻就回答了他：这个错误是因为在更新资源时违反了外键约束。错误信息表明 resource_id: 994 仍然被其他表中的外键引用，也就是是 resource_whitelist 表。我甚至还给出了修改方案。』

『但是，这位开发者并没有满足于我的修改方案，而是对我的答案进行了质疑』。福尔摩斯说道。

『质疑我们的福尔摩斯！』我不由得提高了音量。

『不幸的是，我的朋友』，福尔摩斯皱了皱眉，『这位开发者的质疑是有道理的。我的确应该看到更仔细一些，查出背后真正的元凶，再下结论。你知道，巴斯克维尔的猎犬案之后，我一直有点没恢复过来』。

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514205610.png)

巴斯克维尔的猎犬案涉及到一个古老的家族诅咒，传说中有一只巨大的恶魔猎犬在巴斯克维尔家族的领地上出没，专门袭击家族成员。这种超自然的元素使得案件一开始就笼罩在神秘和恐怖的氛围中，让调查变得异常困难，并且一度影响到了福尔摩斯的声誉。对此我完全赞同。

『问题的关键在于，华生』，福尔摩斯轻敲桌面，『这位开发者并未尝试更改任何主键，也没有删除任何记录。他仅仅是更新了一些无关紧要的字段，比如标题或描述。』

『那么，为什么会触发外键约束错误呢？』

『正是这一点引起了我的兴趣！』福尔摩斯站起身来，开始在房间里踱步，『我们面对的是 DuckDB，一个年轻而有趣的数据库系统。错误信息中提到了'foreign key limitations'，这暗示着某种不寻常的行为。』

『你有什么理论吗，福尔摩斯？』

『我设计了一个实验，华生。』福尔摩斯拿出一张写满代码的纸，三个简单的测试案例，足以揭示真相。』

我凑近看了看那些 Python 代码，『看起来很复杂。』

```python
import duckdb
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 创建测试数据库
conn = duckdb.connect(':memory:')

# 创建测试表结构
conn.execute(『『『
CREATE TABLE parent (
    id INTEGER PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE child (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    data VARCHAR,
    FOREIGN KEY (parent_id) REFERENCES parent(id)
);
『『『)

# 插入测试数据
conn.execute(『INSERT INTO parent VALUES (1, 'Parent 1'), (2, 'Parent 2')『)
conn.execute(『INSERT INTO child VALUES (101, 1, 'Child 1'), (102, 2, 'Child 2')『)

# 测试 1: 正常更新非键字段
try:
    logger.info(『测试 1: 更新 parent 表的非键字段『)
    conn.execute(『UPDATE parent SET name = 'Updated Parent 1' WHERE id = 1『)
    logger.info(『测试 1 成功：可以更新非键字段『)
except Exception as e:
    logger.error(f『测试 1 失败：{e}『)

# 测试 2: 使用 RETURNING 子句更新
try:
    logger.info(『测试 2: 使用 RETURNING 子句更新『)
    result = conn.execute(『UPDATE parent SET name = 'Updated Again' WHERE id = 1 RETURNING id『).fetchall()
    logger.info(f『测试 2 成功：RETURNING 子句返回：{result}『)
except Exception as e:
    logger.error(f『测试 2 失败：{e}『)

# 测试 3: 尝试更新被引用的主键
try:
    logger.info(『测试 4: 尝试更新被引用的主键『)
    conn.execute(『UPDATE parent SET id = 3 WHERE id = 1『)
    logger.info(『测试 4 成功：可以更新被引用的主键『)
except Exception as e:
    logger.error(f『测试 4 失败：{e}『)
    if 『foreign key『 in str(e).lower():
        logger.info(『确认：更新被引用的主键会触发外键约束错误『)

# 显示最终数据
parent_data = conn.execute(『SELECT * FROM parent『).fetchall()
child_data = conn.execute(『SELECT * FROM child『).fetchall()
logger.info(f『最终 parent 表数据：{parent_data}『)
logger.info(f『最终 child 表数据：{child_data}『)
```

『表面上看是如此。但真相往往隐藏在细节之中。』福尔摩斯微笑道，『第一个测试是普通的 UPDATE 操作，没有任何特殊子句。第二个测试添加了一个 RETURNING 子句。第三个测试则直接尝试更新被引用的主键。』

『结果如何？』

『啊，华生，结果令人着迷！『福尔摩斯的眼睛闪烁着兴奋的光芒，『第一个测试完美通过，证明普通的 UPDATE 操作可以正常工作。第三个测试如预期般失败，因为它确实违反了外键约束。』

『那么第二个测试呢？』

『第二个测试失败了，『福尔摩斯停顿了一下，『但第二个测试，华生，第二个测试揭示了真相！』

『怎么说？』

『带有 RETURNING 子句的 UPDATE 操作触发了外键约束错误，尽管它只是更新了非键字段！『福尔摩斯高声宣布，『这证明 DuckDB 在处理带 RETURNING 子句的 UPDATE 操作时，采用了不同的执行路径。它很可能在内部将 UPDATE 实现为'先 DELETE 再 INSERT'的组合操作！』

『太不可思议了，福尔摩斯！』

『初看之下，这似乎是个 bug。但从更深层次看，这是 DuckDB 实现细节的一个特性。『福尔摩斯重新坐下，『当使用 RETURNING 子句时，DuckDB 需要返回受影响行的信息。为了实现这一点，它可能选择了一种不同的执行策略，这种策略会触发完整的外键约束检查。』

『等一下！』我小声地喊起来，『这里还因为 resource 的主键是自增的！所以，当删除原记录，再新增记录时，尽管记录的语义没有改变，但它们的 id 字段却意外更新了』。

『你说得很对！』福尔摩斯微笑着说。

『那么解决方案是什么？』

『简单明了，华生。『福尔摩斯微笑着说，『要么避免在有外键引用的表上使用 RETURNING 子句，要么采用两步操作：先查询，再更新。』

『福尔摩斯，你总是能找到最简单的解决方案。』

『在数据库的世界里，华生，表面上看似简单的操作背后，往往隐藏着复杂的实现细节。』福尔摩斯拿起小提琴，拉出一段欢快的旋律，正如福尔摩斯常说：排除所有不可能的情况后，剩下的，无论多么不可思议，一定就是真相。

『那么这个案例可以称为什么呢？』我问道，准备为新的笔记命名。

『就叫它'RETURNING 子句之谜'吧，华生。』福尔摩斯微笑着回答，『一个小小的 SQL 子句，揭示了数据库引擎深处的秘密。』

窗外，伦敦的雾气渐渐散去，又一个数据库之谜被成功破解。
