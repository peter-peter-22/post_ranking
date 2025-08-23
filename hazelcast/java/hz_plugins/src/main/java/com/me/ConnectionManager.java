package com.me;

import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.LifecycleEvent;
import com.hazelcast.core.LifecycleListener;

public class ConnectionManager implements LifecycleListener {
    public static boolean registered = false;

    @Override
    public void stateChanged(LifecycleEvent event) {
        if (event.getState() == LifecycleEvent.LifecycleState.SHUTDOWN) {
            CockroachConnectionFactory.close();
        }
    }

    public static synchronized void register(HazelcastInstance hz) {
        if (!registered) {
            hz.getLifecycleService().addLifecycleListener(new ConnectionManager());
            registered = true;
        }
    }
}
