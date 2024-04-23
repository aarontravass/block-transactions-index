SELECT SUM(('x'|| LPAD(SUBSTRING(VALUE, 3, LENGTH(VALUE)), 16, '0')):: BIT(64):: BIGINT) AS volume, 
('x'|| LPAD(SUBSTRING("Transaction"."blockNumber", 3, LENGTH("Transaction"."blockNumber")), 16, '0')):: BIT(64):: BIGINT AS "intBlockNumber"
FROM "Transaction"
INNER JOIN "Block" ON "Block"."blockNumber" = "Transaction"."blockNumber"
WHERE 
"timestamp" >= EXTRACT(EPOCH
FROM TIMESTAMP '2024-01-01 00:00:00')*1000 AND 
"timestamp" <= EXTRACT(EPOCH
FROM TIMESTAMP '2024-01-01 00:30:00')*1000
GROUP BY "intBlockNumber"
ORDER BY "volume" DESC
LIMIT 1