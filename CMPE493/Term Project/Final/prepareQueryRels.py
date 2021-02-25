def getQueryRels(subset):
    srcFile = open("qrels-covid_d5_j0.5-5.txt", "r")
    targetFileName = "qrels-covid_d5_j0.5-5_training.txt" if subset.lower() == "training" else "qrels-covid_d5_j0.5-5_test.txt"
    MOD_RESULT = 1 if subset.lower() == "training" else 0
    targetFile = open(targetFileName, "w")
    for line in srcFile.readlines():
        lineTuples = line.split()
        if int(lineTuples[0]) % 2 == MOD_RESULT:
            targetFile.write(line)
    srcFile.close()
    targetFile.close()

getQueryRels("test")