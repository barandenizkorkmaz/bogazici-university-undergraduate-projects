import question.TrieMap;

public class Main {
    public static void main(String[] args){
        TrieMap<String> trieMap = new TrieMap<>();
        trieMap.insert("ab", "ab");
        trieMap.insert("cb", "cb");
        trieMap.insert("acb", "acb");
        trieMap.insert("abc", "abc");

        for(String value : trieMap.returnBFSOrder()){
            System.out.print(value + "\t");
        }
        System.out.println();
        System.out.println(trieMap.search("ab"));
        System.out.println(trieMap.nodeCount());
        trieMap.delete("ab");
        System.out.println(trieMap.search("ab"));
        System.out.println(trieMap.nodeCount());
        System.out.println(TrieMap.containsSubstr("natalia", "ata"));
        System.out.println(TrieMap.wordCount("tal  at  sal  aa   ata   kask   ata    ata", "ata"));
        String[] res = TrieMap.uniqueWords("tal  at  sal  aa   ata   kask   ata    ata");
        for(String word : res){
            System.out.print(word + "\t");
        }

    }
}