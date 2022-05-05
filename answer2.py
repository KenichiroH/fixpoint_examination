def server_disorder_output(logfile, N):
  with open(logfile, 'r') as f:
    dic_servers = {}
    for eachlog in f:
      eachlog = eachlog.split(',')
      if eachlog[1] not in dic_servers.keys():
        dic_servers[eachlog[1]] = [[eachlog[0], eachlog[2]]]
      else:
        dic_servers[eachlog[1]].append([eachlog[0], eachlog[2]])

    for server, condition in dic_servers.items():
      for i, each_condition in enumerate(condition):
        since_time_list = []
        until_time_list = []
        if '-' in each_condition[1] and (i == 0 or (i >= 1 and '-' not in condition[i-1][1])):

        #次に応答するまで何回連続でタイムアウトしたかを調べる（j+1回）
          j = 0
          while i+j+1 < len(condition) and '-' in condition[i+j+1][1]: 
              j += 1

          if j+1 >= N:#もしN回以上連続なら、since_timeとuntil_timeを定義
            since_time_list.append(each_condition[0])
            since_time = min(since_time_list)
            if i+j+1 == len(condition):
              until_time = "now"
            else:
              until_time_list.append(condition[i+j+1][0])
              until_time = max(until_time_list)

            with open('output2.txt', 'a') as o:
                  print('SERVER ERROR: server_name: "'+server+'" since '+since_time+' until '+until_time, file=o)


server_disorder_output("log2.txt", 3) #暫定的にfilename='log2.txt',N=3としています。実行する際は「log2.txt」,「3」を書き換えてください。