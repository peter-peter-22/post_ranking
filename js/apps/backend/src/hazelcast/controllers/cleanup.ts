import { hazelClient } from "../connect";

/** Remove expired dependent entries from the cache. 
 * @todo This possibbly can be optimized further.
*/
export async function cleanCache() {
    // Comments
    const res = await hazelClient.getSql().execute('DELETE FROM posts WHERE "replyingTo" IS NOT NULL AND NOT EXISTS (SELECT * FROM comment_sections WHERE __key="rootPostId")');
    console.log(`Deleted ${res.updateCount} comments during cleanup.`)
}