package com.me;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import javax.sql.DataSource;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.hazelcast.core.HazelcastJsonValue;
import com.hazelcast.map.MapLoaderLifecycleSupport;
import com.hazelcast.map.MapStore;

public class PostsMapStore implements MapStore<String, HazelcastJsonValue>, MapLoaderLifecycleSupport {
    private final ObjectMapper mapper = new ObjectMapper();
    private DataSource ds;

    @Override
    public void init(com.hazelcast.core.HazelcastInstance hazelcastInstance, Properties properties, String mapName) {
        System.out.println("Initializing posts");
        ConnectionManager.register(hazelcastInstance);
        ds = CockroachConnectionFactory.getDataSource();
    }

    @Override
    public HazelcastJsonValue load(String key) {
        System.out.println(String.format("Posts fallback for key '%s'", key));
        try (Connection con = ds.getConnection()) {
            PreparedStatement ps = con.prepareStatement("SELECT * FROM posts WHERE id = ?");
            ps.setString(1, key);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                   return Post.parse(rs);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public List<String> loadAllKeys() {
        return null;
    }

    @Override
    public HashMap<String, HazelcastJsonValue> loadAll(Collection<String> keys) {
        return null;
    }

    @Override
    public void destroy() {
        System.out.println("Destroy");
    }

    @Override
    public void store(String key, HazelcastJsonValue value) {
        System.out.println(String.format("Saving post '%s'", key));
        try (Connection con = ds.getConnection()) {
            JsonNode node = mapper.readTree(value.toString());
            Integer likeCount = node.get("likeCount").asInt();
            Integer replyCount = node.get("replyCount").asInt();
            Integer clickCount = node.get("clickCount").asInt();
            Integer viewCount = node.get("viewCount").asInt();
            PreparedStatement ps = con.prepareStatement(
                    "UPDATE posts SET \"likeCount\"=?, \"replyCount\"=?, \"clickCount\"=?, \"viewCount\"=? WHERE id = ?");
            ps.setInt(1, likeCount);
            ps.setInt(2, replyCount);
            ps.setInt(3, clickCount);
            ps.setInt(4, viewCount);
            ps.setString(5, key);
            ps.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void storeAll(Map<String, HazelcastJsonValue> map) {
        System.out.println("Store all");
        map.entrySet().stream().forEach(e -> {
            store(e.getKey(), e.getValue());
        });
    }

    @Override
    public void delete(String key) {
        System.out.println("Delete");
    }

    @Override
    public void deleteAll(Collection<String> keys) {
        System.out.println("Delete all");
    }
}