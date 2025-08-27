package com.me;

import java.sql.ResultSet;
import java.util.Optional;

import com.hazelcast.core.HazelcastJsonValue;
import com.hazelcast.internal.json.JsonObject;

public class Post {
    public static HazelcastJsonValue parse(ResultSet rs) {
        try {
            JsonObject json = new JsonObject()
                    .add("__key", rs.getString("id"))
                    .add("text", rs.getString("text"))
                    .add("likeCount", rs.getInt("likeCount"))
                    .add("replyCount", rs.getInt("replyCount"))
                    .add("clickCount", rs.getInt("clickCount"))
                    .add("viewCount", rs.getInt("viewCount"))
                    .add("topic", rs.getString("topic"))
                    .add("engaging", rs.getFloat("embedding"))
                    .add("replyingTo", rs.getString("replyingTo"))
                    .add("createdAt", rs.getDate("createdAt").getTime())
                    .add("embedding", rs.getString("embedding"))
                    .add("media", rs.getString("media"))
                    .add("deleted", rs.getBoolean("deleted"))
                    .add("rootPostId", rs.getString("rootPostId"))
                    .add("partition",
                            Optional.ofNullable(rs.getString("replyingTo")).orElse(rs.getString("id")));
            return new HazelcastJsonValue(json.toString());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
