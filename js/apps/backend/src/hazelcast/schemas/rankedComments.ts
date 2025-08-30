import { hazelClient } from "../connect";

export type RankedComment = { __key: string, userId: string, createdAt: number, rootPostId: string }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING ranked_comments (
    __key VARCHAR,
    replyingTo VARCHAR,
    rootPostId VARCHAR,
    createdAt INTEGER,
    userId VARCHAR
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
    'partition-attribute' = 'userId'
)
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS replies_of_user
ON comments ("userId")
TYPE HASH
`);

export const commentSectionsMap = await hazelClient.getMap<string, RankedComment>('ranked_comments');