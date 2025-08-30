import { hazelClient } from "../connect";

export type RankedPostAnchor = { __key: string, userId: string, createdAt: number }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING ranked_post_anchors (
    __key VARCHAR,
    userId VARCHAR,
    createdAt INTEGER,
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
    'partition-attribute' = 'userId'
)
`);

await hazelClient.getSql().execute(`
CREATE INDEX IF NOT EXISTS posts_of_user
ON comments ("userId")
TYPE HASH
`);

export const commentSectionsMap = await hazelClient.getMap<string, RankedPostAnchor>('ranked_post_anchors');