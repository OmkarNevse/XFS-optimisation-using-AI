import subprocess
import json
import csv
import os.path
from datetime import datetime, timedelta

def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.read().decode()
    return res

def read_audit():
    cmd = "aureport -f -i"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.read().decode()
    return res

def clear_audit():
    cmd = "sudo truncate -s 0 /var/log/audit/audit.log"
    p = subprocess.run(cmd, shell=True)

def check_file(dir:str) ->bool:
    cmd = f"""if [ -d "{dir}" ]; then
        echo "d"
    else
        echo "f"
    fi"""
    
    result = run_command(cmd)
    result.strip()
    if(result[0] == 'd'): return False
    else: return True

def check_if_valid(dir: str) -> bool:
    cmd = f"""if [ -e "{dir}" ]; then
    echo "valid"
    else
        echo "notvalid"
    fi"""
    
    result = run_command(cmd)
    # print(result)
    # result.strip()
    if('notvalid' in result): return False
    else: return True

class Pair:
    def _init_(self, first, second) -> None:
        self.first = first
        self.second = second

    def _eq_(self, __value: object) -> bool:
        return self.first == __value.first and self.second == __value.second

def get_file_access_frequencies():
    # Use the ausearch command to retrieve audit logs for file access events
    audit_log = read_audit()
    
    # Split the log entries into lines
    log_entries = audit_log.split("\n")[6:]
    if(len(log_entries)>0):log_entries.pop()

    # file_access_counts = {}

    # Parse each log entry
    # if(not os.path.isfile('saved_progress.txt')):
    #     f = open("saved_progress.txt", "w")

    already_present = {}
    new_data = {}

    with open('dataset.txt', 'w+') as file:
        # Create a dictionary to store file access frequencies
        if(file.read() ==""):already_present=json.loads("{}")
        else: already_present = json.loads(file.read())

        # allDateTimesFD = []

        for entry in log_entries:
            each_entry = entry.split(' ')
            #print(each_entry)
            
            
            
            if (len(each_entry)>=9 and each_entry[5] == 'yes' and each_entry[4] == 'openat'):
                file_path = each_entry[3]
                
                # already_present[file_path] += 
                # print(check_file(each_entry[3]))
                # print('file') if check_file(each_entry[3]) else print('dir')
                if(not check_file(each_entry[3])):continue

                if (file_path in already_present):
                    already_present[file_path] += 1
                else:
                    already_present[file_path] = 1

                dateFormat = each_entry[1].split('/')
                dateFormat = list(map(int, dateFormat))
                timeFormat = each_entry[2].split(':')
                timeFormat = list(map(int, timeFormat))

                datetimeObject: datetime = datetime(dateFormat[2], dateFormat[1], dateFormat[0], timeFormat[0], timeFormat[1], timeFormat[2])

                # newPair = Pair(datetime(dateFormat[2], dateFormat[1], dateFormat[0], timeFormat[0], (timeFormat[1] // 10) * 10, 0), file_path)

                newPair = str(dateFormat[2]) + '/' + str(dateFormat[1]) + '/' + str(dateFormat[0]) + ' ' + str(timeFormat[0]) + ':' + str((timeFormat[1] // 10) * 10) + ':' + '00' + ' ' + file_path

                if newPair in new_data.keys():
                    new_data[newPair] += 1
                else:
                    new_data[newPair] = 1

                # d = {}
                # d[datetimeObject] = file_path

                # allDateTimesFD.append(d)
                
                # Extract the file path from the log entry
                # file_path = entry.split("name=")[1].split(" ")[0]

                # # Update the access count for the file
                # if file_path in file_access_counts:
                #     file_access_counts[file_path] += 1
                # else:
                #     file_access_counts[file_path] = 1
    
        # file.write(json.dumps(already_present))
    
        # allDateTimesFD.sort(key=lambda x : list(x.keys())[0])
        # print(allDateTimesFD)



        # if (len(allDateTimesFD) > 0):
        #     curr_date = list(allDateTimesFD[0].keys())[0].date()

        #     entriesForEachDate = {}
        #     for x in allDateTimesFD:
        #         if list(x.keys())[0].date() == curr_date:
        #             c = datetime
        #         else:

        #             curr_date = list(x.keys())[0].date()
        # else:
        #     print("already up to date!")

        print(new_data)

        file_exists = False
        if os.path.exists('csv_data.csv'):
            file_exists = True

        with open('csv_data.csv', 'a', newline='') as csv_file:
            fieldnames = ['date', 'startTime', 'endTime', 'filePath', 'frequency']
            writer =csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            
            for key in new_data:
                temp = {}
                splitKey = key.split(' ')

                print("key ==----", splitKey)

                dateFormat = splitKey[0].split('/')
                dateFormat = list(map(int, dateFormat))
                timeFormat = splitKey[1].split(':')
                timeFormat = list(map(int, timeFormat))
                
                print(dateFormat)
                strToDate = datetime(year=dateFormat[0], month=dateFormat[1], day=dateFormat[2], hour=timeFormat[0], minute=timeFormat[1], second=timeFormat[2])

                strToDateEnd = strToDate + timedelta(minutes=10)

                temp['date'] = splitKey[0]
                temp['startTime'] = strToDate.time()
                temp['endTime'] = strToDateEnd.time()
                temp['filePath'] = splitKey[2]
                temp['frequency'] = new_data[key]

                writer.writerow(temp)

    with open('dataset.txt', 'w') as file:
        file.write(json.dumps(already_present))
    
    clear_audit()
    return already_present

#location of the directory you want to track
run_command("sudo auditctl -w /home/yash/be_proj_git/ -p rwxa")


file_access_frequencies = get_file_access_frequencies()

# Print file access frequencies
# print("File Access Frequencies:")

# print(file_access_frequencies)
# for file_path, count in file_access_frequencies.items():
#     if(not check_if_valid(file_path)):
#         file_access_frequencies.pop(file_path)
#         #also remove soft links if present
#     else :print(f"{file_path}: {count} times")

# for key in list(file_access_frequencies):
#     if(not check_if_valid(key)):
#         file_access_frequencies.pop(key)
#     else: print(f"{key}: {file_access_frequencies[key]} times")