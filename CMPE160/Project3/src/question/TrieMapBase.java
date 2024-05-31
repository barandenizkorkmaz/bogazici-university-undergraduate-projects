package question;

import java.util.ArrayList;

public abstract class TrieMapBase<T> {
    public abstract void insert(String key, T value);

    public abstract boolean delete(String key);

    public abstract T search(String key);

    public abstract boolean contains(String key);

    public abstract int nodeCount();

    public abstract ArrayList<T> returnBFSOrder();
}
