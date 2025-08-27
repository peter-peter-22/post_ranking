import { hazelClient } from "../connect";

export type CommentSectionAnchor = { __key: string }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING posts (
    __key VARCHAR,     
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
)
`);

export const commentSectionsMap = await hazelClient.getMap<string, string>('comment_sections');