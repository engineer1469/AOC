def digest():
    with open('2024/2/input.txt', 'r') as f:
        #for each line in the file(for example: 48 50 51 53 55 56 59 58), split the line by space into a list integers
        #so we return a list of list of integers
        return [[int(x) for x in line.split()] for line in f]

def isUniform(report):
    #if the numbers in the report are all increasing or decreasing
    return report == sorted(report) or report == sorted(report, reverse=True)

def isSafeReport(report):
    for i in range(len(report)):
        if i == len(report) - 1:
            return True
        distance = abs(report[i] - report[i+1])

        if distance > 3 or distance == 0:
            return False
        
        if not isUniform(report):
            return False

def isSafeReportWithDampener(report):
    if isSafeReport(report):
        return True
    
    for i in range(len(report)):
        reportCopy = report.copy()
        reportCopy.pop(i)
        if isSafeReport(reportCopy):
            return True
        
    return False

def countSafeReports(reports):
    count = 0
    for report in reports:
        if isSafeReportWithDampener(report):
            count += 1
    return count

def main():
    data = digest()
    print(countSafeReports(data))
    

if __name__ == "__main__":
    main()