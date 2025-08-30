import { cleanCache } from "../../../hazelcast/controllers/cleanup";
import { emptyJob } from "../emptyJob";

export const expireJobs = emptyJob({
    name: "expire",
    defaultOptions: {
        repeat: { every: 20 * 1000 }
    },
    handler: cleanCache
})