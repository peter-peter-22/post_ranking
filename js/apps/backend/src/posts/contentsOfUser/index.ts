import { and, desc, eq, lt } from "drizzle-orm"
import { db } from "../../db"
import { posts } from "../../db/schema/posts"
import { User } from "../../db/schema/users"
import { postsPerRequest } from "../../redis/feeds/postFeeds/common"
import { getEnrichedPosts } from "../../redis/postContent/enrich"
import { SingleDatePageParams } from "../common"
import { noPending } from "../filters"

export type UserContentsPageParams = {
    main?: SingleDatePageParams
}

export async function getUserContents({
    user,
    pageParams,
    offset,
    targetUserId,
    replies
}: {
    user?: User,
    pageParams?: UserContentsPageParams,
    offset: number,
    targetUserId: string,
    replies: boolean
}) {
    // Get if this is the first page
    const firstPage = offset === 0

    // Get the posts
    const data = await userContentCandidates({ targetUserId, replies, pageParams: pageParams?.main, firstPage, user })

    // Merge page params
    const allPageParams: UserContentsPageParams = {
        main: data?.pageParams,
    }
    // Return the ranked posts and the page params
    return { data: data?.data || [], pageParams: allPageParams }
}

/** Get the replies or posts of a user.  */
export async function userContentCandidates({
    user,
    firstPage,
    pageParams,
    replies,
    targetUserId
}: {
    user?: User,
    firstPage: boolean,
    pageParams?: SingleDatePageParams,
    replies: boolean,
    targetUserId: string
}) {
    if (!firstPage && !pageParams) return

    // Query
    const q = db
        .select({ id: posts.id })
        .from(posts)
        .where(and(
            eq(posts.userId, targetUserId),
            eq(posts.isReply, replies),
            pageParams && lt(posts.createdAt, new Date(pageParams.maxDate)),
            noPending(),
        ))
        .orderBy(desc(posts.createdAt))
        .limit(postsPerRequest)
    const myPosts = await q

    // Enrich
    const enrichedPosts = await getEnrichedPosts(myPosts.map(p => p.id), user)

    // Get next page params
    const nextPageParams: SingleDatePageParams | undefined = enrichedPosts.length === postsPerRequest ? {
        maxDate: enrichedPosts[enrichedPosts.length - 1].createdAt.toISOString()
    } : undefined

    // Return
    return { data: myPosts, pageParams: nextPageParams }
}