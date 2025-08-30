import { hazelClient } from "../connect";

export type Follow = { __key: string, follower: string, followed: string }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING followers (
    __key VARCHAR,
    follower VARCHAR,
    followed VARCHAR
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
    'partition-attribute' = 'followed'
)
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS followers_of_user
ON followers ("userId")
TYPE HASH
`);

export const followersMap = await hazelClient.getMap<string, Follow>('followers');

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING following (
    __key VARCHAR,
    follower VARCHAR,
    followed VARCHAR
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
    'partition-attribute' = 'follower'
)
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS followed_by_user
ON following ("userId")
TYPE HASH
`);

export const followingMap = await hazelClient.getMap<string, Follow>('following');