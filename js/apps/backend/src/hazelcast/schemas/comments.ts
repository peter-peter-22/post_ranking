import { hazelClient } from "../connect";

export type Comment = { __key: string, userId: string, createdAt: number, rootPostId: string }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING comments (
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
    'partition-attribute' = 'rootPostId'
)
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS recent_replies_of_post
ON comments ("rootPostId","replyingTo","createdAt")
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS replies_of_user_on_post
ON comments ("rootPostId","replyingTo","userId")
TYPE HASH
`);

export const commentSectionsMap = await hazelClient.getMap<string, Comment>('comments');