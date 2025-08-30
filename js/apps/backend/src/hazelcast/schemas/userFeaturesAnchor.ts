import { hazelClient } from "../connect";

export type UserFeaturesAnchor = { __key: string }

await hazelClient.getSql().execute(`
CREATE OR REPLACE MAPPING user_features_anchors (
    __key VARCHAR,     
)
TYPE IMap
OPTIONS (
    'keyFormat' = 'varchar',
    'valueFormat' = 'json-flat'
)
`);

export const userFeaturesAnchorsMap = await hazelClient.getMap<string, UserFeaturesAnchor>('user_features_anchors');