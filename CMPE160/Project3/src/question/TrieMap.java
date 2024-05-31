package question;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

public class TrieMap<T> extends TrieMapBase<T> {

    static class Node<T>{
        public Node<T>[] children;
        public String key;
        public T value;
        public boolean isWord;

        /**
         * Constructor for top level root node.
         */
        public Node()
        {
            children = new Node[26];
            isWord = false;
            key = "";
            value = null;
        }

        /**
         * Constructor for child node.
         */
        public Node(String word,T value)
        {
            this();
            this.key = word;
            this.value = value;
            this.isWord = true;
        }

    }

    public Node<T> root;
    private int numOfNodes = 0;

    public TrieMap(){
        root = new Node<>();
    }

    @Override
    public void insert(String key, T value) {
        // TODO Auto-generated method stub
        Node<T> node = this.root;
        StringBuilder stringBuilder = new StringBuilder();
        for(char c : key.toCharArray()){
            int index = c - 'a';
            if(node.children[index] == null){
                node.children[index] = new Node<>();
            }
            stringBuilder.append(c);
            node.children[index].key = stringBuilder.toString();
            node = node.children[index];
        }
        node.value = value; // value can be overridden
        if(!node.isWord){
            node.isWord = true;
            this.numOfNodes++;
        }
    }

    @Override
    public boolean delete(String key) {
        // TODO Auto-generated method stub
        Node<T> node = this.root;
        for(char c : key.toCharArray()){
            int index = c - 'a';
            if(node.children[index] == null){
                return false;
            }
            node = node.children[index];
        }
        if(node.isWord){
            node.value = null;
            node.isWord = false;
            this.numOfNodes--;
            return true;
        }
        return false;
    }


    @Override
    public T search(String key) {
        // TODO Auto-generated method stub
        Node<T> node = this.root;
        for(char c : key.toCharArray()){
            int index = c - 'a';
            if(node.children[index] == null){
                return null;
            }
            node = node.children[index];
        }
        return node.value;
    }

    @Override
    public boolean contains(String key) {
        // TODO Auto-generated method stub
        Node<T> node = this.root;
        for(char c : key.toCharArray()){
            int index = c - 'a';
            if(node.children[index] == null){
                return false;
            }
            node = node.children[index];
        }
        return node.isWord;
    }

    @Override
    public int nodeCount() {
        // TODO Auto-generated method stub
        return this.numOfNodes;
    }

    @Override
    public ArrayList<T> returnBFSOrder() {
        // TODO Auto-generated method stub
        ArrayList<T> result = new ArrayList<>();
        Queue<Node<T>> queue = new LinkedList<>();
        queue.add(this.root);
        while(!queue.isEmpty()){
            Node<T> current = queue.poll();
            if(current.isWord){
                result.add(current.value);
            }
            for(Node<T> child : current.children){
                if(child != null){
                    queue.add(child);
                }
            }
        }
        return result;
    }

    private static int getSingleChildIndex(Node root){
        for(int i = 0; i < root.children.length; i++){
            if(root.children[i] != null){
                return i;
            }
        }
        return -1;
    }


    private static boolean containsSubstring(Node<String> root, String substring){
        int i = 0;
        while (getSingleChildIndex(root) == substring.charAt(i) - 'a'){
            root = root.children[getSingleChildIndex(root)];
            i++;
            if(i == substring.length())return true;
        }
        return false;
    }

    /**
     * Returns 	true if key appears in text as a substring;
     * 			false, otherwise
     *
     * Use Trie data structure to solve the problem
     */
    public static boolean containsSubstr(String text, String key) {
        /*
            To solve this task, you need 2 steps:
                1. Insert text into trie.
                2. If you can somehow walk on the path of trie map, then return true.
                    Otherwise, return false.
         */
        TrieMap<String> trie = new TrieMap<>();
        trie.insert(text, text);
        Node<String> current = trie.root;
        while(current != null){
            if(containsSubstring(current, key))return true;
            int index = getSingleChildIndex(current);
            if(index == -1)return false;
            current = current.children[index];
        }
        // ...
        return false;
    }

    /**
     * Returns how many times the word in the parameter appears in the book.
     * Each word in book is separated by a white space.
     *
     * Use Trie data structure to solve the problem
     */
    public static int wordCount(String book, String word) {
        String[] wordsArray = book.split("\\s+");
        TrieMap<Integer> trie = new TrieMap<>();
        for(String _word : wordsArray){
            if(trie.search(_word) != null){
                int value = trie.search(_word);
                trie.insert(_word, value + 1);
            }
            else{
                trie.insert(_word, 1);
            }
        }
        if(trie.search(word) == null){
            return 0;
        }
        return trie.search(word);
    }

    /**
     * Returns the array of unique words in the book given as parameter.
     * Each word in book is separated by a white space.
     *
     * Use Trie data structure to solve the problem
     */
    public static String[] uniqueWords(String book) {
        String[] wordsArray = book.split("\\s+");
        TrieMap<String> trie = new TrieMap<>();
        for(String _word : wordsArray){
            trie.insert(_word, _word);
        }
        return trie.returnBFSOrder().toArray(new String[0]);
    }

    /**
     * Recommends word completions based on the user history.
     *
     * Among all the strings in the user history, the method takes
     * those that start with a given incomplete word S,
     * sort the words according to their frequencies (how many
     * times they are written), and recommend the 3 most frequently written ones.
     *
     * @param userHistory
     * 			the words written previously by the user
     *
     * @param incompleteWords
     * 			the list of strings to be autocompleted
     * @return
     * 			a Sx3 array that contains the recommendations
     * 			for each word to be autocompleted.
     *
     * Use Trie data structure to solve the problem
     */
    public static String[][] autoComplete(String[] userHistory, String[] incompleteWords){
        return null;
    }

}