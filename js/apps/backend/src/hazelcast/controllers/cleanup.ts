import { hazelClient } from "../connect";

/** Remove expired dependent entries from the cache. 
 * @todo Not optimized. The anchors and their related data is always on the same node, but SQL ignores it.
*/
export async function cleanCache() {
    // Comments
    hazelClient.getSql().execute('DELETE FROM posts WHERE "replyingTo" IS NOT NULL AND NOT EXISTS (SELECT * FROM comment_sections WHERE key="replyingTo")');
    // TODO: config comment section loading in the cache
}