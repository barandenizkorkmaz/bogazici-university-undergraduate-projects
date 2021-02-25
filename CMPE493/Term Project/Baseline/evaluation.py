def getResultsFile(topKResults:dict):
    # FORMAT: query-id Q0 document-id rank score STANDARD
    with open('RESULTS', 'w') as f:
        for queryId in topKResults:
            for i, resTuple in enumerate(topKResults[queryId]):
                docId = resTuple[0]
                cosineSimilarity = resTuple[1]
                rank = i + 1
                print("%s\tQ0\t%s\t%d\t%f\tSTANDARD" % (queryId,docId,rank,cosineSimilarity), file=f)