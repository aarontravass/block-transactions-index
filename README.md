# Relayer Coding Challenge

### Part 1 Solution

For part 1, install all packages in requirements.txt and run the following in the current directory

```commandline
python .\blockNode.py <quicknode-url> <postgres-uri> 18908800-18909050
```

Replace `<quicknode-url>` and `<postgres-uri>` with the values given in the email. (Hidden from public view due to spam)

The Python program uses the following packages
1. requests
2. sqlalchemy

`requests` is used for making HTTP calls and `sqlalchemy` is the ORM.

We first save all blocks to memory and then persist them in the DB.  


### Part 2 Solution

The following SQL statement will fetch the block with max volume:
```sql
SELECT SUM(('x'|| LPAD(SUBSTRING(VALUE, 3, LENGTH(VALUE)), 16, '0')):: BIT(64):: BIGINT) AS volume, 
('x'|| LPAD(SUBSTRING("Transaction"."blockNumber", 3, LENGTH("Transaction"."blockNumber")), 16, '0')):: BIT(64):: BIGINT AS "intBlockNumber"
FROM "Transaction"
INNER JOIN "Block" ON "Block"."blockNumber" = "Transaction"."blockNumber"
WHERE 
"timestamp" >= EXTRACT(EPOCH FROM TIMESTAMP '2024-01-01 00:00:00')*1000 AND 
"timestamp" <= EXTRACT(EPOCH FROM TIMESTAMP '2024-01-01 00:30:00')*1000
GROUP BY "intBlockNumber"
ORDER BY "volume" DESC
LIMIT 1
```

The sql first converts all value to bigint and then uses `sum` as an aggregate function, thus allowing us to perform group by clause on the `blockNumber` column.
We order by the `volume` and then take the first row.

The solution is 

 Volume               | Block Number 
----------------------|--------------
 53883433384695265018 | 18908973     