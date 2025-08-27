package com.me;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.TimeUnit;

import javax.sql.DataSource;

import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.HazelcastJsonValue;
import com.hazelcast.internal.json.JsonObject;
import com.hazelcast.map.MapLoaderLifecycleSupport;
import com.hazelcast.map.MapStore;

public class CommentSectionMapStore implements MapStore<String, HazelcastJsonValue>, MapLoaderLifecycleSupport {
    private DataSource ds;
    private HazelcastInstance hz;

    @Override
    public void init(HazelcastInstance hazelcastInstance, Properties properties, String mapName) {
        System.out.println("Initializing comment sections");
        ConnectionManager.register(hazelcastInstance);
        ds = CockroachConnectionFactory.getDataSource();
        hz = hazelcastInstance;
    }

    @Override
    public HazelcastJsonValue load(String key) {
        System.out.println(String.format("Comment section fallback for key '%s'", key));
        try (Connection con = ds.getConnection()) {
            PreparedStatement ps = con.prepareStatement("SELECT * FROM posts WHERE \"rootPostId\"=?");
            ps.setString(1, key);
            try (ResultSet rs = ps.executeQuery()) {
                var postsMap = hz.getMap("posts");
                if (rs.next()) {
                    String id = rs.getString("id");
                    var post = Post.parse(rs);
                    postsMap.put(id, post, 0, TimeUnit.SECONDS);
                }
            }
            JsonObject json = new JsonObject().add("__key", key);
            return new HazelcastJsonValue(json.toString());
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
    }

    @Override
    public void store(String key, HazelcastJsonValue value) {
    }

    @Override
    public void storeAll(Map<String, HazelcastJsonValue> map) {
    }

    @Override
    public void delete(String key) {
    }

    @Override
    public void deleteAll(Collection<String> keys) {
    }
}