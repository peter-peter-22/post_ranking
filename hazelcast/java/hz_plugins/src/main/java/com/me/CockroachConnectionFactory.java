package com.me;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import javax.sql.DataSource;

public class CockroachConnectionFactory {
    private static HikariDataSource ds;

    public static synchronized DataSource getDataSource() {
        if (ds == null) {
            HikariConfig config = new HikariConfig();
            config.setJdbcUrl("jdbc:postgresql://db:26257/main?sslmode=disable");
            config.setUsername("root");
            config.setPassword("");
            config.setMaximumPoolSize(100);
            config.setConnectionTimeout(3000);
            config.setDriverClassName("org.postgresql.Driver");
            ds = new HikariDataSource(config);
            System.out.println("Connected to SQL");
        }
        return ds;
    }

    public static synchronized void close() {
        if (ds != null) {
            ds.close();
            ds = null;
            System.out.println("Closed SQL");
        }
    }
}