---
title: "DuckDB RETURNING Clause: The Hidden Foreign Key Trap"
date: 2025-05-14
slug: en/posts/tools/致命的ID-DuckDB中的Returning子句之谜
tags: [Duckdb, Sql, Database, Debugging]
excerpt: "DuckDB’s RETURNING clause in UPDATE statements can unexpectedly trigger foreign key violations. This article details the root cause—internal DELETE/INSERT logic—and provides verified workarounds for safe usage."
lang: en
translation_of: posts/tools/致命的ID-DuckDB中的Returning子句之谜
auto_translated: true
source_sha: 4401a74aa01d34e45f581c4e65c130d9ab050fd9
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514210946.png"
---

DuckDB is a young but highly promising database. Yet, it has a rebellious side: a rare foreign key constraint violation occurred during a standard `UPDATE` statement execution. Relying on Augment, a powerful AI tool, we identified the root cause and validated our conclusions through rigorous experimentation.

‘Watson, have you ever pondered how many hidden secrets lie deep within a database?’ Sherlock Holmes put down his pipe, gazing out at the foggy London window.

‘Holmes, I admit the database is like a maze to me,’ I replied honestly, recording Holmes’s latest adventure.

‘This morning, an anxious developer sought help with a baffling puzzle,’ Holmes said, picking up a note filled with SQL code. ‘His program threw a foreign key constraint error while executing a seemingly harmless `UPDATE` statement.’

Here are the table creation statements. There are two tables: `resources` and `resource_whitelist`. The `resource_whitelist` table has a foreign key referencing the `id` field in the `resources` table.

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
    Here is the modification statement:
    ```sql
    UPDATE resources
            SET seq = ?, title = ?, description = ?, 
            publish_date = ?, price = ?
            WHERE id = ?
            RETURNING id
    ```

‘But what’s strange about that?’ I asked. ‘Aren’t foreign key constraints there to prevent data inconsistency?’

‘I initially thought so too,’ Holmes sighed. ‘As a seasoned detective, I almost immediately answered him: the error occurred because the resource update violated the foreign key constraint. The error message indicated that `resource_id: 994` was still referenced by a foreign key in another table, specifically `resource_whitelist`. I even provided a fix.’

‘However, this developer was not satisfied with my fix and questioned my answer,’ Holmes said.

‘Questioning Holmes!’ I raised my voice involuntarily.

‘Unfortunately, my friend,’ Holmes frowned, ‘this developer’s skepticism was justified. I should have looked more carefully, identified the real culprit behind the scenes, and drawn conclusions. You know, after the *Hound of the Baskervilles*, I’ve been a bit off my game.’

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/05/20250514205610.png)

The *Hound of the Baskervilles* involves an ancient family curse, where a giant demonic hound is said to roam the Baskerville estate, targeting family members. This supernatural element shrouded the case in mystery and terror from the start, making the investigation exceptionally difficult and temporarily damaging Holmes’s reputation. I completely agree.

‘The key to the problem, Watson,’ Holmes tapped the desk lightly, ‘is that this developer did not attempt to change any primary keys or delete any records. He merely updated some inconsequential fields, such as the title or description.’

‘Then why did it trigger a foreign key constraint error?’

‘That is exactly what piqued my interest!’ Holmes stood up and began pacing around the room. ‘We are dealing with DuckDB, a young and intriguing database system. The error message mentioned “foreign key limitations,” hinting at some unusual behavior.’

‘Do you have a theory, Holmes?’

‘I designed an experiment, Watson,’ Holmes said, pulling out a sheet of code. ‘Three simple test cases are sufficient to reveal the truth.’

I leaned in to look at the Python code. ‘It looks complicated.’

```python
import duckdb
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create test database
conn = duckdb.connect(':memory:')

# Create test table structures
conn.execute('''
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
''')

# Insert test data
conn.execute('INSERT INTO parent VALUES (1, 'Parent 1'), (2, 'Parent 2')')
conn.execute('INSERT INTO child VALUES (101, 1, 'Child 1'), (102, 2, 'Child 2')')

# Test 1: Normal update of non-key fields
try:
    logger.info('Test 1: Updating non-key fields of parent table')
    conn.execute('UPDATE parent SET name = 'Updated Parent 1' WHERE id = 1')
    logger.info('Test 1 Success: Non-key fields can be updated')
except Exception as e:
    logger.error(f'Test 1 Failed: {e}')

# Test 2: Update using RETURNING clause
try:
    logger.info('Test 2: Update using RETURNING clause')
    result = conn.execute('UPDATE parent SET name = 'Updated Again' WHERE id = 1 RETURNING id').fetchall()
    logger.info(f'Test 2 Success: RETURNING clause returned: {result}')
except Exception as e:
    logger.error(f'Test 2 Failed: {e}')

# Test 3: Attempt to update the referenced primary key
try:
    logger.info('Test 4: Attempting to update the referenced primary key')
    conn.execute('UPDATE parent SET id = 3 WHERE id = 1')
    logger.info('Test 4 Success: Referenced primary key can be updated')
except Exception as e:
    logger.error(f'Test 4 Failed: {e}')
    if 'foreign key' in str(e).lower():
        logger.info('Confirmed: Updating the referenced primary key triggers a foreign key constraint error')

# Display final data
parent_data = conn.execute('SELECT * FROM parent').fetchall()
child_data = conn.execute('SELECT * FROM child').fetchall()
logger.info(f'Final parent table data: {parent_data}')
logger.info(f'Final child table data: {child_data}')
```

‘On the surface, it seems so. But the truth often lies in the details,’ Holmes smiled. ‘The first test is a standard `UPDATE` operation with no special clauses. The second test adds a `RETURNING` clause. The third test directly attempts to update the referenced primary key.’

‘What were the results?’

‘Ah, Watson, the results are fascinating!’ Holmes’s eyes sparkled with excitement. ‘The first test passed perfectly, proving that standard `UPDATE` operations work normally. The third test failed as expected, as it indeed violated the foreign key constraint.’

‘Then what about the second test?’

‘The second test failed,’ Holmes paused. ‘But the second test, Watson, the second test reveals the truth!’

‘How so?’

‘The `UPDATE` operation with the `RETURNING` clause triggered a foreign key constraint error, even though it only updated non-key fields!’ Holmes announced loudly. ‘This proves that DuckDB adopts a different execution path when handling `UPDATE` operations with the `RETURNING` clause. It likely implements the `UPDATE` internally as a combination of “DELETE then INSERT”!’

‘Incredible, Holmes!’

‘At first glance, this might seem like a bug. But from a deeper perspective, it is a feature of DuckDB’s implementation details,’ Holmes sat back down. ‘When using the `RETURNING` clause, DuckDB needs to return information about the affected rows. To achieve this, it may choose a different execution strategy that triggers a full foreign key constraint check.’

‘Wait a minute!’ I whispered. ‘This is also because the `resource` primary key is auto-incrementing! So, when deleting the original record and inserting a new one, although the record’s semantics remain unchanged, their `id` field unexpectedly updates.’

‘You are quite right!’ Holmes smiled.

‘So, what is the solution?’

‘Simple and clear, Watson,’ Holmes smiled. ‘Either avoid using the `RETURNING` clause on tables with foreign key references, or adopt a two-step operation: query first, then update.’

‘Holmes, you always find the simplest solution.’

‘In the world of databases, Watson, operations that seem simple on the surface often hide complex implementation details,’ Holmes picked up his violin and played a cheerful melody. Just as Holmes often said: when you have eliminated the impossible, whatever remains, however improbable, must be the truth.

‘So, what should we call this case?’ I asked, preparing to name the new note.

‘Let’s call it “The Mystery of the RETURNING Clause,” Watson,’ Holmes replied with a smile. ‘A small SQL clause reveals the secrets deep within the database engine.’

Outside the window, the London fog gradually dispersed, and another database mystery was successfully solved.
