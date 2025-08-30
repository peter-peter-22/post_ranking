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

import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.HazelcastJsonValue;
import com.hazelcast.internal.json.JsonObject;
import com.hazelcast.map.IMap;
import com.hazelcast.map.MapLoaderLifecycleSupport;
import com.hazelcast.map.MapStore;

public class UserFeaturesMapStore implements MapStore<String, HazelcastJsonValue>, MapLoaderLifecycleSupport {
    static DataSource ds;
    static HazelcastInstance hz;
    static IMap<String, HazelcastJsonValue> followersMap;
    static IMap<String, HazelcastJsonValue> followingMap;

    @Override
    public void init(HazelcastInstance hazelcastInstance, Properties properties, String mapName) {
        System.out.println("Initializing comment sections");
        ConnectionManager.register(hazelcastInstance);
        ds = CockroachConnectionFactory.getDataSource();
        hz = hazelcastInstance;
        followersMap = hz.getMap("followers");
        followingMap = hz.getMap("following");
    }

    @Override
    public HazelcastJsonValue load(String key) {
        System.out.println(String.format("User features fallback for key '%s'", key));
        try (Connection con = ds.getConnection()) {
            PreparedStatement ps = con.prepareStatement("SELECT * FROM follows WHERE \"followedId\"=?");
            ps.setString(1, key);
            try (ResultSet rs = ps.executeQuery()) {
                Map<String, HazelcastJsonValue> followers = new HashMap<>();
                if (rs.next()) {
                    String id = rs.getString("id");
                    followers.put(id, Post.parse(rs));
                }
                followersMap.putAll(followers);
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